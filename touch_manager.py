from touch import Touch

update_threshold = 5

class TouchManager(object):

    # A dictionary of the current touches on the screen. Indexed by their given focused_index from the Planar screen.
    active_touches = {}

    # The index of the currently focused touch provided by the Planar screen.
    focused_touch_index = 0

    def __init__(self, socket_connection):
        self.socket_connection = socket_connection

    def handle_touch_down(self, touch_event):
        touch_id = int(touch_event.value)
        self.active_touches[self.focused_touch_index] = Touch(touch_id)

    def handle_touch_up(self):
        if self.focused_touch_code >= len(active_touches):
            return
            
        current_touch = self.active_touches.pop(self.focused_touch_index)
        if current_touch.is_ready():
            self.socket_connection.send_touch_up(current_touch)

    def handle_move_x(self, touch_event):
        if self.focused_touch_code >= len(active_touches):
            return

        current_touch = self.active_touches[self.focused_touch_index]
        x_value = int(touch_event.value)

        if current_touch.needs_x():
            current_touch.xPos = x_value
            if current_touch.is_ready():
                self.socket_connection.send_touch_down(current_touch)

        elif current_touch.is_ready() and abs(current_touch.xPos - x_value) >= update_threshold:
            current_touch.xPos = x_value
            self.socket_connection.send_touch_moved(current_touch)

    def handle_move_y(self, touch_event):
        if self.focused_touch_code >= len(active_touches):
            return

        current_touch = self.active_touches[self.focused_touch_index]
        y_value = int(touch_event.value)

        if current_touch.needs_y():
            current_touch.yPos = y_value
            if current_touch.is_ready():
                self.socket_connection.send_touch_down(current_touch)

        elif current_touch.is_ready() and abs(current_touch.yPos - y_value) >= update_threshold:
            current_touch.yPos = y_value
            self.socket_connection.send_touch_moved(current_touch)

    def finish(self):
        self.socket_connection.close_connection()
