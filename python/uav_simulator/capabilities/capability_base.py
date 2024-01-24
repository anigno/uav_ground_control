from abc import ABC, abstractmethod

from uav_simulator.capabilities.capability_data import CapabilityData
from uav_simulator.data_types.uav_status import UavStatus

class CapabilityBase(ABC):
    """base class for all capabilities"""

    @abstractmethod
    def get(self, uav_status: UavStatus) -> CapabilityData:
        pass
