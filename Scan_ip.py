import socket, struct,sys

def atod(a): # ascii_to_decimal
    return struct.unpack("!L",socket.inet_aton(a))[0]

def dtoa(d): # decimal_to_ascii
    return socket.inet_ntoa(struct.pack("!L", d))

net,_,mask = sys.argv[1].partition('/')
mask = int(mask)
net = atod(net)

for host in (dtoa(net+n) for n in range(0, 1<<32-mask)):
    print host
