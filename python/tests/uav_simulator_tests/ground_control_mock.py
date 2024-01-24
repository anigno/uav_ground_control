import logging
import time

from python.common.logging_provider.logging_initiator_by_code import LoggingInitiatorByCode
from python.uav_simulator.communication.ground_control_communicator import GroundControlCommunicator
from python.uav_simulator.communication.messages.capabilities_update_message import CapabilitiesUpdateMessage
from python.uav_simulator.communication.messages.status_update_message import StatusUpdateMessage
from python.uav_simulator.communication.messages_factory_base import MessagesFactoryBase
from python.uav_simulator.communication.uav_message_factory import UavSimulatorMessageFactory
from python.uav_simulator.data_types.flight_mode_enum import FlightModeEnum
from python.uav_simulator.data_types.location3d import Location3d

class GroundControlMock:
    """simulate a ground control"""

    def __init__(self, logger: logging.Logger, message_factory: MessagesFactoryBase, local_ip, local_port):
        self.last_uav_descriptor = None
        self.logger = logger
        self.communicator = GroundControlCommunicator(logger, message_factory, local_ip, local_port)
        self.communicator.on_uav_status_updated += self.on_oav_status_updated
        self.communicator.on_capabilities_updated += self.on_capabilities_updated
        self.home_location = Location3d(0, 0, 0)

    def start(self):
        self.communicator.start()

    def send_fly_to(self, uav_descriptor: str, destination: Location3d, flight_mode: FlightModeEnum):
        self.communicator.send_fly_to_destination(uav_descriptor, destination, flight_mode)

    def on_oav_status_updated(self, message: StatusUpdateMessage):
        self.logger.debug(f'{message}')
        self.last_uav_descriptor = message.uav_descriptor

    def on_capabilities_updated(self, message: CapabilitiesUpdateMessage):
        self.logger.debug(f'{message}')

if __name__ == '__main__':
    main_logger = logging.getLogger(LoggingInitiatorByCode.FILE_SYSTEM_LOGGER)
    LoggingInitiatorByCode(log_files_path=r'd:\temp\logs\gc')
    main_logger.info(f'starting')
    main_message_factory = UavSimulatorMessageFactory(main_logger)
    gcm = GroundControlMock(main_logger, main_message_factory, 'localhost', 1001)
    gcm.start()
    time.sleep(10)
    if gcm.last_uav_descriptor is not None:
        gcm.send_fly_to('UAV01', Location3d(100, 100, 10), FlightModeEnum.TO_DESTINATION)
    time.sleep(12)
    if gcm.last_uav_descriptor is not None:
        gcm.send_fly_to('UAV01', Location3d(100, 100, 100), FlightModeEnum.TO_DESTINATION)
    time.sleep(12)
    if gcm.last_uav_descriptor is not None:
        gcm.send_fly_to('UAV01', Location3d(0, 0, 0), FlightModeEnum.TO_DESTINATION)

    input('enter to exit')
