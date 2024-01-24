import msgpack

from python.uav_simulator.communication.messages.message_base import MessageBase
from python.uav_simulator.communication.messages.message_type_enum import MessageTypeEnum
from python.uav_simulator.data_types.flight_mode_enum import FlightModeEnum
from python.uav_simulator.data_types.location3d import Location3d

class FlyToDestinationMessage(MessageBase):
    MESSAGE_TYPE = MessageTypeEnum.FLY_TO_DESTINATION

    def __init__(self):
        super().__init__()
        self.destination_flight_mode: FlightModeEnum = FlightModeEnum.IDLE
        self.destination: Location3d = Location3d()

    def __str__(self):
        return super().__str__()

    def to_buffer(self) -> bytes:
        message_dict = {
            # from base
            'message_id': self.message_id,
            'send_time': self.send_time,
            # from derived
            'destination_flight_mode': self.destination_flight_mode.value,
            'destination': [self.destination.x,
                            self.destination.y,
                            self.destination.h]
        }
        return msgpack.dumps(message_dict)

    def from_buffer(self, buffer: bytes):
        message_dict = msgpack.loads(buffer)
        # from base
        self.message_id = message_dict['message_id']
        self.send_time = message_dict['send_time']
        # from derived
        self.destination_flight_mode = FlightModeEnum(message_dict['destination_flight_mode'])
        self.destination = Location3d(message_dict['destination'][0],
                                      message_dict['destination'][1],
                                      message_dict['destination'][2])

if __name__ == '__main__':
    f1 = FlyToDestinationMessage()
    f1.send_time = 1234.567
    f1.destination_flight_mode = FlightModeEnum.TO_DESTINATION
    f1.destination = Location3d(1, 2, 3)
    b1 = f1.to_buffer()

    f2 = FlyToDestinationMessage()
    f2.from_buffer(b1)

    assert f1.destination_flight_mode == f2.destination_flight_mode
    assert f1.destination.h == f2.destination.h
