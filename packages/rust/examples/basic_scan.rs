use tavo_ai::TavoClient;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Create client with test configuration
    let client = TavoClient::with_base_url(
        "test-key",
        "http://127.0.0.1:3001",
    )?;

    // Test basic API connectivity with health check
    println!("Performing health check...");
    match client.health_check().await {
        Ok(response) => {
            println!("Rust SDK: API health check passed - {:?}", response);
        }
        Err(e) => {
            println!("Rust SDK: Health check failed - {}", e);
            return Err(e.into());
        }
    }

    Ok(())
}