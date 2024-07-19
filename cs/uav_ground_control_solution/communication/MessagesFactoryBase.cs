using communication.Messages;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;

namespace communication
{
    /// <summary>base for messages factory, creates message instance from given message type and data bytes</summary>
    public abstract class MessagesFactoryBase
    {
        private Dictionary<int, MessageBase> messagesDictionary = new Dictionary<int, MessageBase>();

        public MessagesFactoryBase()
        {
            initMessages();
        }

        public MessageBase CreateMessageInstance(int messageType, byte[] message_bytes)
        {

        }

        public abstract void initMessages();
    }
}
