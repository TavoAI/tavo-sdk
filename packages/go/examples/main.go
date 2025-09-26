package main

import (
	"fmt"
	"log"

	"github.com/TavoAI/tavo-go-sdk/tavo"
)

func main() {
	// Create configuration
	config := tavo.NewConfig().
		WithAPIKey("your-api-key-here").
		WithBaseURL("https://api.tavoai.net")

	// Create client
	client := tavo.NewClient(config)

	// Health check
	fmt.Println("Performing health check...")
	health, err := client.HealthCheck()
	if err != nil {
		log.Printf("Health check failed: %v", err)
	} else {
		fmt.Printf("Health check response: %+v\n", health)
	}

	// Example authentication (replace with real credentials)
	fmt.Println("\nAttempting authentication...")
	auth, err := client.Auth().Login("username", "password")
	if err != nil {
		log.Printf("Authentication failed: %v", err)
	} else {
		fmt.Printf("Authentication successful: %+v\n", auth)
	}

	// Example scan operations
	fmt.Println("\nListing scans...")
	scans, err := client.Scans().ListScans(nil)
	if err != nil {
		log.Printf("Failed to list scans: %v", err)
	} else {
		fmt.Printf("Scans: %+v\n", scans)
	}

	// Example job operations
	fmt.Println("\nListing jobs...")
	jobs, err := client.Jobs().ListJobs(nil)
	if err != nil {
		log.Printf("Failed to list jobs: %v", err)
	} else {
		fmt.Printf("Jobs: %+v\n", jobs)
	}

	fmt.Println("\nGo SDK example completed!")
}
