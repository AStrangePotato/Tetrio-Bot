import socket

def send_message(epoch, best, bestw):
    server_host="192.168.1.113"
    server_port=65432
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect((server_host, server_port))

        # Send the epoch valuea
        message = f"Epoch: {epoch} Best: {best} Weights: {bestw}"
        client_socket.sendall(message.encode('utf-8'))
        print(f"Sent: {message}")


    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        # Close the connection
        client_socket.close()

