# -*- coding: utf-8 -*-

#┌──────────────────────────────────────────────────────────
#│ Name     : joss_tk.py
#│ Libraly  : Tkinter, Pillow, screeninfo
#│ Function : Screen saver module for Windows 11
#└──────────────────────────────────────────────────────────

import ctypes
import random
import sys
import random
import tkinter as tk
from pathlib import Path

from PIL import Image, ImageTk
from screeninfo import get_monitors


def resource_path(relative_path):
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent / relative_path
    return Path(__file__).parent / relative_path

# ==============================
# 設定
# ==============================
#IMAGE_DIR = Path(__file__).parent / "./images"
                                            # ┌───────────────────────────────────
IMAGE_DIR = resource_path("scr_images")     # │ <=== 表示画像格納ディレクトリ
                                            # │      scriptのカレントに置くこと
                                            # └───────────────────────────────────

ACTIVE_MONITOR_INDEX = 1       # jonesyを表示するモニタ。0=メイン, 1=サブ
SLIDE_INTERVAL_MS = 8000
RANDOM_SLIDE = True
RANDOM_MONITOR_MODE = True

FADE_MOVE = True
FADE_STEPS = 12
FADE_DELAY_MS = 25

BACKGROUND_COLOR = "#000000"

# 非表示モニタのグレーアウト設定
GRAY_COLOR = "#202020"
GRAY_ALPHA = 0.95              # 0.0透明 ～ 1.0不透明

# 復帰条件
EXIT_ON_MOUSE_MOVE = True
MOUSE_MOVE_THRESHOLD = 30

# 復帰時にWindowsロック
LOCK_ON_EXIT = True


class GrayOverlay:
    def __init__(self, monitor):
        self.win = tk.Toplevel()
        self.win.overrideredirect(True)
        self.win.attributes("-topmost", True)
        self.win.attributes("-alpha", GRAY_ALPHA)
        self.win.configure(bg=GRAY_COLOR)

        self.win.geometry(
            f"{monitor.width}x{monitor.height}+{monitor.x}+{monitor.y}"
        )

        label = tk.Label(
            self.win,
            text="",
            bg=GRAY_COLOR,
            fg="#808080",
            font=("Meiryo UI", 24, "bold")
        )
        label.pack(fill="both", expand=True)

    def destroy(self):
        self.win.destroy()

class MonitorWindow:
    def __init__(self, root, monitor):
        self.monitor = monitor
        self.win = tk.Toplevel(root)
        self.win.overrideredirect(True)
        self.win.attributes("-topmost", True)
        self.win.attributes("-alpha", 1.0)
        self.win.configure(bg=GRAY_COLOR)
        self.win.geometry(
            f"{monitor.width}x{monitor.height}+{monitor.x}+{monitor.y}"
        )

        self.label = tk.Label(self.win, bg=GRAY_COLOR)
        self.label.pack(fill="both", expand=True)

        self.image_ref = None

    def make_gray_canvas(self):
        return Image.new("RGB", (self.monitor.width, self.monitor.height), GRAY_COLOR)

    def show_gray(self):
        # 透明にしない。完全なグレー窓で覆う
        self.win.attributes("-alpha", 1.0)

        canvas = self.make_gray_canvas()
        self.image_ref = ImageTk.PhotoImage(canvas)
        self.label.configure(image=self.image_ref, bg=GRAY_COLOR)
        self.win.configure(bg=GRAY_COLOR)
        self.win.lift()

    def make_image_canvas(self, image_path):
        img = Image.open(image_path).convert("RGB")

        sw = self.monitor.width
        sh = self.monitor.height

        screen_ratio = sw / sh
        img_ratio = img.width / img.height

        if img_ratio > screen_ratio:
            new_w = sw
            new_h = int(sw / img_ratio)
        else:
            new_h = sh
            new_w = int(sh * img_ratio)

        img = img.resize((new_w, new_h), Image.LANCZOS)

        canvas = Image.new("RGB", (sw, sh), BACKGROUND_COLOR)
        x = (sw - new_w) // 2
        y = (sh - new_h) // 2
        canvas.paste(img, (x, y))

        return canvas

    def show_image(self, image_path):
        # 透明化しない。常に画面を覆ったままにする
        self.win.attributes("-alpha", 1.0)
        self.win.lift()

        gray_canvas = self.make_gray_canvas()
        image_canvas = self.make_image_canvas(image_path)

        if FADE_MOVE:
            for i in range(FADE_STEPS + 1):
                t = i / FADE_STEPS
                frame = Image.blend(gray_canvas, image_canvas, t)
                self.image_ref = ImageTk.PhotoImage(frame)
                self.label.configure(image=self.image_ref, bg=BACKGROUND_COLOR)
                self.win.update_idletasks()
                self.win.after(FADE_DELAY_MS)
        else:
            self.image_ref = ImageTk.PhotoImage(image_canvas)
            self.label.configure(image=self.image_ref, bg=BACKGROUND_COLOR)

        self.win.configure(bg=BACKGROUND_COLOR)

    def bind_events(self, callback):
        self.win.bind("<Escape>", callback)
        self.win.bind("<Button>", callback)
        self.win.bind("<Key>", callback)
        self.win.bind("<Motion>", callback)


class JonesyScreenSaver:
    def __init__(self):
        self.monitors = get_monitors()

        if not self.monitors:
            raise RuntimeError("モニタ情報を取得できませんでした。")

        self.image_paths = self.load_images()
        self.current_index = 0
        self.start_mouse_pos = None

        self.root = tk.Tk()
        self.root.withdraw()

        self.windows = []
        for mon in self.monitors:
            mw = MonitorWindow(self.root, mon)
            mw.bind_events(self.on_any_event)
            self.windows.append(mw)

        self.active_index = random.randint(0, len(self.monitors) - 1)

        self.show_next_image()
        self.root.mainloop()

    def load_images(self):
        if not IMAGE_DIR.exists():
            raise FileNotFoundError(f"imagesフォルダがありません: {IMAGE_DIR}")

        exts = ["*.png", "*.jpg", "*.jpeg", "*.webp", "*.bmp"]
        files = []

        for ext in exts:
            files.extend(IMAGE_DIR.glob(ext))

        files = sorted(files)

        if not files:
            raise FileNotFoundError(f"画像ファイルがありません: {IMAGE_DIR}")

        return files

    def choose_next_monitor(self):
        if RANDOM_MONITOR_MODE and len(self.windows) >= 2:
            while True:
                new_index = random.randint(0, len(self.windows) - 1)
                if new_index != self.active_index:
                    return new_index

        return min(ACTIVE_MONITOR_INDEX, len(self.windows) - 1)

    def choose_next_image(self):
        if RANDOM_SLIDE:
            return random.choice(self.image_paths)

        image_path = self.image_paths[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.image_paths)
        return image_path

    def show_next_image(self):
        self.active_index = self.choose_next_monitor()
        image_path = self.choose_next_image()

        # まず全モニタをグレーアウト
        for i, win in enumerate(self.windows):
            if i != self.active_index:
                win.show_gray()

        self.root.update_idletasks()

        # 最後に対象モニタだけ画像表示
        self.windows[self.active_index].show_image(image_path)

        self.root.after(SLIDE_INTERVAL_MS, self.show_next_image)

    def on_any_event(self, event=None):
        if event and event.type.name == "Motion":
            if not EXIT_ON_MOUSE_MOVE:
                return

            if self.start_mouse_pos is None:
                self.start_mouse_pos = (event.x_root, event.y_root)
                return

            dx = abs(event.x_root - self.start_mouse_pos[0])
            dy = abs(event.y_root - self.start_mouse_pos[1])

            if dx <= MOUSE_MOVE_THRESHOLD and dy <= MOUSE_MOVE_THRESHOLD:
                return

        self.exit_app()

    def exit_app(self):
        for win in self.windows:
            try:
                win.win.destroy()
            except tk.TclError:
                pass

        self.root.destroy()

        if LOCK_ON_EXIT:
            ctypes.windll.user32.LockWorkStation()

        sys.exit(0)


if __name__ == "__main__":
    args = [a.lower() for a in sys.argv[1:]]

    if "/c" in args:
        sys.exit(0)   # 設定画面は今回は無し

    if "/p" in args:
        sys.exit(0)   # プレビューは今回は無し

    JonesyScreenSaver()
