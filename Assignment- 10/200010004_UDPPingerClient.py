from socket import *
import time

port = 12000
sock = socket(AF_INET, SOCK_DGRAM)
server_addr = ('localhost', port)
sock.settimeout(1)
print("*** Client started ***")

try:
  for i in range(1, 11):
    start = time.time()
    message = 'Ping #' + str(i) + " " + time.ctime(start)
    try:
      sent = sock.sendto(message.encode(), server_addr)
      print("Sent " + message)
      data, server = sock.recvfrom(4096)
      print("Received " + str(data))
      end = time.time();
      elapsed = end - start
      print("RTT: " + str(elapsed) + " seconds\n")
    except timeout:
      print("#" + str(i) + " Requested Time out\n") 

finally:
  print("** closing socket **")
  sock.close()