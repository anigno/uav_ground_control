using Capabilities;
using communication.Messages;
using MessagePack;
using System.Runtime.Intrinsics.X86;
using static System.Runtime.InteropServices.JavaScript.JSType;

namespace Testing.TestCommunication
{
    class TestMessage : MessageBase
    {
        public int val = 11;
        public string name = "hello";

        public override byte[] ToBuffer()
        {
            Dictionary<string, object> d = new Dictionary<string, object>();
            d["val"] = val;
            d["name"] = name;
            byte[] serializedData = MessagePackSerializer.Serialize(d);
            return serializedData;
        }

        public override void FromBuffer(byte[] buffer)
        {
            Dictionary<string, object> d =
                MessagePackSerializer.Deserialize<Dictionary<string, object>>(buffer);
            val = (int)d["val"];
            name = (string)d["name"];
        }
    }

    public class TestMessages
    {
        [SetUp]
        public void Setup()
        {
        }


        [Test]
        public void TestMessageBase()
        {
            TestMessage message = new TestMessage();
            byte[] b1 = message.ToBuffer();
            TestMessage message2 = new TestMessage();

            message2.FromBuffer(b1);
            Assert.That(message2.val, Is.EqualTo(message.val));
            Assert.That(message2.name, Is.EqualTo(message.name));
        }

        [Test]
        public void TestCapabilitiesUpdateMessage()
        {
            CapabilitiesUpdateMessage message = new CapabilitiesUpdateMessage();
            message.SendTime = 1234.567;
            message.UavDescriptor = "UAV01";
            message.Capabilities = new List<CapabilityData>() {
                new CapabilityData("Cam761", new byte[] { 1, 2, 3, 4 }) };
            byte[] b = message.ToBuffer();

            CapabilitiesUpdateMessage message2 = new CapabilitiesUpdateMessage();
            message2.FromBuffer(b);
            Assert.That(message2.UavDescriptor, Is.EqualTo(message.UavDescriptor));

        }
    }
}