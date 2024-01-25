using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Server.Kestrel.Core;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using System;
using System.Net;
using System.Text;


namespace communication.http2
{
    public static class Http2Server
    {
        private static string localIp = "";
        private static int localPort = -1;

        public static event EventHandler<byte[]> OnDataReceived = delegate { };

        public static void RaiseEvent(byte[] data_bytes)
        {
            OnDataReceived(null, data_bytes);
        }

        public static void Init(string ip, int port)
        {
            localIp = ip;
            localPort = port;
        }

        public static void Start()
        {
            CreateHostBuilder(localIp, localPort).Build().Run();
        }

        public static IHostBuilder CreateHostBuilder(string localIp, int localPort) => Host.CreateDefaultBuilder()
            .ConfigureWebHostDefaults(
                webBuilder =>
                {
                    webBuilder.ConfigureKestrel(
                        options =>
                        {
                            options.Listen(
                                IPAddress.Parse(localIp),
                                localPort,
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
                    Http2Server.RaiseEvent(requestBodyBytes);
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