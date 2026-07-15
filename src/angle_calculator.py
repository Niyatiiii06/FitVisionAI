import numpy as np


class AngleCalculator:
    """
    Utility class for calculating joint angles.

    The angle is calculated at point2.

    Example:
        Hip ------ Knee ------ Ankle

        calculate_angle(
            hip,
            knee,
            ankle
        )

        Returns the knee angle.
    """

    @staticmethod
    def calculate_angle(point1, point2, point3):
        """
        Calculate the angle (in degrees) formed by three points.

        Parameters
        ----------
        point1 : list | tuple | np.ndarray
            First point (x, y) or (x, y, z, ...)
        point2 : list | tuple | np.ndarray
            Middle point (joint where angle is measured)
        point3 : list | tuple | np.ndarray
            Third point (x, y) or (x, y, z, ...)

        Returns
        -------
        float
            Angle between 0 and 180 degrees.
        """

        # Use only x and y coordinates
        point1 = np.array(point1[:2], dtype=np.float32)
        point2 = np.array(point2[:2], dtype=np.float32)
        point3 = np.array(point3[:2], dtype=np.float32)

        # Calculate angle
        angle = np.degrees(
            np.arctan2(
                point3[1] - point2[1],
                point3[0] - point2[0]
            )
            -
            np.arctan2(
                point1[1] - point2[1],
                point1[0] - point2[0]
            )
        )

        # Convert to positive angle
        angle = abs(angle)

        # Ensure angle is between 0° and 180°
        if angle > 180:
            angle = 360 - angle

        return angle