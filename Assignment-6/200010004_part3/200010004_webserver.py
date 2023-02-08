from socket import *

print(gethostbyname(gethostname())) # prints the ip addr of server

serverSocket = socket(AF_INET, SOCK_STREAM)

#Prepare a server socket
serverSocket.bind((gethostname(), 7902))
serverSocket.listen(1)

while True:
    #Establish the connection
    print('Ready to serve...')
    conn, addr = serverSocket.accept()
    try:
        # Receive HTTP request from browser
        msg = conn.recv(1024)
        print("\n" + str(msg))

        # Open file mentioned in the first line of the HTTP request header
        filename = msg.split()[1]
        f = open(filename[1:])
        opdata = f.read()

        #Send one HTTP header line into socket
        conn.send("HTTP/1.1 200 OK\r\n\r\n".encode())

        #Send the content of the requested file to the client
        conn.send(opdata.encode())
        conn.close()

    except IOError:
        #Send response msg for file not found
        conn.send("HTTP/1.1 404 Not Found\r\n".encode())
        msg = open("./Error.html")
        opdata = msg.read()
        conn.send(opdata.encode())
        # conn.send(msg.encode())

        #Close client socket
        conn.close()

serverSocket.close()