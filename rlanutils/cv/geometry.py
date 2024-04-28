from typing import List, Union, Tuple

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


class Box3d:
    def __init__(self, position: np.ndarray, scale: np.ndarray, quat: np.ndarray) -> None:
        """_summary_

        Parameters
        ----------
        position : np.ndarray
            of shape (3, )
        scale : np.ndarray
            of shape (3, )
        quat : np.ndarray
            of shape (4, ), scalar-last (x, y, z, w) format

        Returns
        -------
        _type_
            _description_
        """
        self.position = position
        self.scale = scale
        self.quat = quat
        self._corners = None
    
    @property
    def corners(self) -> np.ndarray:
        """
        Returns
        -------
        np.ndarray
            of shape (8, 3)
        """
        if self._corners is None:
            self._corners = self.calc_box_corners(self.position, self.scale, self.quat)
        return self._corners
    
    def calc_box_corners(self) -> np.ndarray:
        """
        Parameters
        -------
        np.ndarray
            of shape (8, 3)
        """
        corners = np.array([
            [0.5, -0.5, -0.5],
            [0.5, 0.5, -0.5],
            [0.5, 0.5, 0.5],
            [0.5, -0.5, 0.5],
            [-0.5, -0.5, -0.5],
            [-0.5, 0.5, -0.5],
            [-0.5, 0.5, 0.5],
            [-0.5, -0.5, 0.5],
        ])
        corners = corners * self.scale[None]
        corners = corners @ self.quat.as_matrix().T
        corners = corners + self.position
        return corners

    @classmethod
    def from_pos_scale_euler(cls, pos_x: float, pos_y: float, pos_z: float, scale_x: float, scale_y: float, scale_z: float, rot_euler_x: float, rot_euler_y: float, rot_euler_z: float, degree: bool = False):
        pos = np.array([pos_x, pos_y, pos_z], dtype=np.float32)
        scale = np.array([scale_x, scale_y, scale_z], dtype=np.float32)
        quat = R.from_euler("XYZ", [[rot_euler_x, rot_euler_y, rot_euler_z]], degree=degree)
        return cls(pos, scale, quat)


__all__ = ["xyzq2mat", "points3d_to_homo", "homo_to_points3d", "Box3d"]
