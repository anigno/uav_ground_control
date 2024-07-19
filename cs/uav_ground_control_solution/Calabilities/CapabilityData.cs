namespace Capabilities
{
    public class CapabilityData
    {
        public string Descriptor { get; private set; }
        public byte[] CapabilityBytes { get; private set; }

        // Constructor
        public CapabilityData(string descriptor, byte[] capabilityBytes)
        {
            Descriptor = descriptor;
            CapabilityBytes = capabilityBytes;
        }

        // Override the ToString method for a readable representation
        public override string ToString()
        {
            return $"(Capability: Data{Descriptor} length:{CapabilityBytes.Length})";
        }
    }
}
