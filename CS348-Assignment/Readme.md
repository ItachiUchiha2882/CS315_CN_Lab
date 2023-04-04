Demo video link : https://drive.google.com/file/d/1vwoyIOygvfaL_Wkz_TAFiW373CcLZ_f8/view?usp=sharing

## Code Files
-- 200010004_manager.py 
    - start_manager(): This function starts the manager, creates a new thread to handle broadcast messages and listens for incoming connections
    - removing_peer(): This function removes a peer from the peer_list dictionary.
    - adding_peer(): This function adds a new peer to the peer_list dictionary.
    - broadcasting_peer_list(): This function broadcasts the active list of peers.
    - handle_client(): This function handles incoming connections from other peers.
    - start():  This function starts the manager, creates a new thread to handle broadcast messages and listens for incoming connections.
    - check_peers(): This function periodically broadcasts the list of active peers to all connected peers.
    - Main program execution will start from start() function.
  
-- 200010004_peer.py
    - connecting_manager(): This function helps in connecting to the manager.
    - disconnecting_from_manager(): This function helps in disconnecting from the manager.
    - requesting_file(): This function helps in requesting a file from another peer.
    - handling_response_fragment(): This function handles the file fragment response from other peers
    - handling_connection(): This function handles the connection request from other peers.
    - updating_peer_list(): This function updates the peer list of the current peer.
    - start(): This function starts the peer, creates a new thread to handle incoming connections and listens for incoming connections.

## Demo Instructions
- In one terminal, run `python3 200010004_manager.py`.
    - This tab will function like a network console
- In other terminal, run `python3 200010004_peer.py <port_number>`.
    - This tab will function like a peer
    - Note that the port number is a mandatory argument.
    - Now, if you want your peer to disconnect from the manager, use `python3 200010004_peer.py <port_number> <time_delay>` where time_delay is the time in seconds after which the peer will disconnect from the manager.
    - In main function, we have coded the condition that if the port number is 5004, peer will request 'data.txt' file and the result will be stored in 'transmitted_data.txt' file.
    - Note that, broadcast_interval is set to 10 by default
    - If peer gets connected or removed, the corresponding message will be displayed in the manager console as well as peer console.
- You can also run multiple peers in different terminals.
- For some debugging and video recording, I used my friend's laptop as in my case it was giving some OS errors.
- Use `Ctrl+C` to terminate the peers first, after operations are completed.
- Finally, terminate the manager with a kill signal by `Ctrl+C`.
