import tkinter as tk
import keyboard
import time
import pyautogui
import json
import threading
import os

class App:
    def __init__(self):
        # Default configuration
        self.start_stop_key = 's'
        self.delay = 0.5
        self.running = False
        self.last_key_press_time = 0
        self.debounce_interval = 0.1  # Debounce interval in seconds

        # Load configuration
        self.load_config()

        # Create GUI window
        self.create_window()

    def load_config(self):
        try:
            with open("config.json", "r") as file:
                config_data = json.load(file)
                self.start_stop_key = config_data.get("start_stop_key", self.start_stop_key)
                self.delay = config_data.get("delay", self.delay)
        except FileNotFoundError:
            pass  # Configuration file not found, using default values

    def save_config(self):
        config_data = {
            "start_stop_key": self.start_stop_key,
            "delay": self.delay
        }
        with open("config.json", "w") as file:
            json.dump(config_data, file)

    def perform_actions(self, action):
        if action == 1:
            keyboard.press_and_release('1')
        elif action == 2:
            keyboard.press_and_release('2')
        elif action == 3:
            keyboard.press_and_release('3')
        elif action == 4:
            keyboard.press_and_release('4')
        elif action == 5:
            keyboard.press_and_release('5')
        time.sleep(0.1)
        pyautogui.click()

    def toggle_actions(self):
        self.running = not self.running
        self.start_button.config(text="Start" if not self.running else "Stop")
        if self.running:
            self.start_actions_thread = threading.Thread(target=self.start_actions)
            self.start_actions_thread.start()
        else:
            self.stop_actions()

    def start_actions(self):
        while self.running:
            for i in range(1, 6):
                if not self.running:  # Check if running becomes False
                    break  # Exit the loop if running is False
                self.perform_actions(i)
                time.sleep(self.delay)

    def stop_actions(self):
        self.running = False
        if hasattr(self, 'start_actions_thread'):
            self.start_actions_thread.join()

    def create_window(self):
        if getattr(self, 'window', None) is not None:
            return
        self.window = tk.Tk()
        self.window.title("Auto farm fruits battleground")
        self.window.geometry("300x250")
        self.window.resizable(False, False)
        self.window.configure(bg="#f0f0f0")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir, "Icons/Main.ico")
        if os.path.exists(icon_path):
            self.window.iconbitmap(icon_path)

        self.add_delay_setting()
        self.add_key_setting()
        self.add_start_button()

        # Bind start/stop key press event
        keyboard.on_press_key(self.start_stop_key, self.start_stop_key_pressed)

        # Bind window close event
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        # Bind window visibility event
        #self.window.bind("<Visibility>", self.on_visibility_change)

        # Run the GUI event loop
        self.window.mainloop()

    def on_close(self):
        self.stop_actions()
        self.window.destroy()

    def on_visibility_change(self, event):
        if event.type == tk.VisibilityNotify:
            if event.state == 1:  # Window shown
                self.stop_actions()

    def add_delay_setting(self):
        delay_label = tk.Label(self.window, text="Set delay (in seconds):", font=("Arial", 12), bg="#f0f0f0")
        delay_label.pack(pady=5)

        self.delay_entry = tk.Entry(self.window, font=("Arial", 12))
        self.delay_entry.insert(0, str(self.delay))
        self.delay_entry.pack()

    def add_key_setting(self):
        self.key_label = tk.Label(self.window, text=f"Start/stop key: {self.start_stop_key}", font=("Arial", 12), bg="#f0f0f0")
        self.key_label.pack(pady=5)

        set_key_button = tk.Button(self.window, text="Set Start/Stop Key", font=("Arial", 10), command=self.set_start_stop_key)
        set_key_button.pack(pady=5)

    def set_start_stop_key(self):
        self.key_label.config(text="Press a key to set start/stop key:")
        keyboard.unhook_key(self.start_stop_key)
        if self.running:
            self.stop_actions()
        self.window.bind("<Key>", self.set_start_stop_key_pressed)

    def set_start_stop_key_pressed(self, event):
        self.start_stop_key = event.keysym
        self.key_label.config(text=f"Start/stop key: {self.start_stop_key}")
        self.save_config()
        keyboard.on_press_key(self.start_stop_key, self.start_stop_key_pressed)
        self.window.unbind("<Key>")


    def start_stop_key_pressed(self, _event=None):  # Ignore the event argument
        self.toggle_actions()

    def add_start_button(self):
        self.start_button = tk.Button(self.window, text="Start", font=("Arial", 12), command=self.start_stop_key_pressed)
        self.start_button.pack(pady=5)

if __name__ == "__main__":
    # Start the program by creating the app
    app = App()
