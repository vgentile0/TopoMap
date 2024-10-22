import socket

def ipHandler():
    target_ip = ""
    ip_type = int(input("Type 1 to scan by domain or 2 to scan by IPv4:  "))

    if ip_type == 1:
        domain = input("Enter target domain: ")

        #  URL parser - automatically add www. if not present
        if not domain.startswith("www."):
            domain = "www." + domain

        try:
            target_ip = socket.gethostbyname(domain)
        except socket.gaierror:
            print("Invalid domain name.")
            return None

    elif ip_type == 2:
        target_ip = input("Enter target IP: ")

    return target_ip

