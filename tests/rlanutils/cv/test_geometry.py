import numpy as np

from rlanutils.cv.geometry import points3d_to_homo


def test_to_homo():
    np.testing.assert_almost_equal(
        points3d_to_homo(
            np.array([[0, 2, 3], [0.1, -0.2, 0.3]])
        ),
        np.array([[0, 2, 3, 1], [0.1, -0.2, 0.3, 1]])
    )
