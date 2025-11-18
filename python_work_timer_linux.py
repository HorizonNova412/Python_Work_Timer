import tkinter as tk
from tkinter import messagebox
import time
from datetime import datetime
import os

class WorkTimer:
    """Customizable timer application with work/pause intervals."""
    def __init__(self, root):
        """Initialize the timer GUI and default settings."""
        self.root = root
        self.root.title("Work Timer")
        self.root.geometry("270x365")
        self.root.resizable(False, False)
        self.root.attributes('-topmost', True)
        self.root.configure(bg='#222222')

        # Configuration frame for time inputs
        config_frame = tk.Frame(root, bg='#222222')
        config_frame.pack(pady=5)

        # Work time input
        tk.Label(
            config_frame,
            text="Work (min):",
            fg='white',
            bg='#222222',
            anchor="w"
        ).grid(row=0, column=0, padx=3, sticky="w")
        self.work_entry = tk.Entry(
            config_frame,
            width=5,
            fg='white',
            bg='#333333',
            justify="center"
        )
        self.work_entry.grid(row=0, column=1, padx=3, sticky="w")
        self.work_entry.insert(0, "25")

        # Pause time input
        tk.Label(
            config_frame,
            text="Pause (min):",
            fg='white',
            bg='#222222',
            anchor="w"
        ).grid(row=1, column=0, padx=3, sticky="w")
        self.pause_entry = tk.Entry(
            config_frame,
            width=5,
            fg='white',
            bg='#333333',
            justify="center"
        )
        self.pause_entry.grid(row=1, column=1, padx=3, sticky="w")
        self.pause_entry.insert(0, "5")

        # Long pause time input
        tk.Label(
            config_frame,
            text="Long pause (min):",
            fg='white',
            bg='#222222',
            anchor="w"
        ).grid(row=2, column=0, padx=3, sticky="w")
        self.long_pause_entry = tk.Entry(
            config_frame,
            width=5,
            fg='white',
            bg='#333333',
            justify="center"
        )
        self.long_pause_entry.grid(row=2, column=1, padx=3)
        self.long_pause_entry.insert(0, "30")

        # Cycle until long pause input
        tk.Label(
            config_frame,
            text="Cycles until long pause:",
            fg='white',
            bg='#222222',
            anchor="w"
        ).grid(row=3, column=0, padx=3, sticky="w")
        self.cylce_entry = tk.Entry(
            config_frame,
            width=5,
            fg='white',
            bg='#333333',
            justify="center"
        )
        self.cylce_entry.grid(row=3, column=1, padx=3)
        self.cylce_entry.insert(0, "4")

        # Timer display
        self.label = tk.Label(
            root,
            text="00:00",
            font=("Arial", 30),
            fg='#FFD700',
            bg='#222222'
        )
        self.label.pack(pady=10)

        # Mode display
        self.mode_label = tk.Label(
            root,
            text="Mode: Work",
            font=("Arial", 12),
            fg='white',
            bg='#222222'
        )
        self.mode_label.pack(pady=5)

        # Cycle counter display
        self.cycle_label = tk.Label(
            root,
            text="Cycle: 1",
            font=("Arial", 12),
            fg='white',
            bg='#222222'
        )
        self.cycle_label.pack(pady=5)

        # Button frame
        button_frame = tk.Frame(root, bg='#222222')
        button_frame.pack(pady=10)

        # Control buttons
        self.start_button = tk.Button(
            button_frame,
            text="Start",
            command=self.start_timer,
            width=5,
            fg='white',
            bg='#333333'
        )
        self.start_button.pack(side=tk.LEFT, padx=3)

        self.stop_button = tk.Button(
            button_frame,
            text="Stop",
            command=self.stop_timer,
            state=tk.DISABLED,
            width=5,
            fg='white',
            bg='#333333'
        )
        self.stop_button.pack(side=tk.LEFT, padx=3)

        self.reset_button = tk.Button(
            button_frame,
            text="Reset",
            command=self.reset_timer,
            width=5,
            fg='white',
            bg='#333333'
        )
        self.reset_button.pack(side=tk.LEFT, padx=5)

        # Real-time clock label at the bottom (smaller font)
        self.clock_label = tk.Label(
            root,
            text="",
            font=("Arial", 10),
            fg='#888888',
            bg='#222222'
        )
        self.clock_label.pack(side=tk.BOTTOM, pady=5)
        self.update_clock()  # Start clock updates

        # Timer state variables
        self.remaining_time = 0
        self.is_work_time = True
        self.timer_running = False
        self.cycle_counter = 1
        self.update_durations()

    def update_clock(self):
        """Update the real-time clock display (HH:MM)."""
        now = datetime.now().strftime("%H:%M")
        self.clock_label.config(text=now)
        self.root.after(60000, self.update_clock)

    def start_timer(self):
        """Start the timer with current settings."""
        if not self.timer_running:
            if self.remaining_time <= 0:
                messagebox.showerror("Error", "Please enter valid durations!")
                return
            self.timer_running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.update_timer()

    def update_durations(self):
        """Update timer durations from entry fields."""
        try:
            self.get_durations()
            if self.is_work_time:
                self.remaining_time = self.work_min * 60
            elif self.cycle_counter % self.cycle_until_long_pause == 0:
                self.remaining_time = self.long_pause_min * 60
            else:
                self.remaining_time = self.pause_min * 60
            mins, _ = divmod(self.remaining_time, 60)
            self.label.config(text=f"{mins:02d}:00")
            return True
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers!")
            return False
        
    def get_durations(self):
        self.work_min = int(self.work_entry.get())
        self.pause_min = int(self.pause_entry.get())
        self.long_pause_min = int(self.long_pause_entry.get())
        self.cycle_until_long_pause = int(self.cylce_entry.get())

    def stop_timer(self):
        """Stop the timer and reset button states."""
        self.timer_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def reset_timer(self):
        """Reset timer to initial state with current settings."""
        self.stop_timer()
        self.update_durations()
        self.cycle_counter = 1
        self.cycle_label.config(text=f"Cycle: {self.cycle_counter}")
        self.mode_label.config(text=f"Mode: Work")

    def gentle_beep(self):
        """Play a sound file using aplay."""
        sound_file = "/usr/share/sounds/sound-icons/prompt.wav"
        for _ in range(6):
            os.system(f"aplay {sound_file}")
            time.sleep(1)
            # print("beep")

    def update_timer(self):
        """Update timer display and handle time transitions."""
        if self.timer_running:
            mins, secs = divmod(self.remaining_time, 60)
            self.label.config(text=f"{mins:02d}:{secs:02d}")
            self.remaining_time -= 1
            if self.remaining_time <= 0:
                if self.is_work_time == False:
                    self.cycle_counter += 1
                    self.cycle_label.config(text=f"Cycle: {self.cycle_counter}")
                self.gentle_beep()
                self.is_work_time = not self.is_work_time
                self.update_durations()
                mins, secs = divmod(self.remaining_time, 60)
                mode = "Work" if self.is_work_time else "Pause"
                self.mode_label.config(text=f"Mode: {mode}")
                messagebox.showinfo(
                    mode,
                    f"Switched to {mode} time!\nRemaining:"
                    f"{mins:02d}:{secs:02d}"
                )
            self.root.after(1000, self.update_timer)

if __name__ == "__main__":
    root = tk.Tk()
    app = WorkTimer(root)
    root.mainloop()
