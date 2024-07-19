using communication.Messages;
using MessagePack;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace communication.http2
{
    /// <summary>sends and receives messages based on MessageBase, using http2 client and server</summary>
    public class Http2Communicator
    {
        public event EventHandler<MessageBase> OnMessageReceived = delegate { };
        private MessagesFactoryBase messageFactory;
        public Http2Communicator(MessagesFactoryBase messageFactory, string local_ip, int local_port)
        {
            this.messageFactory = messageFactory;
            Http2Server.OnDataReceived += Http2Server_OnDataReceived;
            Http2Server.Init(local_ip, local_port);
        }

        public void Start()
        {
            Http2Server.Start();
        }

        private void Http2Server_OnDataReceived(object? sender, byte[] data_bytes)
        {
            // reverse bytes for little endian of BitConverter and get message type
            byte[] messageTypeBytes = [data_bytes[1], data_bytes[0]];
            ushort messageTypeValue = BitConverter.ToUInt16(messageTypeBytes, 0);
            // get message bytes
            byte[] messageDataBytes = new byte[data_bytes.Length - 2];
            Array.Copy(data_bytes, 2, messageDataBytes, 0, data_bytes.Length - 2);
            // create message instance
            MessageBase message = messageFactory.CreateMessageInstance(messageTypeValue, messageDataBytes);
            OnMessageReceived(this, message);

            

            //TODO: msgPack and use message factory to get the message
            Console.WriteLine($"****** received data {messageTypeValue} {messageDataBytes.Length}");


            Console.WriteLine($"****** unpacked");

        }
    }
}
