import time
from abc import ABC
from threading import RLock
import msgpack

from common.utils.printable_params import PrintableParams
from uav_simulator.communication.messages.message_type_enum import MessageTypeEnum

class MessageBase(ABC):
    """base class for messages, uses msgpack serialization"""
    MESSAGE_TYPE = MessageTypeEnum.BASE
    _message_id_counter = 1000
    _locker = RLock()

    def __init__(self):
        self.send_time = -1
        self.message_id = -1
        with MessageBase._locker:
            self.message_id = MessageBase._message_id_counter
            MessageBase._message_id_counter += 1

    def to_buffer(self) -> bytes:
        return msgpack.dumps(self.__dict__)

    def from_buffer(self, buffer: bytes):
        self.__dict__ = msgpack.loads(buffer)

    def __str__(self):
        return f'[{type(self)}: {self.message_id} {self.send_time}]\n'

if __name__ == '__main__':
    class Message1(MessageBase):
        MESSAGE_TYPE = 2222

        def __init__(self):
            super().__init__()
            self.name = 'abc'
            self.data = [1, 2, 3]

    Message1()
    Message1()
    m1 = Message1()
    m1.send_time = time.time()
    PrintableParams.print(m1, True)
    buffer1 = m1.to_buffer()

    m2 = Message1()
    m2.from_buffer(buffer1)
    PrintableParams.print(m2, True)

    assert m1.message_id == m2.message_id
    assert m1.name == m2.name
