import evdev as e
from socket_connection import SocketConnection
from touch_manager import TouchManager

# Configuration steps:

# 1. Set the event# file that corresponds to the connected Planar screen
device = e.InputDevice('/dev/input/event1')
# 2. Set the screen number
screen = 1
# 3. Set the broadcast IP for your router, usually ends in .255
host = '10.0.0.255'
# 4. Set the port for which to broadcast touch packets
port = 12221


# Touch codes
focused_touch_code = 47
new_touch_code = 57
touch_end_code = -1
x_move_code = 53
y_move_code = 54


def start_event_loop(manager):
    # Connect to device's input file
    device.grab()

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

    # Close the socket connection
    manager.finish()


# Ensure main is only run once
if __name__ == "__main__":
    socket_connection = SocketConnection(host, port, screen)
    touch_manager = TouchManager(socket_connection)
    start_event_loop(touch_manager)
