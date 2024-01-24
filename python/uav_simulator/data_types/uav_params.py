import json

from common.utils.printable_params import PrintableParams

class UavParams:
    """UAV configuration values
        Attributes:
            in_location_distance (float): when is considered that uav reached destination
            status_update_interval (float): status message sending interval
            capabilities_update_interval (float): capabilities update message sending interval
    """

    @staticmethod
    def from_json_config_file(json_config: str):
        with open(file=json_config, mode='r') as file:
            data_dict = json.load(file)
            return UavParams(data_dict)

    def __init__(self, uav_config: dict):
        self.uav_descriptor = uav_config['uav_descriptor']
        self.max_flight_time = uav_config['max_flight_time']
        self.flight_velocity = uav_config['flight_velocity']
        self.status_update_interval = uav_config['status_update_interval']
        self.capabilities_update_interval = uav_config['capabilities_update_interval']
        self.in_location_distance = uav_config['in_location_distance']
        # communication
        self.uav_ip = uav_config['local_ip']
        self.uav_port = uav_config['local_port']
        self.ground_control_ip = uav_config['ground_control_ip']
        self.ground_control_port = uav_config['ground_control_port']

    def __str__(self):
        return PrintableParams.to_string(self, True)

if __name__ == '__main__':
    config = {'uav_descriptor': 'UAV01',
              'max_flight_time': 60 * 5,
              'flight_velocity': 10.0,
              'status_update_interval': 2,
              'capabilities_update_interval': 5,
              'in_location_distance': 10.0,
              'local_ip': '127.0.0.1',
              'local_port': 2001,
              'ground_control_ip': '127.0.0.1',
              'ground_control_port': 1000}
    params = UavParams(config)
    print(params)
