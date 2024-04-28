from typing import List, Union

from scipy.interpolate import splprep, splev
import numpy as np


def lerp(p1: Union[list,np.array], p2: Union[list,np.array], u: Union[list,np.array]) -> np.ndarray:
    """
    Linear interpolation between two points.
    
    Args:
        p1 (Sequence): First 3D point in the form (x1, y1, z1) 
        p2 (Sequence): Second 3D point in the form (x2, y2, z2)
        t (Sequence): Interpolation parameter in the range [0, 1] 
        
    Returns:
        tuple: Interpolated list of points
    """
    assert len(p1) == len(p2)
    n_dimensions = len(p1)
    res = np.zeros((len(u), n_dimensions), dtype=np.float32)
    if not isinstance(u, np.ndarray):
        u = np.array(u)
    for d in range(n_dimensions):
       res[:, d] = (1 - u) * p1[d] + u * p2[d]

    return res


class SplineInterpolator:
    def __init__(self, data: List[Union[list, np.ndarray]], k: int = 3, s: float = 0) -> None:
        """_summary_

        Parameters
        ----------
        data : List[Union[list, np.ndarray]]
            If passed np.ndarray, the shape of it should be (3, N);
        k : int, optional
            _description_, by default 3
        s : float, optional
            _description_, by default 0
        """
        if not isinstance(data[0], list) and not isinstance(data[0], np.ndarray):
            data = [data]
        self.tck, u = splprep(data, s=0, k=k)

    def interpolate(self, u: Union[np.ndarray, list]) -> List[list]:
        return splev(u, self.tck)


def calc_polyline_length(points: np.ndarray):
    # Convert list of points to numpy array
    if not isinstance(points, np.ndarray):
        points = np.array(points)
    
    # Calculate the differences between each point
    diffs = points[1:] - points[:-1]
    
    # Calculate the distances between each point using the L2 norm
    distances = np.linalg.norm(diffs, axis=1)
    
    # Sum up all the distances
    total_distance = np.sum(distances)
    
    return total_distance


__all__ = ["lerp", "SplineInterpolator", "calc_polyline_length"]
