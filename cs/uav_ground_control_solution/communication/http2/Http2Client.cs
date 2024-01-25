using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System;
using System.Net.Http;
using System.Threading.Tasks;
using static System.Runtime.InteropServices.JavaScript.JSType;

namespace communication.http2
{
    public static class Http2Client
    {
        //private static HttpClient client = new HttpClient();

        public static async void SendDataRequest(byte[] dataBytes, string ip, uint port)
        {
            using(HttpClient client = new HttpClient())
            {
                client.BaseAddress = new Uri($"http://{ip}:{port}");
                ByteArrayContent content = new ByteArrayContent(dataBytes);
                HttpResponseMessage response = await client.PostAsync("/path/to/endpoint", content);
                if(response.IsSuccessStatusCode)
                {
                    string responseBody = await response.Content.ReadAsStringAsync();
                } else
                {
                    var code = response.StatusCode;
                }
            }
        }
        //static async Task SendByteArrayViaHttp2()
        //{
        //    // Create an instance of HttpClient
        //    using (HttpClient client = new HttpClient())
        //    {
        //        // Set the base address of the server
        //        client.BaseAddress = new Uri("http://127.0.0.1:1001");

        //        // Create a byte array to send
        //        byte[] data = new byte[] { 0x48, 0x65, 0x6C, 0x6C, 0x6F }; // Example: "Hello"

        //        // Create ByteArrayContent with the byte array
        //        ByteArrayContent content = new ByteArrayContent(data);

        //        // Send an HTTP POST request with the byte array content
        //        HttpResponseMessage response = await client.PostAsync("/path/to/endpoint", content);

        //        // Check if the request was successful
        //        if (response.IsSuccessStatusCode)
        //        {
        //            // Read the response content
        //            string responseBody = await response.Content.ReadAsStringAsync();
        //            Console.WriteLine($"Response: {responseBody}");
        //        }
        //        else
        //        {
        //            Console.WriteLine($"HTTP request failed with status code: {response.StatusCode}");
        //        }
        //    }
        //}
    }



}

