from socket import *
import ssl
import base64

msg = "\r\n I love computer networks!" 
endmsg = "\r\n.\r\n"

# Choose a mail server (e.g. Google mail server) and call it mailserver 
# mailServer = "smtp.mailtrap.io" # Fill in here
mailServer = "smtp.gmail.com" # Fill in here
mailPort = 587

# Create socket called clientSocket and establish a TCP connection with mailserver 
#Fill in start
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailServer, mailPort))
#Fill in end
recv = clientSocket.recv(1024).decode() 
print(recv)
if recv[:3] != '220':
  print('220 reply not received from server.')

# Send HELO command and print server response. 
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode()) 
recv1 = clientSocket.recv(1024).decode() 
print(recv1)
if recv1[:3] != '250':
  print('250 reply not received from server.')

cmd = "STARTTLS\r\n".encode()
clientSocket.send(cmd)
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != "220":
    print("220 reply not received from server")
clientSocket = ssl.wrap_socket(clientSocket)

# Authentication details
email = (base64.b64encode("smtplab23@gmail.com".encode()) + ("\r\n").encode())
password = (base64.b64encode("lmvgusmmhxkmzoti".encode()) + ("\r\n").encode())

clientSocket.send("AUTH LOGIN\r\n".encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != "334":
    print ("334 reply not received from server")

clientSocket.send(email)
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != "334":
    print ("334 reply not received from server")
clientSocket.send(password)
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != "235":
    print ("235 reply not received from server")

# Send MAIL FROM command and print server response.
# Fill in start
mailFromCommand = 'MAIL FROM: <smptlab23@gmail.com>' + '\r\n'
clientSocket.send(mailFromCommand.encode())
# clientSocket.write(mailFromCommand)
# recv2 = clientSocket.read(1024)
recv2 = clientSocket.recv(1024).decode()
print(recv2)
if recv2[:3] != '250':
  print('250 reply not received from server.')
# Fill in end

# Send RCPT TO command and print server response.
# Fill in start 
rcptToCommand = 'RCPT TO: <sbhosale544321@gmail.com>'  + '\r\n'
clientSocket.send(rcptToCommand.encode())
# clientSocket.write(rcptToCommand)
# recv3 = clientSocket.read(1024)
recv3 = clientSocket.recv(1024).decode()
print(recv3)
if recv3[:3] != '250':
	print('250 reply not received from server.')
# Fill in end

# Send DATA command and print server response.
# Fill in start
dataCommand = 'DATA\r\n'
print(dataCommand)
clientSocket.send(dataCommand.encode())
# clientSocket.write(dataCommand)
# recv4 = clientSocket.read(1024)
recv4 = clientSocket.recv(1024).decode()
print(recv4)
if recv4[:3] != '354':
	print('354 reply not received from server.')
# Fill in end

# Send message
# data. # Fill in here
message = input('Enter Message Here: ')
# clientSocket.write(msg)

# Message ends with a single period. 
# Fill in start
mailMessageEnd = '\r\n.\r\n'
clientSocket.send(message.encode() + mailMessageEnd.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')
# clientSocket.write(endmsg)
# recv5 = clientSocket.read(1024)
# print(recv5)
# if recv5[:3] != '250':
# 	print('250 reply not received from server.')
# Fill in end

# Send QUIT command and ge server response.
# Fill in start 
quitCommand = 'QUIT\r\n'
# print(quitCommand)
clientSocket.send(quitCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '221':
    print('221 reply not received from server.')
# quitCommand = 'QUIT\r\n'
# clientSocket.write(quitCommand)
# recv6 = clientSocket.read(1024)
# print(recv6)
# if recv6[:3] != '221':
# 	print('221 reply not received from server.')
# Fill in end

clientSocket.close()