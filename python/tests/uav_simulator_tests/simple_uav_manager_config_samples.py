class SimpleUavManagerConfigSamples:
    ground_control_ip = '127.0.0.1'
    ground_control_port = 1000
    config_list = [
        {'name': 'UAV01',
         'max_flight_time': 60 * 2,
         'flight_velocity': 10.0,
         'update_interval': 5,
         'in_location_distance': 10.0,
         'local_ip': '127.0.0.1',
         'local_port': 2001,
         'ground_control_ip': ground_control_ip,
         'ground_control_port': ground_control_port},
        {'name': 'UAV02',
         'max_flight_time': 60 * 5,
         'flight_velocity': 8.0,
         'update_interval': 5,
         'in_location_distance': 10.0,
         'local_ip': '127.0.0.1',
         'local_port': 2002,
         'ground_control_ip': ground_control_ip,
         'ground_control_port': ground_control_port}
    ]
