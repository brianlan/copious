from typing import List, Union

import numpy as np
from scipy.spatial.transform import Rotation as R


def xyzq2mat4x4(x, y, z, qx, qy, qz, qw) -> np.ndarray:
    rot = R.from_quat([qx, qy, qz, qw]).as_matrix()
    T = np.eye(4)
    T[:3, 3] = [x, y, z]
    T[:3, :3] = rot
    return T


def points3d_to_homo(points3d: np.ndarray) -> np.ndarray:
    return np.concatenate((points3d, np.ones(len(points3d))[:, None]), axis=1)


def homo_to_points3d(points_homo: np.ndarray) -> np.ndarray:
    return points_homo[:, :3]
