import asyncio, evdev


# Touch codes
focused_touch_code = 47
new_touch_code = 57
touch_end_code = -1
x_move_code = 53
y_move_code = 54


async def handle_events(device):
    async for event in device.async_read_loop():
        if event.code == focused_touch_code:
            print("_____")
        elif event.code == new_touch_code:
            if event.value == touch_end_code:
                print("Touch Up")
            else:
                print("Touch Down")
        elif event.code == x_move_code:
            print("Touch X Changed")
        elif event.code == y_move_code:
            print("Touch Y Changed")


for device in [evdev.InputDevice(path) for path in evdev.list_devices()]:
    if device.name == "USBest Technology SiS HID Touch Controller":
        print("Listening to device at path: " + device.path)
        touch_screen = evdev.InputDevice(device.path)
        asyncio.ensure_future(handle_events(touch_screen))



loop = asyncio.get_event_loop()
loop.run_forever()