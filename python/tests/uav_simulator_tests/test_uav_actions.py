import math
import unittest

from python.uav_simulator.data_types.direction3d import Direction3d
from python.uav_simulator.data_types.location3d import Location3d
from python.uav_simulator.logic.simple_uav_actions import SimpleUavActions

class TestUavActions(unittest.TestCase):

    def test_move(self):
        cos45 = math.cos(math.pi / 4)
        # move 1 second, azimuth=0 deg
        location = SimpleUavActions.calculate_new_location(Location3d(0.0, 0.0, 0.0), Direction3d(0.0, 0.0), 1.0, 1.0)
        self.assertAlmostEqual(location.x, 1, 2)
        # move 1 second, azimuth=90 deg
        location = SimpleUavActions.calculate_new_location(Location3d(0.0, 0.0, 0.0), Direction3d(math.pi / 2, 0.0), 1.0, 1.0)
        self.assertAlmostEqual(location.y, 1, 2)
        # move 1 second, elevation=45 deg
        location = SimpleUavActions.calculate_new_location(Location3d(0.0, 0.0, 0.0), Direction3d(0.0, math.pi / 4), 1.0, 1.0)
        self.assertAlmostEqual(location.x, cos45, 2)
        self.assertAlmostEqual(location.h, cos45, 2)
        # move 1 second, azimuth=45 deg,elevation=45 deg
        location = SimpleUavActions.calculate_new_location(Location3d(0.0, 0.0, 0.0), Direction3d(math.pi / 4, math.pi / 4), 1.0,
                                                           1.0)
        self.assertAlmostEqual(location.x, 0.5, 2)
        self.assertAlmostEqual(location.y, 0.5, 2)
        self.assertAlmostEqual(location.h, cos45, 2)
        # move 1 second, azimuth=90 deg,elevation=45 deg
        location = SimpleUavActions.calculate_new_location(Location3d(0.0, 0.0, 0.0), Direction3d(math.pi / 2, math.pi / 4), 1.0,
                                                           1.0)
        self.assertAlmostEqual(location.x, 0, 2)
        self.assertAlmostEqual(location.y, cos45, 2)
        self.assertAlmostEqual(location.h, cos45, 2)
        # move 1 second, azimuth=90 deg,elevation=90 deg
        location = SimpleUavActions.calculate_new_location(Location3d(0.0, 0.0, 0.0), Direction3d(math.pi / 2, math.pi / 2), 1.0,
                                                           1.0)
        self.assertAlmostEqual(location.x, 0, 2)
        self.assertAlmostEqual(location.y, 0, 2)
        self.assertAlmostEqual(location.h, 1, 2)

    def test_calculate_direction_to(self):
        # to 100,100
        direction = SimpleUavActions.calculate_Direction(Location3d(0, 0, 0), Location3d(100, 100, 0))
        self.assertAlmostEqual(direction.azimuth_degree, 45, 2)
        # to -100,-100
        direction = SimpleUavActions.calculate_Direction(Location3d(0, 0, 0), Location3d(-100, -100, 0))
        self.assertAlmostEqual(direction.azimuth_degree, -135, 2)
        # to 0,0,100
        direction = SimpleUavActions.calculate_Direction(Location3d(0, 0, 0), Location3d(0, 0, 100))
        self.assertAlmostEqual(direction.elevation_degree, 90, 2)
        # to 100,0,100
        direction = SimpleUavActions.calculate_Direction(Location3d(0, 0, 0), Location3d(100, 0, 100))
        self.assertAlmostEqual(direction.elevation_degree, 45, 2)
        # to 100,100, diagonal
        direction = SimpleUavActions.calculate_Direction(Location3d(0, 0, 0),
                                                         Location3d(100, 100, math.sqrt(100 ** 2 + 100 ** 2)))
        self.assertAlmostEqual(direction.elevation_degree, 45, 2)
        # to 100,100,100
        direction = SimpleUavActions.calculate_Direction(Location3d(0, 0, 0), Location3d(100, 100, 100))
        self.assertAlmostEqual(direction.elevation_degree, 35.26, 2)

    def test_distance(self):
        # distance to 100,0,0
        distance = SimpleUavActions.calculate_distance(Location3d(0, 0, 0), Location3d(100, 0, 0))
        self.assertAlmostEqual(distance, 100, 2)
        # distance to 100,100
        distance = SimpleUavActions.calculate_distance(Location3d(0, 0, 0), Location3d(100, 100, 0))
        self.assertAlmostEqual(distance, 141.42, 2)
        # distance to 100,100,100
        distance = SimpleUavActions.calculate_distance(Location3d(0, 0, 0), Location3d(100, 100, 100))
        self.assertAlmostEqual(distance, 173.205, 2)
