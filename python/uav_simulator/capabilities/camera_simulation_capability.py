from PIL import Image
import io

from python.uav_simulator.capabilities.capability_base import CapabilityBase
from python.uav_simulator.capabilities.capability_data import CapabilityData
from python.uav_simulator.data_types.uav_status import UavStatus

class CameraSimulationCapability(CapabilityBase):
    def __init__(self):
        # print(os.getcwd())
        image_path = r'..\..\testings\house.jpg'
        image = Image.open(image_path)
        image_bytes = io.BytesIO()
        image.save(image_bytes, format='JPEG')
        self.image_bytes = image_bytes.getvalue()
        image.close()

    def get(self, uav_status: UavStatus) -> CapabilityData:
        return CapabilityData('CAMERA01_JPG', self.image_bytes)

if __name__ == '__main__':
    c = CameraSimulationCapability()
    print(c.get(UavStatus()))
