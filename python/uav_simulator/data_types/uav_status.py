from typing import Optional

from uav_simulator.data_types.direction3d import Direction3d
from uav_simulator.data_types.flight_mode_enum import FlightModeEnum
from uav_simulator.data_types.location3d import Location3d

class UavStatus:
    """UAV current state parameters"""

    def __init__(self):
        self.location: Optional[Location3d] = None
        self.destination: Optional[Location3d] = None
        self.direction: Optional[Direction3d] = None
        self.remaining_flight_time = 0
        self.flight_mode = FlightModeEnum.IDLE

    def __str__(self):
        return f'(UavStatus: location:{self.location} remaining:{self.remaining_flight_time} {self.flight_mode})'
