import math

class Direction3d:
    def __init__(self, azimuth=0.0, elevation=0.0):
        self.azimuth = azimuth
        self.elevation = elevation

    def copy(self):
        """generate a copy of this instance"""
        return Direction3d(self.azimuth, self.elevation)

    @property
    def azimuth_degree(self):
        return math.degrees(self.azimuth)

    @property
    def elevation_degree(self):
        return math.degrees(self.elevation)

    def __str__(self):
        return f'(az={math.degrees(self.azimuth):.3f},el={math.degrees(self.elevation):.3f})'
