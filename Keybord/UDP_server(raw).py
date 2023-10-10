import socket
import struct
bufferSize=1024
msgFromServer="Client,This is server"
serverport = 2222
serverip = '192.168.2.209'
bytestosend = msgFromServer.encode('utf-8')
RPIsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print('server is listning ...')
cnt=0
while True:
    massage, adr  = RPIsocket.recvfrom(bufferSize)
    massage = massage.decode('utf-8')
    print(massage)
    print('clinet add',adr[0])
    if massage=='b':
        cnt=cnt+1
    msg=str(cnt)
    msg=msg.encode('utf-8')
    RPIsocket.sendto(msg,adr)


