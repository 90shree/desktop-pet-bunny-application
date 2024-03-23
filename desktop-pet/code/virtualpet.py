import tkinter as tk
import time
import random

class Bunny:
    def __init__(self):
        self.window = tk.Tk()
        self.window.config(highlightbackground='purple')
        self.window.overrideredirect(True)
        self.window.attributes('-topmost', True)
        self.window.wm_attributes('-transparentcolor', 'purple')

        self.load_gifs()

        self.init_variables()

        self.label = tk.Label(self.window, bd=0, bg='purple')
        self.label.pack()

        self.dragging = False
        self.start_x = 0
        self.start_y = 0

        self.label.bind("<ButtonPress-1>", self.start_drag)
        self.label.bind("<B1-Motion>", self.drag)
        self.label.bind("<ButtonRelease-1>", self.release_drag)

        self.update()
        self.window.mainloop()

    def load_gifs(self):
        self.sleep = [tk.PhotoImage(file='sleep.gif', format='gif -index %i' % i) for i in range(7)]
        self.eat = [tk.PhotoImage(file='eat.gif', format='gif -index %i' % i) for i in range(14)]
        self.walk_left = [tk.PhotoImage(file='walkleft.gif', format='gif -index %i' % i) for i in range(6)]
        self.walk_right = [tk.PhotoImage(file='walkright.gif', format='gif -index %i' % i) for i in range(6)]
        self.idle = [tk.PhotoImage(file='idle.gif', format='gif -index %i' % i) for i in range(2)]
        self.idle_to_sleep = [tk.PhotoImage(file='idle_to_sleep.gif', format='gif -index %i' % i) for i in range(7)]

    def init_variables(self):
        self.current_action = None
        self.img = self.idle[0]
        self.y = self.window.winfo_screenheight() - 110
        self.x = (self.window.winfo_screenwidth() - 110) / 2
        self.vel_x = 0
        self.vel_y = 0
        self.gravity = 0.981
        self.last_action_time = time.time()
        self.last_change_time = time.time()
        self.action_duration = 0
        self.moving_back = False

    def update(self):
        self.update_movement()
        self.update_window()
        self.window.after(10, self.update)

    def update_movement(self):
        current_time = time.time()

        if current_time > self.last_change_time + 7 and not self.moving_back:
            self.last_change_time = current_time
            self.img = self.idle[0]
            self.action_duration = 7
            self.last_action_time = current_time

            if self.current_action is None or self.current_action == 'idle':
                random_action = random.randint(1, 4)
                if random_action == 1:
                    self.current_action = 'sleep'
                    self.img_sequence = self.sleep
                    self.action_duration = 7
                elif random_action == 2:
                    self.current_action = 'eat'
                    self.img_sequence = self.eat
                    self.action_duration = 8
                elif random_action == 3 or random_action == 4:
                    direction = 'walk_right' if random_action == 3 else 'walk_left'
                    self.start_walking(direction)
                    self.action_duration = 7
                time.sleep(4)

        if not self.dragging:
            self.vel_y += self.gravity
            self.y += self.vel_y

            if self.y > self.window.winfo_screenheight() - 110:
                self.y = self.window.winfo_screenheight() - 110
                self.vel_y = 0

        if hasattr(self, 'img_sequence'):
            num_frames = len(self.img_sequence)
            elapsed_time = current_time - self.last_action_time
            frame_index = int((elapsed_time / 0.1) % num_frames)
            self.img = self.img_sequence[frame_index]

            if self.current_action == 'walk_right':
                if not self.moving_back and self.x > self.window.winfo_screenwidth() - 110:
                    self.start_moving_back('left')
                else:
                    self.x += 1
            elif self.current_action == 'walk_left':
                if not self.moving_back and self.x < 0:
                    self.start_moving_back('right')
                else:
                    self.x -= 1

        if current_time > self.last_action_time + self.action_duration:
            self.current_action = None
            self.img = self.idle[0]
            self.moving_back = False

    def start_walking(self, direction):
        self.current_action = direction
        self.img_sequence = self.walk_right if direction == 'walk_right' else self.walk_left
        self.action_duration = random.randint(5, 7)

    def start_moving_back(self, direction):
        self.moving_back = True
        self.start_walking('walk_right' if direction == 'right' else 'walk_left')
        self.action_duration = 2

    def update_window(self):
        self.window.geometry('110x110+{x}+{y}'.format(x=str(int(self.x)), y=str(int(self.y))))
        self.label.configure(image=self.img)

    def start_drag(self, event):
        self.dragging = True
        self.start_x = event.x_root
        self.start_y = event.y_root

    def drag(self, event):
        if self.dragging:
            self.x = event.x_root - self.start_x + self.x
            self.y = event.y_root - self.start_y + self.y
            self.start_x = event.x_root
            self.start_y = event.y_root

    def release_drag(self, event):
        self.dragging = False

Bunny()
