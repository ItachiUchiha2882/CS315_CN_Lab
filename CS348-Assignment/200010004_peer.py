import sys
from socket import *
import threading
import json
import time

# Set the IP address of the network manager
Manager_IP_ADDRESS = "127.0.0.1"

# Initialize an empty dictionary to store information about all peers in the system
peer_list = {}

# Set the port number of the network manager
Manager_PORT = 5005

# Create a list of files that can be shared by all peers in the network
share_files = ["data.txt"]

def handling_connection(conn, addr):
    # Try to receive data from the connection
    try:
        data = conn.recv(1024)

        # If there is data, decode it and check what type of request it is
        if data:
            request = json.loads(data.decode())
            
            # If the request contains a new list of peers, update the current peer list
            if "peers" in request:
                updating_peer_list(request["peers"])
                
            # If the request is for a file fragment, check if the requested file exists in share_files
            elif request["type"] == "requesting_file":
                file_name = request["file_name"]
                if file_name in share_files:
                    with open(file_name, "r") as file:
                        content_file = file.read()
                        
                        # Calculate the size of each fragment and the starting and ending indices of this fragment
                        size_file = len(content_file)
                        size_frag = size_file // len(peer_list)
                        # print(size_frag)
                        start_frag = request["fragment_number"] * size_frag
                        # print(start_frag)
                        end_frag = start_frag + size_frag
                        # print(end_frag)
                        
                        # Adjust the ending index of the last fragment
                        if request["fragment_number"] == len(peer_list) - 1:
                            end_frag = size_file
                        
                        # Extract the requested file fragment and send it back to the requester
                        file_fragment = content_file[start_frag:end_frag]
                        res = json.dumps({"type": "file_fragment", "file_name": file_name, "file_fragment": file_fragment, "fragment_number": request["fragment_number"]}).encode()
                        conn.sendall(res)
                        
    finally:
        # Commented out line to close the connection - this may cause issues if the same socket is reused later!
        # conn.close()
        pass

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

def requesting_file(file_name):
    # Create a separate list of peers that participated in the file transfer
    transfer_peers = peer_list.copy()

    # Initialize variables to keep track of file fragments received and whether all fragments have been received
    file_fragments = [None] * len(peer_list)
    frags_completed = 0

    # This function handles the file fragment response from other peers
    def handling_response_fragment(conn, addr):
        nonlocal frags_completed
        data = conn.recv(1024)
        if data:
            res = json.loads(data.decode())
            # print(f"[200010004] Received fragment {res['fragment_number']} from {addr[0]}:{addr[1]}")
            if res["type"] == "file_fragment":
                file_fragments[res["fragment_number"]] = res["file_fragment"]
                frags_completed += 1
                print(f"[200010004] Received fragment {res['fragment_number']} from {addr[0]}:{addr[1]}")

    # Request file fragments from all active peers
    for idx, ((addr, port), _) in enumerate(transfer_peers.items()):
        with socket(AF_INET, SOCK_STREAM) as soc:
            soc.connect((addr, port))
            request = json.dumps({"type": "requesting_file", "file_name": file_name, "fragment_number": idx}).encode()
            soc.sendall(request)
            print(f"[200010004] Requested fragment {idx} from {addr}:{port}")

            # Start a new thread to handle incoming responses for this file fragment
            t = threading.Thread(target=handling_response_fragment, args=(soc, (addr, port)))
            t.start()

    # Wait until all file fragments are received before reconstructing the original file
    while frags_completed < len(peer_list):
        time.sleep(0.1)

    # Reconstruct the original file and save it locally
    transmitted_file = "".join(file_fragments)
    with open(f"transmitted_{file_name}", "w") as op_file:
        op_file.write(transmitted_file)

    print(f"[200010004] File transfer complete for {file_name}")
    
def connecting_manager(ip, port):
    # Print a message indicating that a new peer has joined the network with provided IP address and port number
    print(f"[200010004] New peer joined network as {ip}:{port}")

    # Create a new socket object and bind it to provided IP and port
    with socket(AF_INET, SOCK_STREAM) as soc:
        soc.bind((ip, port))
        # soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.listen()

        # Create a new socket object and connect it to the manager's IP and port, then send a request with the port number
        with socket(AF_INET, SOCK_STREAM) as manager_conn:
            manager_conn.connect((Manager_IP_ADDRESS, Manager_PORT))
            # if manager_conn != port:
                # print("manager_con is", manager_conn)
                # pass
            req_join = json.dumps({"type": "join", "port": port}).encode()
            manager_conn.sendall(req_join)

        # Keep accepting connections and start a new thread for each connection 
        while True:
            conn, addr = soc.accept()
            t = threading.Thread(target=handling_connection, args=(conn, addr))
            t.start()

def updating_peer_list(new_peers):
    # Create a new dictionary mapping (address, port) tuples to their corresponding port numbers
    peers_updated = {(peer_addr, peer_port): peer_port for peer_addr, peer_port in new_peers}
    
    # Update the existing peer_list with the new information
    peer_list.update(peers_updated)
    
    # Print out a message indicating that the peer list has been updated
    print("[200010004] Updated active peer_list: {}".format(peer_list))

def disconnecting_from_manager(ip, port):
    # Print a message indicating that this peer left the network with provided IP and port number
    print("[200010004] Peer left the network {}:{}".format(ip, port))

    # Create a new socket object and connect to the manager's IP and port,
    # then send a request with the port number to notify the manager that this peer is leaving the network
    with socket(AF_INET, SOCK_STREAM) as soc:
        soc.connect((Manager_IP_ADDRESS, Manager_PORT))
        leave_request = json.dumps({"type": "leave", "port": port}).encode()
        soc.sendall(leave_request)
        # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as manager_conn:
        #     manager_conn.connect((Manager_IP_ADDRESS, Manager_PORT))
        #     req_join = json.dumps({"type": "join", "port": port}).encode()
        #     manager_conn.sendall(req_join)

def handlling_connection(conn, addr):
    # Keep receiving data from the connection and handle the request
    with conn:
        # print("conn is", conn)
        while True:
            data = conn.recv(1024)
            if data:
                res = json.loads(data.decode())
                # print(f"[200010004] Received {res['type']} from {addr[0]}:{addr[1]}")
                if res["type"] == "join":
                    # Add the new peer to the peer list
                    peer_list[(addr[0], res["port"])] = res["port"]
                    print(f"[200010004] New peer joined network as {addr[0]}:{res['port']}")

                    # Send the updated peer list to the new peer
                    res = json.dumps({"type": "peer_list", "peer_list": list(peer_list.keys())}).encode()
                    conn.sendall(res)
                elif res["type"] == "leave":
                    # Remove the peer from the peer list
                    peer_list.pop((addr[0], res["port"]), None)
                    print(f"[200010004] Peer left the network {addr[0]}:{res['port']}")
                elif res["type"] == "peer_list":
                    # Update the peer list with the new information
                    updating_peer_list(res["peer_list"])
                elif res["type"] == "requesting_file":
                    # If this peer has the requested file, send the file fragment to the requesting peer
                    if res["file_name"] in file_list:
                        with open(res["file_name"], "r") as ip_file:
                            file_fragments = ip_file.read().splitlines()
                            res = json.dumps({"type": "file_fragment", "file_fragment": file_fragments[res["fragment_number"]], "fragment_number": res["fragment_number"]}).encode()
                            conn.sendall(res)
                elif res["type"] == "file_fragment":
                    # If this peer is the one requesting the file, save the file fragment
                    if res["file_name"] in file_list:
                        file_fragments[res["fragment_number"]] = res["file_fragment"]
                        frags_completed += 1
                        print(f"[200010004] Received fragment {res['fragment_number']} from {addr[0]}:{addr[1]}")
            else:
                break

def connectingg_peer():
    # Create a new socket object and connect to the manager's IP and port, then send a request with the port number
    with socket(AF_INET, SOCK_STREAM) as soc:
        soc.connect((Manager_IP_ADDRESS, Manager_PORT))
        with soc as s:
            # print("socket is", s)
            pass
        req_join = json.dumps({"type": "join", "port": port}).encode()
        soc.sendall(req_join)

if __name__ == "__main__":
    # Get the peer's port number from the command-line arguments
    PORT = sys.argv[1]
    PORT = int(PORT)

    # Start a new thread to handle incoming connections from other peers
    peer_thread = threading.Thread(target=connecting_manager, args=("127.0.0.1", PORT))
    peer_thread.start()

    # If this is the first peer in the network, wait 15 seconds and request a file
    if PORT == 5004:
        time.sleep(15)  # sleeping for 15 seconds
        requesting_file("data.txt")

    # Check for an optional third argument specifying a time delay before disconnecting
    arg_len = len(sys.argv)
    if arg_len == 3:
        time_delay = sys.argv[2]
        time_delay = int(time_delay)
        if type(time_delay) == int:   # Check that the delay is an integer
            time.sleep(time_delay)
            disconnecting_from_manager("127.0.0.1", PORT)
        else:
            print("Make sure that last argument is an integer")


