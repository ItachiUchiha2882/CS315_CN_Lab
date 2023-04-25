import socket
import random

def server_program():
  host = socket.gethostname()                       # get the hostname
  # print("host is " + host)
  port = 53535                                      # initiating port no (preferrably above 1024)
  server_socket = socket.socket()                   # get instance
  server_socket.bind((host, port))                  # bind host address and port together
  # print(server_socket)
  server_socket.listen(2)                           # configure how many client the server can listen simultaneously
  print("*** Server started ***")
  conn, address = server_socket.accept()            # accept new connection
  # print("Connection from: " + str(address))

  while True:                                       # while loop keeps waiting for client request
    data = conn.recv(1024).decode()                 # receive data stream. it won't accept data packet greater than 1024 bytes
    if not data:                                    # if data is not received break
      break
    data = data.split(',')
    # print("data : " + str(data))
    print("Client Name: ", data[0])     
    print("Server name: " + str(address)) 
    num_s = random.randint(1, 100)                  # generating random number
    num_c = int(data[1])                            # received number from client side
    sum = num_s + num_c                             # computing sum
    print("Client's number : " + str(num_c))
    print("Server's number : " + str(num_s))
    print("Sum of numbers : " + str(sum))
    data = str(host) + "," + str(sum)
    conn.send(data.encode())                        # send data to the client
  
  conn.close()                                      # close the connection


if __name__ == '__main__':
    server_program()

# Disclaimer: the assignment does not say what the client should do after it receives message from the server. So here I am just printing the number it generates.
# And also, here there won't be the case of server receiveing an integer value that is out of range, so here I am just shutting down both the server and client after generation of one random number from each side.