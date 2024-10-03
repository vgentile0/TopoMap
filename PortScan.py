import socket

def scan_port(ip, port):
    portDic= {}
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(1)
    result = sock.connect_ex((ip, port))
    if result == 0:
        print(f"Port {port} is open")
        portDic[port] = True

    else:
        print(f"Port {port} is closed")
        portDic[port] = False
    sock.close()