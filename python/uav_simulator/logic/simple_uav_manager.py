import logging
import time
from threading import Thread, RLock
from typing import Optional, List

from common.utils.printable_params import PrintableParams
from uav_simulator.capabilities.capability_base import CapabilityBase
from uav_simulator.communication.messages.fly_to_destination_message import FlyToDestinationMessage
from uav_simulator.communication.uav_communicator import UavCommunicator
from uav_simulator.data_types.direction3d import Direction3d
from uav_simulator.data_types.flight_mode_enum import FlightModeEnum
from uav_simulator.data_types.location3d import Location3d
from uav_simulator.data_types.uav_params import UavParams
from uav_simulator.data_types.uav_status import UavStatus
from uav_simulator.logic.simple_uav_actions import SimpleUavActions

class SimpleUavManager:
    """manage the Uav operations and messaging
        Attributes:
            uav_params (UavParams): uav configuration params
            uav_status (UavStatus): uav updated location, direction etc.
    """
    LOCATION_CALCULATION_INTERVAL = 0.1

    def __init__(self, logger: logging.Logger, uav_params: UavParams, home_location: Location3d, capabilities: List[CapabilityBase],
                 communicator: UavCommunicator):
        self.logger = logger
        self.logger.info(f'\n{uav_params}\n')
        self.uav_params = uav_params
        self.uav_status = UavStatus()
        self.home_location = home_location.copy()
        self.uav_status.location = home_location.copy()
        self.uav_status.destination = home_location.copy()
        self.uav_status.direction = Direction3d(0, 0)
        self.status_locker = RLock()
        self._status_update_thread: Optional[Thread] = None
        self._capabilities_update_thread: Optional[Thread] = None
        self._is_update_thread_run = False
        self.capabilities = capabilities
        self.communicator = communicator
        self.communicator.on_fly_to_destination += self._on_fly_to_destination_received

    def start(self):
        with self.status_locker:
            if self._is_update_thread_run:
                raise Exception('update thread is already running')
            self._is_update_thread_run = True
        self.reset_flight_time()
        self._status_update_thread = Thread(name='update', target=self._status_update_thread_start, daemon=True)
        self._status_update_thread.start()
        self._capabilities_update_thread = Thread(name='capabilities', target=self._capabilities_thread_start,
                                                  daemon=True)
        self._capabilities_update_thread.start()
        self.communicator.start()

    def stop(self):
        with self.status_locker:
            self._is_update_thread_run = False

    def set_destination(self, destination: Location3d):
        with self.status_locker:
            self.uav_status.destination = destination.copy()

    def set_state(self, flight_mode: FlightModeEnum):
        with self.status_locker:
            self.uav_status.flight_mode = flight_mode

    def reset_flight_time(self):
        """reset remaining flight time to full (battery charged)"""
        with self.status_locker:
            self.uav_status.remaining_flight_time = self.uav_params.max_flight_time

    def __str__(self):
        return PrintableParams.to_string(self, True)

    def _status_update_thread_start(self):
        previous_update_time = time.time()
        update_message_snd_time_counter = 0
        while self._is_update_thread_run:
            time.sleep(SimpleUavManager.LOCATION_CALCULATION_INTERVAL)
            new_update_time = time.time()
            delta_time = new_update_time - previous_update_time
            previous_update_time = new_update_time
            update_message_snd_time_counter += delta_time
            with self.status_locker:
                if not self.uav_status.flight_mode == FlightModeEnum.IDLE:
                    # update uav status
                    self.uav_status.direction = SimpleUavActions.calculate_Direction(self.uav_status.location,
                                                                                     self.uav_status.destination)
                    distance = SimpleUavActions.calculate_distance(self.uav_status.location,
                                                                   self.uav_status.destination)
                    if distance > self.uav_params.in_location_distance:
                        self.uav_status.location = SimpleUavActions.calculate_new_location(
                            self.uav_status.location,
                            self.uav_status.direction,
                            self.uav_params.flight_velocity,
                            delta_time)
                    else:
                        self.uav_status.flight_mode = FlightModeEnum.IN_DESTINATION
                    self.uav_status.remaining_flight_time -= delta_time
                # check for update message sending need
                if update_message_snd_time_counter >= self.uav_params.status_update_interval:
                    update_message_snd_time_counter = 0
                    self.communicator.send_uav_status_update(self.uav_status)
                    self.logger.debug(f'{self.uav_params.uav_descriptor} {self.uav_status}')

    def _capabilities_thread_start(self):
        while self._is_update_thread_run:
            time.sleep(self.uav_params.capabilities_update_interval)
            capabilities_data_list = [c.get(self.uav_status) for c in self.capabilities]
            self.communicator.send_uav_capabilities(capabilities_data_list)

    def _on_fly_to_destination_received(self, message: FlyToDestinationMessage):
        self.logger.debug(f'{message.destination} {message.destination_flight_mode}')
        self.set_destination(message.destination)
        self.set_state(message.destination_flight_mode)
