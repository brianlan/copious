import math

import pytest
import numpy as np

from copious.cv.geometry import points3d_to_homo, Box3d, xyzq2mat


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


def test_xyzq2mat_homogeneous_matrix_shape():
    # Test when as_homo is True
    homo_matrix = xyzq2mat(1, 2, 3, 0, 0, 0, 1, True)
    assert homo_matrix.shape == (4, 4), "Homogeneous matrix should be 4x4"

def test_xyzq2mat_non_homogeneous_matrix_shape():
    # Test when as_homo is False
    non_homo_matrix = xyzq2mat(1, 2, 3, 0, 0, 0, 1, False)
    assert non_homo_matrix.shape == (3, 4), "Non-homogeneous matrix should be 3x4"

def test_xyzq2mat_default_as_homo():
    # Test when as_homo is not provided (should default to False)
    default_matrix = xyzq2mat(1, 2, 3, 0, 0, 0, 1)
    assert default_matrix.shape == (3, 4), "Default matrix should be 3x4 when as_homo is not provided"

def test_xyzq2mat_translation_components():
    # Check if the translation components are set correctly for both cases
    homo_matrix = xyzq2mat(1, 2, 3, 0, 0, 0, 1, True)
    non_homo_matrix = xyzq2mat(1, 2, 3, 0, 0, 0, 1, False)
    np.testing.assert_array_equal(homo_matrix[:3, 3], [1, 2, 3])
    np.testing.assert_array_equal(non_homo_matrix[:, 3], [1, 2, 3])

def test_xyzq2mat_rotation_matrix_validity():
    # Identity quaternion should produce an identity rotation matrix for both cases
    homo_matrix = xyzq2mat(0, 0, 0, 0, 0, 0, 1, True)
    non_homo_matrix = xyzq2mat(0, 0, 0, 0, 0, 0, 1, False)
    expected_rotation = np.eye(3)
    np.testing.assert_array_almost_equal(homo_matrix[:3, :3], expected_rotation)
    np.testing.assert_array_almost_equal(non_homo_matrix[:3, :3], expected_rotation)



def test_xyzq2mat_matrix_shape():
    # Test both homogeneous and non-homogeneous output shapes
    homo_matrix = xyzq2mat(1, 2, 3, 0, 0, 0, 1, True)
    non_homo_matrix = xyzq2mat(1, 2, 3, 0, 0, 0, 1, False)
    assert homo_matrix.shape == (4, 4), "Homogeneous matrix should be 4x4"
    assert non_homo_matrix.shape == (3, 4), "Non-homogeneous matrix should be 3x4"


def test_xyzq2mat_identity_quaternion():
    # Identity quaternion with zero translation
    matrix = xyzq2mat(0, 0, 0, 0, 0, 0, 1, True)
    expected_matrix = np.eye(4)
    np.testing.assert_array_almost_equal(matrix, expected_matrix)

def test_xyzq2mat_non_identity_quaternion():
    # Non-identity quaternion (90 degrees rotation around z-axis)
    matrix = xyzq2mat(0, 0, 0, 0, 0, np.sqrt(0.5), np.sqrt(0.5), False)
    expected_rotation = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
    np.testing.assert_array_almost_equal(matrix[:3, :3], expected_rotation)

def test_xyzq2mat_zero_translation():
    # Zero translation with an identity quaternion
    matrix = xyzq2mat(0, 0, 0, 0, 0, 0, 1, False)
    expected_matrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]])
    np.testing.assert_array_almost_equal(matrix, expected_matrix)