import socket
import sys
import argparse
import os

def create_socket():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return s
    except socket.error as e:
        print(f"Could not create socket due to {3}")
        exit(0)


def send(connection, data):
    try:
        connection.sendall(str.encode(data))
    except socket.error as e:
        print(f"Unable to send data {e}")
        connection.close()

def recv(connection):
    try:
        data = connection.recv(1024)
        return data
    except socket.error as e:
        print(e)
        exit(0)

def connect(sk,ip_addr, port):
    try:
        sk.connect((ip_addr,port))
    except socket.error as e:
        print(f"Unable to connect. Error: {e}")
        exit(0)


def argument_parser():
    port = 80
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", nargs='+',required=True,help="name of the file to read")
    parser.add_argument("-p", "--port", type = int , help="port to connect to ")
    parser.add_argument("-ip_addr", "--ip_address", required=True, help="the server's ip address")
    args = parser.parse_args()
    if(args.filename):
        filename=args.filename
    else:
        print("No file name provided")
        exit(0)
    
    if(args.port):
        port = args.port
    else:
        print(f"No port provided. Using port: {port}")

    if(args.ip_address):
        ip_addr = args.ip_address
    else:
        print("No IP address provied")
        exit(0)

    return (port,filename,ip_addr)

def open_file(filename):
    if(os.path.isfile(filename)):
        content = open(filename, "r")
        return content.read()
    else:
        return ""

def file_size(filename):
    return os.path.getsize(filename)

def main():
    s = create_socket()
    port,filenames,ip_addr = argument_parser()
    print(f"Connnecting to {ip_addr} on port {port}")
    connect(s,ip_addr,port)
    try:
        for file in filenames:
            file_content = open_file(file)

            if(file_content == ""):
                print("No file found")
                continue
            
            send(s,str(file_size(file)))

            if(recv(s).decode() == "Size received"):
                send(s,file_content)
                response = int(recv(s).decode())
                print(f"Character Count for {file}: {response}")
    finally:
        print("closing socket")
        s.close()
main()