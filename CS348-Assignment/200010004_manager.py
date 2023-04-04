from socket import *
from threading import *
import json
import time

IP_ADDRESS = "127.0.0.1"
port = 5005

# Initializes an empty dictionary called 'peer_list'.
peer_list = {}

# Initializes a threading thread_lock object called 'thread_lock'.
thread_lock = Lock()

broadcast_interval = 10 # by default set to 10 seconds

# This function starts the manager, creates a new thread to handle broadcast messages and listens for incoming connections.
def start():
    # Prints out a message that the manager has started.
    # print("Starting manager...")
    print("*** Manager Listening on", IP_ADDRESS, ":", port)
    print("[200010004] Waiting for clients/peers...")
    print("=============================================")

    # Creates a new thread to repeatedly broadcast active peer information at a set interval.
    broadcast_thread = Thread(target=check_peers)
    # print("[200010004] Broadcasting thread started...")
    broadcast_thread.start()

    # Sets up a socket connection and begins listening on the specified IP_ADDRESS address and port number.
    with socket(AF_INET, SOCK_STREAM) as soc:
        soc.bind((IP_ADDRESS, port))
        soc.listen()
        # sock.settimeout(5)
        # sock.setblocking(0)

        while True:
            # Accepts incoming connections and creates a new thread to handle each connection individually.
            conn, addr = soc.accept()
            # print("[200010004] New connection from", addr)
            t = Thread(target=handle_client, args=(conn, addr))
            t.start()

# This function starts the manager, creates a new thread to handle broadcast messages and listens for incoming connections.
def start_manager():
    # Prints out a message to confirm that the manager has started.
    print("[200010004] Starting manager...")
    # Creates a new thread to handle broadcast messages.
    broadcast_thread = Thread(target=periodic_broadcast)
    broadcast_thread.start()
    # Creates a new socket connection.
    with socket(AF_INET, SOCK_STREAM) as soc:
        # Binds the socket to the specified IP_ADDRESS and port.
        soc.bind((IP_ADDRESS, port))
        # Listens for incoming connections.
        soc.listen()
        # Loops indefinitely.
        while True:
            # Accepts a new connection and stores the connection object and address in the 'conn' and 'addr' variables respectively.
            conn, addr = soc.accept()
            # Creates a new thread to handle the connection.
            t = Thread(target=handle_client, args=(conn, addr))
            # Starts the thread.
            t.start()

def manage_peers():
    # Create a new socket object and connect it to the manager's IP and port, then send a request to join the network
    with socket(AF_INET, SOCK_STREAM) as soc:
        soc.connect((Manager_IP_ADDRESS, Manager_PORT))
        req_join = json.dumps({"type": "join"}).encode()
        soc.sendall(req_join)
        
        # Keep accepting connections and start a new thread for each connection 
        while True:
            conn, addr = soc.accept()
            t = threading.Thread(target=handling_connection, args=(conn, addr))
            t.start()

# This function handles incoming connections from other peers.
def handle_client(conn, addr):
    try:
        # Receives incoming data from the connection with a maximum buffer of 1024 bytes.
        data = conn.recv(1024)
        if data:
            # Decodes the received data as a JSON string.
            request = json.loads(data.decode())
            # If the request type is "join", adds a new peer using the provided address and port number.
            if request["type"] == "join":
                adding_peer(addr[0], request["port"])
            # If the request type is "leave", removes an existing peer using the provided address and port number.
            elif request["type"] == "leave":
                removing_peer(addr[0], request["port"])
    finally:
        # Closes the connection when finished handling any incoming requests.
        conn.close()

# This function broadcasts the active list of peers.
def broadcasting_peer_list():
    # Uses self.thread_lock as a context manager to acquire a thread_lock before modifying the shared state.
    with thread_lock:
        # Prints out a message that broadcasting has started.
        print("[200010004] Broadcasting the active peer_list")
        # Loops through all key-value pairs in the peer_list dictionary.
        for (addr, peer_port), _ in peer_list.items():
            try:
                # Tries to create a new socket connection and send a JSON-encoded message containing a list of active peers to each connected address.
                # print("Checking peers 1 ==> Active peers:", peer_list)
                with socket(AF_INET, SOCK_STREAM) as soc:
                    soc.connect((addr, peer_port))
                    # print("testing peer", addr)
                    soc.sendall(json.dumps({"peers": list(peer_list.keys())}).encode())
            except error:
                # If an error occurs during the connection or sending of the message, it is ignored.
                pass

def periodic_brroadcast():
    while True:
        # Sleeps for a set interval before broadcasting again.
        time.sleep(broadcast_interval)
        # Calls the broadcasting_peer_list function to send updated active peer information to all connected peers.
        broadcasting_peer_list()

# This function adds a new peer to the peer_list dictionary.
def adding_peer(addr, peer_port):
    # Uses self.thread_lock as a context manager to acquire a thread_lock before modifying the shared state.
    with thread_lock:
        # Adds the (addr, peer_port) key-value pair to the peer_list dictionary.
        peer_list[(addr, peer_port)] = peer_port
        print(f"[200010004] ++ Adding peer: {addr}:{peer_port}")

# This function periodically broadcasts the list of active peers to all connected peers.
def check_peers():
    while True:
        # Sleeps for a set interval before broadcasting again.
        time.sleep(broadcast_interval)
        # time.sleep(5)
        # Calls the broadcasting_peer_list function to send updated active peer information to all connected peers.
        broadcasting_peer_list()

def handle_cliennt(conn, addr):
    try:
        # Receives incoming data from the connection with a maximum buffer of 1024 bytes.
        data = conn.recv(1024)
        if data:
            # Decodes the received data as a JSON string.
            request = json.loads(data.decode())
            # If the request type is "join", adds a new peer using the provided address and port number.
            if request["type"] == "join":
                adding_peer(addr[0], request["port"])
            # If the request type is "leave", removes an existing peer using the provided address and port number.
            elif request["type"] == "leave":
                removing_peer(addr[0], request["port"])
    finally:
        # Closes the connection when finished handling any incoming requests.
        conn.close()

# This function removes a peer from the peer_list dictionary.
def removing_peer(addr, peer_port):
    # Uses self.thread_lock as a context manager to acquire a thread_lock before modifying the shared state.
    with thread_lock:
        # Deletes the (addr, peer_port) key-value pair from the peer_list dictionary.
        del peer_list[(addr, peer_port)]
        print(f"[200010004] -- Removing peer: {addr}:{peer_port}")

if __name__ == "__main__":
    
    start()
