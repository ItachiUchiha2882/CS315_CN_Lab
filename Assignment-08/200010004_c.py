# Note : Please, change the recipient mail at line no 16 accordingly.
from socket import *
import ssl
import base64

msg = "\r\n I love computer networks!" 
endmsg = "\r\n.\r\n"

# Choose a mail server (e.g. Google mail server) and call it mailserver 
# mailServer = "smtp.mailtrap.io" # Fill in here
mailServer = "smtp.gmail.com" # Fill in here
mailPort = 587

# All sender and receiver information
sender = "<smtplab23@gmail.com>"
recipient = "<rcpt@gmail.com>"
username = "smtplab23@gmail.com"
password = "lmvgusmmhxkmzoti"

# Create socket called clientSocket and establish a TCP connection with mailserver 
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailServer, mailPort))
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

# Request an encrypted connection
TLScmd = "STARTTLS\r\n"
clientSocket.send(TLScmd.encode())
tls_recv = clientSocket.recv(1024).decode()
print(tls_recv)
if tls_recv[:3] != "220":
    print("220 reply not received from server")

# Encrypt the socket
clientSocket = ssl.wrap_socket(clientSocket)

# Send the AUTH LOGIN command and print server response.
authCommand = 'AUTH LOGIN\r\n'
clientSocket.send(authCommand.encode())
auth_recv = clientSocket.recv(1024).decode()
print(auth_recv)
if auth_recv[:3] != '334':
	print('334 reply not received from server')

# Send username and print server response.
email = base64.b64encode(username.encode()) + ('\r\n').encode()
clientSocket.send(email)
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '334':
	print('334 reply not received from server')

# Send password and print server response.
password = base64.b64encode(password.encode()) + ('\r\n').encode()
clientSocket.send(password)
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '235':
	print('235 reply not received from server')

# Send MAIL FROM command and print server response.
mailFromCommand = 'MAIL FROM: ' + sender + '\r\n'
clientSocket.send(mailFromCommand.encode())
recv2 = clientSocket.recv(1024).decode()
print(recv2)
if recv2[:3] != '250':
  print('250 reply not received from server.')

# Send RCPT TO command and print server response.
rcptToCommand = 'RCPT TO: ' +  recipient  + '\r\n'
clientSocket.send(rcptToCommand.encode())
recv3 = clientSocket.recv(1024).decode()
print(recv3)
if recv3[:3] != '250':
	print('250 reply not received from server.')

# Send DATA command and print server response.
dataCommand = 'DATA\r\n'
print(dataCommand)
clientSocket.send(dataCommand.encode())
recv4 = clientSocket.recv(1024).decode()
print(recv4)
if recv4[:3] != '354':
	print('354 reply not received from server.')

# Send message
message = input('Enter Message Here: ')

# Message ends with a single period. 

mailMessageEnd = '\r\n.\r\n'
clientSocket.send(message.encode() + mailMessageEnd.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')

# Send QUIT command and ge server response.
quitCommand = 'QUIT\r\n'
clientSocket.send(quitCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '221':
    print('221 reply not received from server.')

clientSocket.close()