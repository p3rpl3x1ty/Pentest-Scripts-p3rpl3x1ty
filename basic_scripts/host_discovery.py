import socket
import sys

if sys.argv[1]:
    print(socket.gethostbyname(sys.argv[1]))
else:
    print("Usage: python host_discovery.py [URL]")

