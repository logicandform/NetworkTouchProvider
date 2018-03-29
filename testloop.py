import asyncio
import evdev

screen1 = evdev.InputDevice('/dev/input/event1')
screen2 = evdev.InputDevice('/dev/input/event3')

async def capture_events(device):
    async for event in device.async_read_loop():
        print(device.fn, evdev.categorize(event), sep=': ')

for device in screen1, screen2:
    asyncio.ensure_future(capture_events(device))

loop = asyncio.get_event_loop()
loop.run_forever()
