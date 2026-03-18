# 🦊 Kitsubi Autoklicker PRO
# ======================================
# Advanced AutoClicker + AimBot + Pixel Detection + Overlay
# Ready for GitHub Upload

# =========================
# 📦 REQUIREMENTS
# =========================
# pip install pyautogui pynput pillow

import pyautogui
import time
import threading
import random
import tkinter as tk
from pynput import mouse
from PIL import Image

pyautogui.FAILSAFE = True
APP_NAME = "Kitsubi Autoklicker 🦊 PRO"

# =========================
# 🧠 AIMBOT CORE
# =========================
class AimBot:
    def __init__(self):
        self.region = None
        self.target_color = None
        self.running = False
        self.ignore_margin = 20  # UI Rand ignorieren

    def pick_color(self):
        x, y = pyautogui.position()
        self.target_color = pyautogui.screenshot().getpixel((x, y))
        print("🎯 Ziel-Farbe:", self.target_color)

    def select_region(self):
        print("Ziehe Bereich...")
        start = [0, 0]

        def on_click(x, y, button, pressed):
            if pressed:
                start[0], start[1] = x, y
            else:
                self.region = (
                    min(start[0], x),
                    min(start[1], y),
                    abs(x - start[0]),
                    abs(y - start[1])
                )
                print("📦 Region:", self.region)
                return False

        with mouse.Listener(on_click=on_click) as listener:
            listener.join()

    def find_target(self):
        if not self.region or not self.target_color:
            return None

        img = pyautogui.screenshot(region=self.region)
        pixels = img.load()

        w, h = img.size

        for x in range(self.ignore_margin, w - self.ignore_margin):
            for y in range(self.ignore_margin, h - self.ignore_margin):
                if pixels[x, y] == self.target_color:
                    return (self.region[0] + x, self.region[1] + y)

        return None

    def smooth_aim(self, x, y):
        cx, cy = pyautogui.position()
        steps = random.randint(3, 8)

        for i in range(steps):
            nx = cx + (x - cx) * (i + 1) / steps
            ny = cy + (y - cy) * (i + 1) / steps
            pyautogui.moveTo(nx, ny)
            time.sleep(0.001)

    def run(self):
        def loop():
            self.running = True
            print("▶ AIM gestartet")
            while self.running:
                target = self.find_target()
                if target:
                    self.smooth_aim(*target)
                    pyautogui.click()
                time.sleep(0.01)
            print("⏹ AIM gestoppt")

        threading.Thread(target=loop, daemon=True).start()

    def stop(self):
        self.running = False


bot = AimBot()

# =========================
# 🖥 GUI
# =========================
root = tk.Tk()
root.title(APP_NAME)
root.geometry("500x400")
root.configure(bg="#0a0f2c")

frame = tk.Frame(root, bg="#0a0f2c")
frame.pack(pady=10)

logo = tk.Label(frame, text="🦊", font=("Arial", 40), fg="#4da6ff", bg="#0a0f2c")
logo.pack()


def styled(text, cmd):
    return tk.Button(frame, text=text, command=cmd, width=30,
                     bg="#1a2b6d", fg="white", activebackground="#4da6ff")

styled("🎯 Farbe wählen", bot.pick_color).pack(pady=5)
styled("📦 Bereich wählen", bot.select_region).pack(pady=5)
styled("▶ AIM START", bot.run).pack(pady=5)
styled("⏹ STOP", bot.stop).pack(pady=5)

# =========================
# 🖊 OVERLAY
# =========================
overlay = tk.Toplevel(root)
overlay.geometry("140x50+10+10")
overlay.attributes("-topmost", True)
overlay.attributes("-alpha", 0.5)
overlay.configure(bg="black")

label = tk.Label(overlay, text="🦊 PRO AIM", fg="#4da6ff", bg="black")
label.pack()

# =========================
# ▶ START
# =========================
print(f"{APP_NAME} gestartet")
root.mainloop()

# =========================
# 📦 BUILD EXE
# =========================
# pip install pyinstaller
# pyinstaller --onefile --noconsole --name "Kitsubi_Autoklicker_PRO" main.py

# =========================
# 📄 README (für GitHub)
# =========================
# Kitsubi Autoklicker PRO 🦊
#
# Features:
# - Auto Aim (Farb-Erkennung)
# - Bereichsauswahl
# - Smooth Mouse Movement
# - Overlay UI
# - Low CPU Nutzung
#
# Usage:
# 1. Farbe wählen
# 2. Bereich markieren
# 3. AIM starten
#
# Hinweis:
# Funktioniert am besten mit stabilen Farben ohne starke Effekte
