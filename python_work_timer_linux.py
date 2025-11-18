import tkinter as tk
from tkinter import messagebox
import time
from datetime import datetime
import os


class TimerApp:
    """Customizable timer application with work/pause intervals."""
    def __init__(self, root):
        """Initialize the timer GUI and default settings."""
        self.root = root
        self.root.title("Timer")
        self.root.geometry("330x220")
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
            bg='#222222'
        ).grid(row=0, column=0, padx=3)
        self.work_entry = tk.Entry(
            config_frame,
            width=5,
            fg='white',
            bg='#333333'
        )
        self.work_entry.grid(row=0, column=1, padx=3)
        self.work_entry.insert(0, "25")

        # Pause time input
        tk.Label(
            config_frame,
            text="Pause (min):",
            fg='white',
            bg='#222222'
        ).grid(row=0, column=2, padx=3)
        self.pause_entry = tk.Entry(
            config_frame,
            width=5,
            fg='white',
            bg='#333333'
        )
        self.pause_entry.grid(row=0, column=3, padx=3)
        self.pause_entry.insert(0, "5")

        # Timer display
        self.label = tk.Label(
            root,
            text="25:00",
            font=("Arial", 30),
            fg='white',
            bg='#222222'
        )
        self.label.pack(pady=5)

        # Button frame
        button_frame = tk.Frame(root, bg='#222222')
        button_frame.pack(pady=2)

        # Control buttons
        self.start_button = tk.Button(
            button_frame,
            text="Start",
            command=self.start_timer,
            width=6,
            fg='white',
            bg='#333333'
        )
        self.start_button.pack(side=tk.LEFT, padx=3)

        self.stop_button = tk.Button(
            button_frame,
            text="Stop",
            command=self.stop_timer,
            state=tk.DISABLED,
            width=6,
            fg='white',
            bg='#333333'
        )
        self.stop_button.pack(side=tk.LEFT, padx=3)

        self.reset_button = tk.Button(
            root,
            text="Reset",
            command=self.reset_timer,
            width=6,
            fg='white',
            bg='#333333'
        )
        self.reset_button.pack(pady=1)

        # Real-time clock label at the bottom (smaller font)
        self.clock_label = tk.Label(
            root,
            text="",
            font=("Arial", 10),
            fg='#888888',
            bg='#222222'
        )
        self.clock_label.pack(side=tk.BOTTOM, pady=2)
        self.update_clock()  # Start clock updates

        # Timer state variables
        self.remaining_time = 0
        self.is_work_time = True
        self.timer_running = False
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
            work_min = int(self.work_entry.get())
            pause_min = int(self.pause_entry.get())
            self.remaining_time = (work_min * 60
                                  if self.is_work_time
                                  else pause_min * 60)
            mins, _ = divmod(self.remaining_time, 60)
            self.label.config(text=f"{mins:02d}:00")
            return True
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers!")
            return False

    def stop_timer(self):
        """Stop the timer and reset button states."""
        self.timer_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def reset_timer(self):
        """Reset timer to initial state with current settings."""
        self.stop_timer()
        self.update_durations()

    def gentle_beep(self):
        """Play a sound file using aplay."""
        sound_file = "/usr/share/sounds/sound-icons/prompt.wav"
        for _ in range(6):
            os.system(f"aplay {sound_file}")
            time.sleep(1)

    def update_timer(self):
        """Update timer display and handle time transitions."""
        if self.timer_running:
            mins, secs = divmod(self.remaining_time, 60)
            self.label.config(text=f"{mins:02d}:{secs:02d}")
            self.remaining_time -= 1
            if self.remaining_time < 0:
                self.gentle_beep()
                self.is_work_time = not self.is_work_time
                self.update_durations()
                mins, secs = divmod(self.remaining_time, 60)
                mode = "Work" if self.is_work_time else "Pause"
                messagebox.showinfo(
                    mode,
                    f"Switched to {mode} time!\nRemaining: {mins:02d}:{secs:02d}"
                )
            self.root.after(1000, self.update_timer)

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
