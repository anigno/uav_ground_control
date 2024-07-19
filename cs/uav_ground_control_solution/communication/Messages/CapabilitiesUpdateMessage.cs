using Capabilities;
using MessagePack;
using System.Xml.Linq;

namespace communication.Messages
{
    public class CapabilitiesUpdateMessage : MessageBase
    {
        public static readonly MessageType MESSAGE_TYPE = MessageType.CAPABILITIES_UPDATE;
        public string UavDescriptor = "";
        public List<CapabilityData> Capabilities = new List<CapabilityData>();

        public override void FromBuffer(byte[] buffer)
        {
            //deserialize using msgPack
            Dictionary<string, object> deserializedData =
                MessagePackSerializer.Deserialize<Dictionary<string, object>>(buffer);
        }

        public override byte[] ToBuffer()
        {
            // should never be used
            throw new NotImplementedException();
        }
    }
}
