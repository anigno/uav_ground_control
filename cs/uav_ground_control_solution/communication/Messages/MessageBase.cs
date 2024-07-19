using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace communication.Messages
{
    public enum MessageType
    {
        BASE = 100,
        STATUS_UPDATE = 101,
        CAPABILITIES_UPDATE = 102,
        FLY_TO_DESTINATION = 103
    }

    /// <summary>
    /// base class for messages
    /// </summary>
    public abstract class MessageBase
    {
        public static readonly MessageType MESSAGE_TYPE = MessageType.BASE;
        private uint messageIdCounter = 1000;
        public double SendTime = 0;
        public uint MessageId = 0;
        public MessageBase()
        {
            MessageId = Interlocked.Increment(ref messageIdCounter) - 1;
        }

        public abstract byte[] ToBuffer();

        public abstract void FromBuffer(byte[] buffer);
    }
}
