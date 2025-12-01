import tkinter as tk
from tkinter import messagebox
import threading
import time
import os
import sys
import queue 

# --- 1. SECURITY MODULES ---
try:
    import keyboard 
    from pynput import mouse
except ImportError:
    print("⚠️ Security modules missing. Run: pip install keyboard pynput")
    keyboard = None
    mouse = None

# --- 2. AUDIO & GAME MODULES ---
try:
    import pygame
    pygame.mixer.init()
except ImportError:
    pygame = None

# --- CONFIGURATION ---
COLOR_BG = "#050505"
COLOR_ACCENT = "#00FFFF"
COLOR_DANGER = "#FF3333"
#User Configuration
PIN = ""#enter your pin here
THEME_MUSIC_PATH = r"" #Enter the path to your favourite music...

# --- VOICE ENGINE SETUP ---
import sounddevice as sd
try:
    sd.query_devices()
    sd.default.device = (1, None)
except Exception: pass

try:
    import pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)
    engine.setProperty('voice', engine.getProperty('voices')[0].id)
except Exception: engine = None


try:
    from advanced_verify_pass import authenticate_user as run_ath
except ImportError:
    def run_ath(): time.sleep(2); return False


speech_q = queue.Queue()

def speech_worker():
    """
    A dedicated background thread that waits for text 
    and speaks it one by one. No overlaps!
    """
    while True:
        text = speech_q.get() # Blocks until text is available
        if engine and text:
            try:
                engine.say(text)
                engine.runAndWait()
            except Exception as e:
                print(f"TTS Error: {e}")
        speech_q.task_done()

# Start the narrator thread immediately
threading.Thread(target=speech_worker, daemon=True).start()

def speak(text):
    """Adds text to the queue. Non-blocking."""
    speech_q.put(text)

# ==========================================

def play_anthem():
    if pygame and os.path.exists(THEME_MUSIC_PATH):
        try:
            pygame.mixer.music.load(THEME_MUSIC_PATH)
            pygame.mixer.music.play()
        except Exception: pass

# ==========================================
# 🛡️ SHAKTHI SECURITY CORE
# ==========================================
class SystemLockdown:
    def __init__(self):
        self.mouse_listener = None
        self.keys_blocked = False

    def lock_inputs(self):
        """Activates the digital cage."""
        if keyboard:
            try:
                keyboard.block_key('alt')
                keyboard.block_key('windows') 
                keyboard.block_key('left windows')
                keyboard.block_key('right windows')
                keyboard.block_key('tab') 
                keyboard.block_key('esc')
                self.keys_blocked = True
            except Exception: pass

        if mouse:
            self.mouse_listener = mouse.Listener(suppress=True)
            self.mouse_listener.start()

    def unlock_inputs(self):
        """Releases the digital cage."""
        if keyboard and self.keys_blocked:
            try:
                keyboard.unhook_all()
                self.keys_blocked = False
            except Exception: pass

        if self.mouse_listener:
            self.mouse_listener.stop()
            self.mouse_listener = None

security = SystemLockdown()

# --- GUI CLASS ---
class VoiceAuthGUI:
    def __init__(self, master):
        self.master = master
        master.title("Shakthi 2.0 - Biometric Gate")
        master.attributes("-fullscreen", True)
        master.configure(bg=COLOR_BG)
        master.attributes("-topmost", True)
        
        master.protocol("WM_DELETE_WINDOW", lambda: None) 
        security.lock_inputs()

        self.auth_active = True
        self.animation_running = True
        
        # UI
        self.header_frame = tk.Frame(master, bg=COLOR_BG)
        self.header_frame.pack(pady=30)
        
        tk.Label(self.header_frame, text="SHAKTHI 2.0", font=("Impact", 40), bg=COLOR_BG, fg=COLOR_ACCENT).pack()
        tk.Label(self.header_frame, text="SYSTEM LOCKED // INPUT DISABLED", font=("Consolas", 10, "bold"), bg=COLOR_BG, fg="gray").pack()

        # Canvas
        self.canvas = tk.Canvas(master, width=300, height=300, bg=COLOR_BG, highlightthickness=0)
        self.canvas.pack(pady=20)
        self.center_x, self.center_y = 150, 150
        self.pulse_radius = 50
        self.pulse_growing = True
        self.animate_arc_reactor()

        # Log
        self.log_text = tk.Label(master, text="> SECURE ENVIRONMENT", font=("Consolas", 14), bg=COLOR_BG, fg=COLOR_ACCENT)
        self.log_text.pack(pady=20)

        # PIN
        self.pin_frame = tk.Frame(master, bg=COLOR_BG)
        self.pin_frame.pack(side="bottom", pady=50)

        self.pin_entry = tk.Entry(self.pin_frame, show="•", width=10, font=("Arial", 20), justify='center', bg="#1a1a1a", fg="white", insertbackground="white")
        self.pin_entry.pack(side="left", padx=10)
        
        self.pin_entry.focus_force() 
        self.master.after(100, self.pin_entry.focus_force)

        self.pin_attempt_flag = False
        threading.Thread(target=self.auth_loop, daemon=True).start()
        self.master.bind('<Return>', self.trigger_pin_check)

    def trigger_pin_check(self, event=None):
        self.pin_attempt_flag = True

    # --- ANIMATION ---
    def animate_arc_reactor(self):
        if not self.animation_running: return
        try:
            self.canvas.delete("all")
            self.canvas.create_oval(50, 50, 250, 250, outline="#004444", width=2)
            if self.pulse_growing:
                self.pulse_radius += 2
                if self.pulse_radius > 90: self.pulse_growing = False
            else:
                self.pulse_radius -= 2
                if self.pulse_radius < 60: self.pulse_growing = True
            r = self.pulse_radius
            self.canvas.create_oval(self.center_x-r, self.center_y-r, self.center_x+r, self.center_y+r, outline=COLOR_ACCENT, width=3)
            self.canvas.create_oval(self.center_x-(r-10), self.center_y-(r-10), self.center_x+(r-10), self.center_y+(r-10), fill=COLOR_ACCENT, outline="")
            self.master.after(50, self.animate_arc_reactor)
        except tk.TclError: pass 

    def log(self, message, color=COLOR_ACCENT):
        try:
            self.log_text.config(text=f"> {message}", fg=color)
            self.master.update()
        except tk.TclError: pass

    # --- LOGIC ---
    def run_voice_auth(self):
        self.log("AUTHENTICATION REQUIRED", "yellow")
        speak("Identity verification required.")
        
        time.sleep(2.5) 
        
        self.log("LISTENING NOW...", "#00FF00")
        self.canvas.create_oval(10, 10, 290, 290, outline="red", width=5)
        self.master.update()
        
        speak("Speak now.")
        time.sleep(1.5)
        
        try: return run_ath()
        except Exception: return False

    def access_granted(self, msg="IDENTITY CONFIRMED."):
        security.unlock_inputs()
        self.auth_active = False
        self.animation_running = False
        self.canvas.delete("all")
        self.canvas.create_oval(50, 50, 250, 250, fill="#00FF00", outline="")
        self.canvas.create_text(150, 150, text="✔", font=("Arial", 60), fill="black")
        
        self.log(msg, "#00FF00")
        speak("Welcome back, Boss.")
        play_anthem()
        time.sleep(2)
        
        self.master.withdraw() 
        time.sleep(30)
        sys.exit()

    def shutdown_sequence(self):
        security.unlock_inputs()
        self.auth_active = False
        self.log("CRITICAL SECURITY VIOLATION", "white")
        speak("Unauthorized access detected. Initiating lockdown protocol.")
        
        time.sleep(5) 
        self.master.destroy()
        os.system("shutdown /s /t 1")

    def auth_loop(self):
        time.sleep(1)
        for attempt in range(2):
            if self.run_voice_auth():
                self.access_granted()
                return
            self.log(f"MATCH FAILED ({attempt+1}/2)", COLOR_DANGER)
            speak("No match found.")
            time.sleep(2)

        speak("Voice systems failing. Enter PIN.")
        time.sleep(3) 
        
        for attempt in range(3): 
            self.log(f"TYPE PIN & HIT ENTER ({attempt+1}/3)", "orange")
            self.master.after(10, lambda: self.pin_entry.focus_force())
            self.pin_entry.delete(0, tk.END)
            self.pin_attempt_flag = False
            while not self.pin_attempt_flag and self.auth_active:
                time.sleep(0.1)
            
            pin_input = self.pin_entry.get()
            if pin_input == PIN:
                self.access_granted("MANUAL OVERRIDE ACCEPTED")
                return
            else:
                self.log("INCORRECT PIN", COLOR_DANGER)
                speak("Incorrect pin.")
                time.sleep(2)
        
        self.shutdown_sequence()

if __name__ == "__main__":
    splash = tk.Tk()
    splash.overrideredirect(True)
    width = splash.winfo_screenwidth()
    height = splash.winfo_screenheight()
    splash.geometry(f"{width}x{height}")
    splash.configure(bg="black")
    tk.Label(splash, text="SHAKTHI KERNEL LOADING...", font=("Courier", 30), bg="black", fg="cyan").pack(expand=True)
    splash.after(2000, splash.destroy)
    splash.mainloop()

    root = tk.Tk()
    app = VoiceAuthGUI(root)
    root.mainloop()