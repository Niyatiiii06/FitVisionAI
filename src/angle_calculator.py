import numpy as np


class AngleCalculator:

    @staticmethod
    def calculate_angle(point1, point2, point3):

        point1 = np.array(point1)
        point2 = np.array(point2)
        point3 = np.array(point3)

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

        angle = abs(angle)

        if angle > 180:
            angle = 360 - angle

        return angle