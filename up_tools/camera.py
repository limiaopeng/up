"""Camera tools."""
# pylint: disable=invalid-name
import numpy as np


def rotateY(points, angle):
    """Rotate all points in a 2D array around the y axis."""
    ry = np.array([
        [np.cos(angle),     0.,     np.sin(angle)],  # pylint: disable=bad-whitespace
        [0.,                1.,     0.           ],  # pylint: disable=bad-whitespace
        [-np.sin(angle),    0.,     np.cos(angle)]  # pylint: disable=bad-whitespace
    ])
    return np.dot(points, ry)

def rotateX( points, angle ):
    rx = np.array([
        [1.,    0.,                 0.           ],
        [0.,    np.cos(angle),     -np.sin(angle)],
        [0.,    np.sin(angle),     np.cos(angle) ]
    ])
    return np.dot(points, rx)

def rotateZ( points, angle ):
    rz = np.array([
        [np.cos(angle),     -np.sin(angle),     0. ],
        [np.sin(angle),     np.cos(angle),      0. ],
        [0.,                0.,                 1. ]
    ])
    return np.dot(points, rz)
