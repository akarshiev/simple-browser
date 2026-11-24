package main

import (
	"fmt"
	"net"
	"strings"
)

func main() {
	var host, port string

	fmt.Print("Who do you want to connect to: ")
	fmt.Scanln(&host)

	fmt.Print("Port number: ")
	fmt.Scanln(&port)

	host = strings.TrimSpace(host)

	fmt.Printf("Connecting to %s...\n", host)

	conn, err := net.Dial("tcp", host+":"+port)
	if err != nil {
		fmt.Println("Connection error:", err)
		return
	}
	defer conn.Close()

	// Build HTTP request
	request := fmt.Sprintf(
		"GET / HTTP/1.1\r\n"+
			"Host: %s\r\n"+
			"Connection: close\r\n"+
			"\r\n",
		host,
	)

	// Send HTTP request
	_, err = conn.Write([]byte(request))
	if err != nil {
		fmt.Println("Request error:", err)
		return
	}

	// Receive HTTP response
	buffer := make([]byte, 4096)

	n, err := conn.Read(buffer)
	if err != nil {
		fmt.Println("Read error:", err)
		return
	}

	fmt.Println(string(buffer[:n]))
}
