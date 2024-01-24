from enum import Enum

class MessageTypeEnum(Enum):
    """every message class must have a class field named MESSAGE_TYPE set to this enum"""
    BASE = 100
    STATUS_UPDATE = 101
    CAPABILITIES_UPDATE = 102
    FLY_TO_DESTINATION = 103
