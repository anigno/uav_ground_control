from python.uav_simulator.communication.messages.capabilities_update_message import CapabilitiesUpdateMessage
from python.uav_simulator.communication.messages.fly_to_destination_message import FlyToDestinationMessage
from python.uav_simulator.communication.messages.status_update_message import StatusUpdateMessage
from python.uav_simulator.communication.messages_factory_base import MessagesFactoryBase

class UavSimulatorMessageFactory(MessagesFactoryBase):
    """specific UAV simulator messages factory"""

    def __init__(self, logger):
        super().__init__(logger)

    def init_messages(self):
        self.register_message(CapabilitiesUpdateMessage)
        self.register_message(FlyToDestinationMessage)
        self.register_message(StatusUpdateMessage)
