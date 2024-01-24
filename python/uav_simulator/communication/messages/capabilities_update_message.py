from typing import List
import msgpack

from uav_simulator.capabilities.capability_data import CapabilityData
from uav_simulator.communication.messages.message_base import MessageBase
from uav_simulator.communication.messages.message_type_enum import MessageTypeEnum

class CapabilitiesUpdateMessage(MessageBase):
    MESSAGE_TYPE = MessageTypeEnum.CAPABILITIES_UPDATE

    def __init__(self):
        super().__init__()
        self.uav_descriptor: str = ''
        self.capabilities: List[CapabilityData] = []

    def __str__(self):
        return super().__str__()

    def to_buffer(self) -> bytes:
        message_dict = {
            # from base
            'message_id': self.message_id,
            'send_time': self.send_time,
            # from derived
            'uav_descriptor': self.uav_descriptor,
            'capabilities': []
        }
        for capability_data in self.capabilities:
            message_dict['capabilities'].append([capability_data.descriptor, capability_data.capability_bytes])
        return msgpack.dumps(message_dict)

    def from_buffer(self, buffer: bytes):
        message_dict = msgpack.loads(buffer)
        # from base
        self.message_id = message_dict['message_id']
        self.send_time = message_dict['send_time']
        # from derived
        self.uav_descriptor = message_dict['uav_descriptor']
        for capability in message_dict['capabilities']:
            self.capabilities.append(CapabilityData(capability[0], capability[1]))

if __name__ == '__main__':
    c1 = CapabilitiesUpdateMessage()
    c1.send_time = 12345.678
    c1.uav_descriptor = 'uav02'
    c1.capabilities = [CapabilityData('Camera01', b'12345678'),
                       CapabilityData('IR01', b'abcdefg')]
    b1 = c1.to_buffer()

    c2 = CapabilitiesUpdateMessage()
    c2.from_buffer(b1)
    assert c1.capabilities[0].descriptor == c2.capabilities[0].descriptor
    assert c1.capabilities[1].capability_bytes == c2.capabilities[1].capability_bytes
