namespace communication.http2
{
    public static class Http2Client
    {
        public static async void SendDataRequest(byte[] dataBytes, string ip, uint port)
        {
            using (HttpClient client = new HttpClient())
            {
                client.BaseAddress = new Uri($"http://{ip}:{port}");
                ByteArrayContent content = new ByteArrayContent(dataBytes);
                try
                {
                    HttpResponseMessage response = await client.PostAsync("/path/to/endpoint", content);
                }
                catch (HttpRequestException ex)
                {
                    Console.WriteLine(ex.Message);
                }
                catch (Exception ex)
                {
                    Console.WriteLine(ex.Message + Environment.NewLine + ex.StackTrace);
                }
            }
        }
    }
}

