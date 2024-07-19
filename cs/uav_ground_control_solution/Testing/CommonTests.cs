using communication.http2;

namespace Testing
{
    class Program
    {
        public static void Main()
        {
            Task.Factory
                .StartNew(
                    () =>
                    {
                        Http2Server.Init("127.0.0.1", 1001);
                        Http2Server.OnDataReceived += Http2Server_OnDataReceived;
                        Http2Server.Start();
                    });

            Task.Factory
                .StartNew(
                    async () =>
                    {
                        while (true)
                        {
                            // convert current milliseconds to bytes
                            long ms = DateTime.Now.Ticks / TimeSpan.TicksPerMillisecond;
                            byte[] bytes = BitConverter.GetBytes(ms);
                            // send the bytes
                            Http2Client.SendDataRequest(bytes, "127.0.0.1", 1001);
                            await Task.Delay(TimeSpan.FromSeconds(1));

                        }
                    });
            Console.WriteLine("enter to exit");
            Console.ReadLine();

        }


        private static void Http2Server_OnDataReceived(object? sender, byte[] data_bytes)
        {
            // reverse bytes for little endian of BitConverter and get message type
            byte[] dataBytes = [data_bytes[1], data_bytes[0]];
            ushort messageTypeValue = BitConverter.ToUInt16(dataBytes, 0);
            // get message bytes
            byte[] messageDataBytes = new byte[data_bytes.Length - 2];
            Array.Copy(data_bytes, 2, messageDataBytes, 0, data_bytes.Length - 2);
            Console.WriteLine($"received data {messageTypeValue} {messageDataBytes.Length}");
        }
    }
}