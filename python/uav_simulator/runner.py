import argparse
import logging
from typing import List

from common.logging_provider.logging_initiator_by_code import LoggingInitiatorByCode
from data_types.uav_params import UavParams
from uav_simulator.capabilities.capability_base import CapabilityBase
from uav_simulator.communication.uav_communicator import UavCommunicator
from uav_simulator.communication.uav_message_factory import UavSimulatorMessageFactory
from uav_simulator.data_types.location3d import Location3d
from uav_simulator.logic.simple_uav_manager import SimpleUavManager

class Runner:
    def __init__(self, logger: logging.Logger, config_file: str, location_string: str,
                 capabilities: List[CapabilityBase]):
        """main UAV simulator runner"""
        uav_params = UavParams.from_json_config_file(config_file)
        # convert string 'x,y,h' to three floats x,y,h
        location_float_params = [float(b) for b in [a for a in location_string.split(',')]]
        home_location = Location3d(*location_float_params)
        capabilities = capabilities
        messages_factory = UavSimulatorMessageFactory(logger)
        communicator = UavCommunicator(logger, messages_factory, uav_params.uav_descriptor, uav_params.uav_ip,
                                       uav_params.uav_port, uav_params.ground_control_ip,
                                       uav_params.ground_control_port, )
        self.uav_manager = SimpleUavManager(logger, uav_params, home_location, capabilities, communicator)

    def start(self):
        self.uav_manager.start()

if __name__ == '__main__':
    app_logger = logging.getLogger(LoggingInitiatorByCode.FILE_SYSTEM_LOGGER)
    LoggingInitiatorByCode(log_files_path=r'd:\temp\logs\uav1')

    # parse commandline args
    parser = argparse.ArgumentParser(description='UAV simulation runner')
    parser.add_argument('--config', type=str, required=True, help='json uav params config file')
    parser.add_argument('--home', type=str, required=True, help='location of home (x,y,h)')
    args = parser.parse_args()

    external_capabilities = []
    runner = Runner(app_logger, args.config, args.home, external_capabilities)
    runner.start()

    input('Enter to exit')
