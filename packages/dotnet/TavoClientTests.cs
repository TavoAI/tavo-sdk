using System;
using System.Threading.Tasks;
using Xunit;

namespace TavoAI.Tests
{
    public class TavoClientTests
    {
        [Fact]
        public void CreateClient_WithApiKey_ShouldSucceed()
        {
            // Arrange
            var config = new TavoConfig { ApiKey = "test-api-key" };

            // Act
            var client = new TavoClient(config);

            // Assert
            Assert.NotNull(client);
        }

        [Fact]
        public void CreateClient_WithNullConfig_ShouldThrow()
        {
            // Arrange & Act & Assert
            Assert.Throws<ArgumentNullException>(() => new TavoClient(null!));
        }

        [Fact]
        public void CreateClient_WithEmptyApiKey_ShouldThrow()
        {
            // Arrange
            var config = new TavoConfig { ApiKey = "" };

            // Act & Assert
            Assert.Throws<ArgumentException>(() => new TavoClient(config));
        }

        [Fact]
        public void DeviceOperations_ShouldNotBeNull()
        {
            // Arrange
            var config = new TavoConfig { ApiKey = "test-api-key" };
            var client = new TavoClient(config);

            // Act
            var deviceOps = client.Device;

            // Assert
            Assert.NotNull(deviceOps);
        }

        [Fact]
        public void ScannerOperations_ShouldNotBeNull()
        {
            // Arrange
            var config = new TavoConfig { ApiKey = "test-api-key" };
            var client = new TavoClient(config);

            // Act
            var scannerOps = client.Scanner;

            // Assert
            Assert.NotNull(scannerOps);
        }

        [Fact]
        public void CodeSubmissionOperations_ShouldNotBeNull()
        {
            // Arrange
            var config = new TavoConfig { ApiKey = "test-api-key" };
            var client = new TavoClient(config);

            // Act
            var codeOps = client.CodeSubmission;

            // Assert
            Assert.NotNull(codeOps);
        }
    }
}
