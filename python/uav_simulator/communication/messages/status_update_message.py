import msgpack

from uav_simulator.communication.messages.message_base import MessageBase
from uav_simulator.communication.messages.message_type_enum import MessageTypeEnum
from uav_simulator.data_types.direction3d import Direction3d
from uav_simulator.data_types.flight_mode_enum import FlightModeEnum
from uav_simulator.data_types.location3d import Location3d
from uav_simulator.data_types.uav_status import UavStatus

class StatusUpdateMessage(MessageBase):
    MESSAGE_TYPE = MessageTypeEnum.STATUS_UPDATE

    def __init__(self):
        super().__init__()
        self.uav_descriptor: str = ''
        self.uav_local_ip = ''
        self.uav_local_port = -1
        self.uav_status: UavStatus = UavStatus()

    def __str__(self):
        return super().__str__()

    def to_buffer(self) -> bytes:
        message_dict = {
            # from base
            'message_id': self.message_id,
            'send_time': self.send_time,
            # from derived
            'uav_descriptor': self.uav_descriptor,
            'uav_local_ip': self.uav_local_ip,
            'uav_local_port': self.uav_local_port,
            'status_location': [self.uav_status.location.x,
                                self.uav_status.location.y,
                                self.uav_status.location.h],
            'status_destination': [self.uav_status.destination.x,
                                   self.uav_status.destination.y,
                                   self.uav_status.destination.h],
            'status_direction': [self.uav_status.direction.azimuth,
                                 self.uav_status.direction.elevation],
            'status_remaining_flight_time': self.uav_status.remaining_flight_time,
            'status_flight_mode': self.uav_status.flight_mode.value}
        return msgpack.dumps(message_dict)

    def from_buffer(self, buffer: bytes):
        message_dict = msgpack.loads(buffer)
        # from base
        self.message_id = message_dict['message_id']
        self.send_time = message_dict['send_time']
        # from derived
        self.uav_descriptor = message_dict['uav_descriptor']
        self.uav_local_ip = message_dict['uav_local_ip']
        self.uav_local_port = message_dict['uav_local_port']
        self.uav_status.location = Location3d(message_dict['status_location'][0],
                                              message_dict['status_location'][1],
                                              message_dict['status_location'][2])
        self.uav_status.destination = Location3d(message_dict['status_destination'][0],
                                                 message_dict['status_destination'][1],
                                                 message_dict['status_destination'][2])
        self.uav_status.direction = Direction3d(message_dict['status_direction'][0],
                                                message_dict['status_direction'][1])
        self.uav_status.remaining_flight_time = message_dict['status_remaining_flight_time']
        self.uav_status.flight_mode = FlightModeEnum(message_dict['status_flight_mode'])

if __name__ == '__main__':
    s1 = StatusUpdateMessage()
    s1.uav_local_ip = '22.22.22.22'
    s1.uav_local_port = 4444
    s1.send_time = 12345678.1234
    s1.uav_descriptor = 'uav01'
    s1.uav_status.location = Location3d(1, 2, 3)
    s1.uav_status.direction = Direction3d(4, 5)
    s1.uav_status.destination = Location3d(7, 8, 9)
    s1.uav_status.flight_mode = FlightModeEnum.TO_DESTINATION
    s1.uav_status.remaining_flight_time = 17.45
    b1 = s1.to_buffer()

    s2 = StatusUpdateMessage()
    s2.from_buffer(b1)

    assert s1.uav_status.flight_mode == s2.uav_status.flight_mode
    assert s1.uav_status.location.y == s2.uav_status.location.y
    assert s1.uav_local_ip == s2.uav_local_ip
