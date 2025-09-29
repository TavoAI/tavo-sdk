package main

import (
	"fmt"
	"log"

	"github.com/TavoAI/tavo-go-sdk/tavo"
)

func main() {
	// Create configuration for mock API
	config := tavo.NewConfig().
		WithAPIKey("test-key").
		WithBaseURL("http://localhost:3001")

	// Create client
	client := tavo.NewClient(config)

	// Health check
	fmt.Println("Performing health check...")
	health, err := client.HealthCheck()
	if err != nil {
		log.Printf("Health check failed: %v", err)
	} else {
		fmt.Printf("Go SDK: API health check passed - %+v\n", health)
	}
}
