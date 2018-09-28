import socket
import sys
from struct import pack

# Packet type identifiers
touch_down_id = 1000
touch_up_id = 1001
touch_move_id = 1002


# Creates a socket connection to broadcast touch objects.
class SocketConnection(object):

    def __init__(self, host, port, screen):
        self.host = host
        self.port = port
        self.screen = screen
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            print('Socket created.')
        except socket.error as msg:
            print('Could not create socket. Socket error ' + str(msg[0]) + ' message ' + msg[1])
            sys.exit()
        try:
            self.socket.bind((host, port))
            print("Broadcasting touches...")
        except socket.error as msg:
            print('Bind failed: ' + str(msg))
            sys.exit()

    def broadcast(self, p_type, x, y, t):
        # UInt32, size=28, Int32 type, Int32 id (-1), Int screen, Int touch, Int x, Int y
        data = pack('@Iiiiiii', 28, p_type, -1, int(self.screen), int(t), int(x), int(y))
        self.socket.sendto(data, (self.host, self.port))

    def send_touch_down(self, touch):
        print('Touch ' + str(touch.identifier) + ' down at ' + str((touch.xPos, touch.yPos)))
        self.broadcast(touch_down_id, touch.xPos, touch.yPos, touch.identifier)

    def send_touch_up(self, touch):
        print('Touch ' + str(touch.identifier) + ' up at ' + str((touch.xPos, touch.yPos)))
        self.broadcast(touch_up_id, touch.xPos, touch.yPos, touch.identifier)

    def send_touch_moved(self, touch):
        print('Touch ' + str(touch.identifier) + ' moved to ' + str((touch.xPos, touch.yPos)))
        self.broadcast(touch_move_id, touch.xPos, touch.yPos, touch.identifier)

    def close_connection(self):
        self.socket.close()
