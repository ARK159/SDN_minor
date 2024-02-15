import socket

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to a specific address and port
server_address = ('127.0.0.2', 8888)
server_socket.bind(server_address)

print(f"UDP Server is listening on {server_address}")
output_filename = 'received_file.txt'
while True:
    # Receive data and address from the client
    response_data, client_address = server_socket.recvfrom(1024)
    print(f"Received data from {client_address}: {response_data.decode('utf-8')}")
    # print(type(response_data))
    response_data=response_data=response_data.decode()
    if response_data!='1':
        with open(output_filename, 'w') as file:
            file.write(response_data)
    
        # with open(output_filename,'w') as file:
        #     pass
    