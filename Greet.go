package main

import (
	"fmt"
)

// Simulated list of WhatsApp group members
var members = []string{
	"Alice",
	"Bob"
	"Charlie",
	"David",
	"Eva",
}

// greetMembers loops through the member list and prints a greeting
func greetMembers(members []string) {
	for _, member := range members {
		fmt.Printf("Hello, %s! Welcome to the group chat. 🎉\n", member)
	}
}

func main() {
	fmt.Println("Sending greetings to all group members...")
	greetMembers(members)
	fmt.Println("All members have been greeted!")
}
