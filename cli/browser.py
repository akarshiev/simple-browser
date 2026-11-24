import socket

host = input("Who do you want to connect to: ")
port = int(input("Port number: "))

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print(f"Connecting to {host}...")
client.connect((host, port))

# Build HTTP request
request = (
    f"GET / HTTP/1.1\r\n"
    f"Host: {host}\r\n"
    f"Connection: close\r\n"
    f"\r\n"
)

# Send HTTP request
client.sendall(request.encode())

# Receive HTTP response
response = client.recv(4096)

print(response.decode())

# Close connection
client.close()
