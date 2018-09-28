import asyncio, evdev, time, sys
from socket_connection import SocketConnection
from touch_manager import TouchManager


# Configuration steps:

# 1. Set the screen number
screen = 1
# 2. Set the broadcast IP for your router, usually ends in .255
host = '192.168.1.255'
# 3. Set the port for which to broadcast touch packets
port = 13001
# 4. Set the name of the touch input device name (find device name using evdev)
device_name = "USBest Technology SiS HID Touch Controller"


# Touch codes
focused_touch_code = 47
new_touch_code = 57
touch_end_code = -1
x_move_code = 53
y_move_code = 54


# Setup
socket_connection = SocketConnection(host, port, screen)
touch_manager = TouchManager(socket_connection)


async def handle_events(device):
    try:
        async for event in device.async_read_loop():
            if event.code == focused_touch_code:
                touch_manager.focused_touch_index = event.value
            elif event.code == new_touch_code:
                if event.value == touch_end_code:
                    touch_manager.handle_touch_up()
                else:
                    touch_manager.handle_touch_down(event)
            elif event.code == x_move_code:
                touch_manager.handle_move_x(event)
            elif event.code == y_move_code:
                touch_manager.handle_move_y(event)
    except IOError:
        print('Device disconnected: ' + device.path)
        scan_for_devices()
    except:
        print('Unexpected error: ' + sys.exc_info()[0])
        scan_for_devices()


def get_devices():
    devices = []
    for device in [evdev.InputDevice(path) for path in evdev.list_devices()]:
        if device.name == device_name:
            devices.append(evdev.InputDevice(device.path))
    return devices


def start_listening(devices):
    for device in devices:
        print("Attached to device at path: " + device.path)
        asyncio.ensure_future(handle_events(device))


def scan_for_devices():
    print('Scanning for devices named: ' + device_name)
    devices = get_devices()
    while len(devices) is 0:
        time.sleep(20)
        devices = get_devices()
    start_listening(devices)


# Ensure main is only run once
if __name__ == "__main__":
    scan_for_devices()


loop = asyncio.get_event_loop()
loop.run_forever()
