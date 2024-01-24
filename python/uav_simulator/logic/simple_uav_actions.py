import math

from python.uav_simulator.data_types.direction3d import Direction3d
from python.uav_simulator.data_types.location3d import Location3d

class SimpleUavActions:
    """flying UAV calculations"""
    RANDOMIZE_FACTOR = 0.1

    @staticmethod
    def calculate_new_location(location: Location3d, direction: Direction3d, velocity: float, interval: float) -> Location3d:
        new_location = Location3d()
        new_location.x = location.x + math.cos(direction.azimuth) * math.cos(
            direction.elevation) * velocity * interval
        new_location.y = location.y + math.sin(direction.azimuth) * math.cos(
            direction.elevation) * velocity * interval
        new_location.h = location.h + math.sin(direction.elevation) * velocity * interval
        return new_location

    @staticmethod
    def calculate_Direction(origin: Location3d, destination: Location3d) -> Direction3d:
        delta_x = destination.x - origin.x
        delta_y = destination.y - origin.y
        delta_z = destination.h - origin.h
        azimuth = math.atan2(delta_y, delta_x)
        horizontal_distance = math.sqrt(delta_x ** 2 + delta_y ** 2)
        elevation = math.atan2(delta_z, horizontal_distance)
        return Direction3d(azimuth, elevation)

    @staticmethod
    def calculate_distance(origin: Location3d, location: Location3d) -> float:
        distance = math.sqrt((location.x - origin.x) ** 2 + (location.y - origin.y) ** 2 + (
                location.h - origin.h) ** 2)
        return distance
