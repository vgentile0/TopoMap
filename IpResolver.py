import socket

def ipHandler ():
    target_ip = ""
    ip_type = int(input("Type 1 to scan by domain or 2 to scan by IPv4:  "))

# ADD URL parser to automatically add www.
    if ip_type == 1 :
        target_ip = socket.gethostbyname(input("Enter target domain: "))
    if ip_type == 2 :
        target_ip = input("Enter target IP: ")

    return target_ip
