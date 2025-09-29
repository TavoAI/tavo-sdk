using System;
using System.Threading.Tasks;
using TavoAI;

namespace BasicScan
{
    class Program
    {
        static async Task Main(string[] args)
        {
            try
            {
                // Create configuration for mock API
                var config = new TavoConfig
                {
                    ApiKey = "test-key",
                    BaseUrl = "http://127.0.0.1:3002"
                };

                // Create client
                var client = new TavoClient(config);

                // Health check
                Console.WriteLine("Performing health check...");
                var health = await client.HealthCheckAsync();
                Console.WriteLine($".NET SDK: API health check passed - {health}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($".NET SDK: Health check failed - {ex.Message}");
                Environment.Exit(1);
            }
        }
    }
}