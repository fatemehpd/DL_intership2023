import socket

msgfromclint = 'this is clinet(Ground Station)'
bytestosend =msgfromclint.encode('utf-8')
serveradd=('172.20.2.2',2222)
buffersize=1024
UDPclient= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
    cmd=input('input ? ')
    cmd = cmd.encode('utf-8')
    UDPclient.sendto(cmd,serveradd)
    data,add= UDPclient.recvfrom(buffersize)
    data= data.decode('utf-8')
    print('data from server',data) 
    print('server IP Add : ', add[0])
    print('server port: ', add[1])
