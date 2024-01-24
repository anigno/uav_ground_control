from logging import Logger
from typing import List

from python.common.utils.generic_event import GenericEvent
from python.uav_simulator.capabilities.capability_data import CapabilityData
from python.uav_simulator.communication.messages.capabilities_update_message import CapabilitiesUpdateMessage
from python.uav_simulator.communication.messages.fly_to_destination_message import FlyToDestinationMessage
from python.uav_simulator.communication.messages.message_base import MessageBase
from python.uav_simulator.communication.messages.message_type_enum import MessageTypeEnum
from python.uav_simulator.communication.messages.status_update_message import StatusUpdateMessage
from python.uav_simulator.communication.messages_factory_base import MessagesFactoryBase
from python.uav_simulator.communication.specialized_communicator_base import SpecializedCommunicatorBase
from python.uav_simulator.data_types.uav_status import UavStatus

class UavCommunicator(SpecializedCommunicatorBase):
    """handle receiving GC messages and send status messages to GC"""
    def __init__(self, logger: Logger, messages_factory: MessagesFactoryBase, uav_descriptor, uav_ip, uav_port, gc_ip,
                 gc_port):
        super().__init__(logger, messages_factory, uav_ip, uav_port)
        self.on_fly_to_destination = GenericEvent(FlyToDestinationMessage)
        self.gc_ip = gc_ip
        self.gc_port = gc_port
        self.uav_descriptor = uav_descriptor

    def send_uav_status_update(self, uav_status: UavStatus):
        message = StatusUpdateMessage()
        message.uav_descriptor = self.uav_descriptor
        message.uav_local_ip = self.communicator.local_ip
        message.uav_local_port = self.communicator.local_port
        message.uav_status = uav_status
        self.communicator.send_message(message, self.gc_ip, self.gc_port)

    def send_uav_capabilities(self, capabilities: List[CapabilityData]):
        message = CapabilitiesUpdateMessage()
        message.uav_descriptor = self.uav_descriptor
        message.capabilities = capabilities
        self.communicator.send_message(message, self.gc_ip, self.gc_port)

    def _on_message_received(self, message: MessageBase):
        if message.MESSAGE_TYPE == MessageTypeEnum.FLY_TO_DESTINATION:
            self.on_fly_to_destination.raise_event(message)
