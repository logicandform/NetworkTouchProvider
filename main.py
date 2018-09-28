import evdev
import time
import sys
from socket_connection import SocketConnection
from touch_manager import TouchManager


# Configuration steps:

# 1. Set the event# file that corresponds to the connected Planar screen
input_connection = '/dev/input/event0'
# 2. Set the screen number
screen = 1
# 3. Set the broadcast IP for your router, usually ends in .255
host = '192.168.1.255'
# 4. Set the port for which to broadcast touch packets
port = 13001
# 5. Set the name of the touch input device name (find device name using evdev)
device_name = "USBest Technology SiS HID Touch Controller"


# Touch codes
focused_touch_code = 47
new_touch_code = 57
touch_end_code = -1
x_move_code = 53
y_move_code = 54


def check_for_device():
    while not evdev.util.is_device(input_connection):
        time.sleep(20)

    # Input connection established, start event loop
    socket_connection = SocketConnection(host, port, screen)
    touch_manager = TouchManager(socket_connection)
    start_event_loop(touch_manager)

def start_event_loop(manager):
    try:
        # Connect to input connection
        device = evdev.InputDevice(input_connection)

        # Parse events received from the Planar screen
        for event in device.read_loop():
            if event.code == focused_touch_code:
                manager.focused_touch_index = event.value
            elif event.code == new_touch_code:
                if event.value == touch_end_code:
                    manager.handle_touch_up()
                else:
                    manager.handle_touch_down(event)
            elif event.code == x_move_code:
                manager.handle_move_x(event)
            elif event.code == y_move_code:
                manager.handle_move_y(event)
    except IOError:
        # Close the socket connection
        manager.finish()
        check_for_device()
    except:
        print("Unexpected error:" + sys.exc_info()[0])
        # Close the socket connection
        manager.finish()


# Ensure main is only run once
if __name__ == "__main__":
    check_for_device()
