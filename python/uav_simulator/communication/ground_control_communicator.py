from logging import Logger
from typing import Dict, Tuple

from common.utils.generic_event import GenericEvent
from uav_simulator.communication.messages.capabilities_update_message import CapabilitiesUpdateMessage
from uav_simulator.communication.messages.fly_to_destination_message import FlyToDestinationMessage
from uav_simulator.communication.messages.message_base import MessageBase
from uav_simulator.communication.messages.message_type_enum import MessageTypeEnum
from uav_simulator.communication.messages.status_update_message import StatusUpdateMessage
from uav_simulator.communication.messages_factory_base import MessagesFactoryBase
from uav_simulator.communication.specialized_communicator_base import SpecializedCommunicatorBase
from uav_simulator.data_types.flight_mode_enum import FlightModeEnum
from uav_simulator.data_types.location3d import Location3d

class GroundControlCommunicator(SpecializedCommunicatorBase):
    """handle receiving UAVs messages and send flight missions to UAVs, manage uav addressbook"""

    def __init__(self, logger: Logger, messages_factory: MessagesFactoryBase, local_ip, local_port):
        super().__init__(logger, messages_factory, local_ip, local_port)
        self.on_uav_status_updated = GenericEvent(StatusUpdateMessage)
        self.on_capabilities_updated = GenericEvent(CapabilitiesUpdateMessage)
        self.uav_addressbook_dict: Dict[str, Tuple[str, int]] = {}

    def send_fly_to_destination(self, uav_descriptor: str, destination: Location3d, flight_mode: FlightModeEnum):
        message = FlyToDestinationMessage()
        message.destination = destination.copy()
        message.destination_flight_mode = flight_mode
        ip_endpoint = self.uav_addressbook_dict[uav_descriptor]
        self.communicator.send_message(message, *ip_endpoint)

    def _on_message_received(self, message: MessageBase):
        if message.MESSAGE_TYPE == MessageTypeEnum.STATUS_UPDATE:
            message: StatusUpdateMessage
            # update addressbook with uav ip and port
            self.uav_addressbook_dict[message.uav_descriptor] = (message.uav_local_ip, message.uav_local_port)
            self.on_uav_status_updated.raise_event(message)
        elif message.MESSAGE_TYPE == MessageTypeEnum.CAPABILITIES_UPDATE:
            self.on_capabilities_updated.raise_event(message)

if __name__ == '__main__':
    def func(a, b, c):
        print(a, b, c)

    d = (1, 2, 3)
    func(*d)
