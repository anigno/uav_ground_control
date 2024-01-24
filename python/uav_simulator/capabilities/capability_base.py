from abc import ABC, abstractmethod

from python.uav_simulator.capabilities.capability_data import CapabilityData
from python.uav_simulator.data_types.uav_status import UavStatus

class CapabilityBase(ABC):
    """base class for all capabilities"""

    @abstractmethod
    def get(self, uav_status: UavStatus) -> CapabilityData:
        pass
