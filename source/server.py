import socket
import sys
import argparse

def create_socket():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return s
    except socket.error as e:
        print(f"Could not create socket due to {e}")
        exit(0)

def argument_parser():
    port = 5000
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type = int , help="port to connect to ")
    args = parser.parse_args()
    if(args.port):
        port = args.port
    else:
        print(f"No port provided. Using port: {port}")

    return port

def accept(s):
    try: 
        connection, clientaddr = s.accept()
        return (connection, clientaddr)
    except socket.error as e:
        print(e)
        exit(0)


def recv(connection):
    try:
        data = connection.recv(1024)
        return data
    except socket.error as e:
        print(e)
        exit(0)


def send(connection, data):
    try:
        connection.sendall(str.encode(data))
    except socket.error as e:
        print(f"Unable to send data {e}")
        connection.close()

def bind(sk, port):
    try:
        sk.bind(('', port))
    except socket.error as e:
        print(e)
        exit(0)


def listen(sk):
    try:
        sk.listen(1)
    except socket.error as e:
        print(F"Socket unable to listen {e}")
        exit(0)

def count_char(content):
    content.replace('\n', '')
    count = 0
    for c in content:
        if c.isalpha():
            count+=1
    
    return count

def main():
    port = argument_parser()
    s = create_socket()
    bind(s,port)
    listen(s)
    try:
        while(True):
            print(f"Waiting for connection on port: {port}")
            connection, addr = accept(s)
            clientaddr, val = addr
            print(f"Connection from : {clientaddr}")

            while (True):
                data = recv(connection).decode()

                if(data):
                    file_size = int(data)
                    send(connection, "Size received")
                    
                    received_content = b""
                    while len(received_content) < file_size:
                        chunk = recv(connection)
                        if not chunk:
                            break
                        received_content += chunk
                    char_count = count_char(received_content.decode())
                    send(connection,str(char_count))

                else:
                    print("All requests completed")
                    break
    except KeyboardInterrupt as e:
        print("Shutting Server")
        s.close()
        exit(0)

main()