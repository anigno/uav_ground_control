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
        public static void Main() { CreateHostBuilder().Build().Run(); }

        public static IHostBuilder CreateHostBuilder() => Host.CreateDefaultBuilder()
            .ConfigureWebHostDefaults(
                webBuilder =>
                {
                    webBuilder.ConfigureKestrel(
                        options =>
                        {
                            options.Listen(
                                IPAddress.Parse("127.0.0.1"),
                                1001,
                                listenOptions =>
                                {
                                    listenOptions.Protocols = HttpProtocols.Http1AndHttp2;
                                });
                        });

                    webBuilder.UseStartup<Startup>();
                });
    }

    public class Startup
    {
        public void ConfigureServices(IServiceCollection services)
        {
            // Add any required services here
        }

        public void Configure(IApplicationBuilder app)
        {
            app.Run(
                async context =>
                {
                    var request = context.Request;
                    byte[] requestBodyBytes = await ReadRequestBodyAsync(request.Body);
                    // reverse bytes for little endian of BitConverter and get message type
                    byte[] dataBytes = new byte[] { requestBodyBytes[1], requestBodyBytes[0] };
                    ushort messageTypeValue = BitConverter.ToUInt16(dataBytes, 0);
                    // get message bytes
                    byte[] message_data_bytes = new byte[requestBodyBytes.Length - 2];
                    Array.Copy(requestBodyBytes, 2, message_data_bytes, 0, requestBodyBytes.Length - 2);

                    Console.WriteLine($"Received: message type:{messageTypeValue} {requestBodyBytes.Length}");

                    // Respond with a message (replace with your response logic)
                    await context.Response.WriteAsync("200");
                });
        }

        private async Task<byte[]> ReadRequestBodyAsync(Stream body)
        {
            using (var memoryStream = new MemoryStream())
            {
                await body.CopyToAsync(memoryStream);
                return memoryStream.ToArray();
            }
        }

    }
}