"""Define the capsule target."""
import numpy as np
import chumpy as ch
try:
    # Robustify against setup.
    from smpl.lbs import verts_core
except ImportError:
    # pylint: disable=import-error
    try:
        from psbody.smpl.lbs import verts_core
    except:
        from smpl_webuser.lbs import verts_core

from capsule_man import get_capsules, set_sphere_centers,\
  get_sphere_bweights, collisions, capsule_dist


class SphereCollisions(ch.Ch):
  dterms = ('pose', 'betas')
  terms = ('regs', 'model')
    
  def update_capsules_and_centers(self):
    centers = [set_sphere_centers(capsule) for capsule in self.capsules]    
    count = 0 
    for capsule in self.capsules:
        capsule.center_id = count
        count += len(capsule.centers)
    self.sph_vs = ch.vstack(centers)
    self.sph_weights = get_sphere_bweights(self.sph_vs, self.capsules)
    self.ids0 = []
    self.ids1 = []
    self.radiuss = []
    self.caps_pairs = []
    for collision in collisions:
        if hasattr(self, 'no_hands'):
            (id0, id1, rd) = capsule_dist(self.capsules[collision[0]], self.capsules[collision[1]], increase_hand=False)
        else:
            (id0, id1, rd) = capsule_dist(self.capsules[collision[0]], self.capsules[collision[1]])
        self.ids0.append(id0.r)
        self.ids1.append(id1.r)
        self.radiuss.append(rd)
        self.caps_pairs.append(['%02d_%02d' % (collision[0], collision[1])]*len(id0))
    self.ids0 = np.concatenate(self.ids0).astype(int) # numpy?
    self.ids1 = np.concatenate(self.ids1).astype(int)
    self.radiuss = np.concatenate(self.radiuss)
    self.caps_pairs = np.concatenate(self.caps_pairs)
    assert(self.caps_pairs.size==self.ids0.size)
    assert(self.radiuss.size==self.ids0.size)

  def update_pose(self):
    self.sph_v = verts_core(self.pose,
                            self.sph_vs,
                            self.model.J,
                            self.sph_weights,
                            self.model.kintree_table,
                            want_Jtr=False)[0]

  def get_objective(self):
    return ch.sum((ch.exp(-((ch.sum((self.sph_v[self.ids0]-
                                     self.sph_v[self.ids1])**2,
                                    axis=1))/(self.radiuss))/2.))**2)**.5

  def compute_r(self):
    return self.get_objective().r

  
  def compute_dr_wrt(self, wrt):
    if wrt is self.pose:
        return self.get_objective().dr_wrt(wrt)

  def on_changed(self, which):
    if 'regs' in which:
        self.length_regs = self.regs['betas2lens']
        self.rad_regs = self.regs['betas2rads']
        #self.capsules = get_capsules(self.model)
        #self.prev_betas = None

    if 'betas' in which:
        if not hasattr(self, 'capsules'):
            self.capsules = get_capsules(self.model,
                                         wrt_betas=self.betas,
                                         length_regs=self.length_regs,
                                         rad_regs=self.rad_regs)
        self.update_capsules_and_centers()

    if 'pose' in which:
      self.update_pose()
