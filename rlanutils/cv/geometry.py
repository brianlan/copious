from typing import List, Union

import numpy as np
from scipy.spatial.transform import Rotation as R


def xyzq2mat(
    x: float, y: float, z: float, qx: float, qy: float, qz: float, qw: float, as_homo: bool = False
) -> np.ndarray:
    """A helper function that convert xyzq (7 values) representation to transformation matrix representation.

    Parameters
    ----------
    x : float
        x coordinate of the translation
    y : float
        y coordinate of the translation
    z : float
        z coordinate of the translation
    qx : float
        x component of the rotation Quaternion
    qy : float
        y component of the rotation Quaternion
    qz : float
        z component of the rotation Quaternion
    qw : float
        w component of the rotation Quaternion
    as_homo: bool
        if true, the matrix will be saved as homogeneous (4x4), otherwise, it will be saved as 3x4

    Returns
    -------
    np.ndarray
        of shape (3, 4) if as_homo == False, otherwise, (4, 4)
    """
    rot = R.from_quat([qx, qy, qz, qw]).as_matrix()
    T = np.eye(4)
    T[:3, 3] = [x, y, z]
    T[:3, :3] = rot
    if as_homo:
        T = T[:3, :]
    return T


def points3d_to_homo(points3d: np.ndarray) -> np.ndarray:
    return np.concatenate((points3d, np.ones(len(points3d))[:, None]), axis=1)


def homo_to_points3d(points_homo: np.ndarray) -> np.ndarray:
    return points_homo[:, :3]


__all__ = ["xyzq2mat", "points3d_to_homo", "homo_to_points3d"]
