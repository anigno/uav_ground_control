class CapabilityData:
    def __init__(self, descriptor: str, capability_bytes):
        """data produced by all capabilities"""
        self.descriptor: str = descriptor
        self.capability_bytes: bytes = capability_bytes

    def __str__(self):
        return f'(Capability: Data{self.descriptor} length:{len(self.capability_bytes)})'
