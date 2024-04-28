import math

import pytest
import numpy as np

from rlanutils.cv.geometry import points3d_to_homo, Box3d


def test_to_homo():
    np.testing.assert_almost_equal(
        points3d_to_homo(
            np.array([[0, 2, 3], [0.1, -0.2, 0.3]])
        ),
        np.array([[0, 2, 3, 1], [0.1, -0.2, 0.3, 1]])
    )


@pytest.fixture
def box3d_psr_1():
    return [0, 0, 0, 5, 2, 1.8, 0, 0, math.pi / 2]

@pytest.fixture
def box3d_psr_2():
    return [6, 8, -0.05, 5, 2, 1.8, 0, 0, -math.pi / 2]


def test_box3d_get_corners1(box3d_psr_1):
    box = Box3d.from_pos_scale_euler(*box3d_psr_1, degrees=False)
    np.testing.assert_almost_equal(box.corners, np.array([
        [1.0,  2.5, -0.9],
        [-1.0, 2.5, -0.9],
        [-1.0, 2.5, 0.9],
        [1.0,  2.5, 0.9],
        [1.0,  -2.5, -0.9],
        [-1.0, -2.5, -0.9],
        [-1.0, -2.5, 0.9],
        [1.0,  -2.5, 0.9],
    ]))


def test_box3d_get_corners2(box3d_psr_2):
    box = Box3d.from_pos_scale_euler(*box3d_psr_2, degrees=False)
    np.testing.assert_almost_equal(box.corners, np.array([
        [5.0,  5.5, -0.95],
        [7.0,  5.5, -0.95],
        [7.0,  5.5, 0.85],
        [5.0,  5.5, 0.85],
        [5.0, 10.5, -0.95],
        [7.0, 10.5, -0.95],
        [7.0, 10.5, 0.85],
        [5.0, 10.5, 0.85],
    ]))
