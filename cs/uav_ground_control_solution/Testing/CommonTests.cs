using communication.http2;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Server.Kestrel.Core;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using System;
using System.Net;
using System.Text;

namespace Testing
{
    class Program
    {
        public static void Main()
        {
            Http2Server.Init("127.0.0.1", 1001);
            Http2Server.OnDataReceived += Http2Server_OnDataReceived;
            Http2Server.Start();
        }

        private static void Http2Server_OnDataReceived(object? sender, byte[] data_bytes)
        {
            // reverse bytes for little endian of BitConverter and get message type
            byte[] dataBytes = [data_bytes[1], data_bytes[0]];
            ushort messageTypeValue = BitConverter.ToUInt16(dataBytes, 0);
            // get message bytes
            byte[] messageDataBytes = new byte[data_bytes.Length - 2];
            Array.Copy(data_bytes, 2, messageDataBytes, 0, data_bytes.Length - 2);
            Console.WriteLine($"{messageTypeValue} {messageDataBytes.Length}");
        }
    }
}