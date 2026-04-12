"""
Temporizador Pomodoro sencillo con Tkinter.
25 min de trabajo + 5 min de descanso, con botones Start y Reset.
"""

import tkinter as tk
from tkinter import ttk

WORK_SECS = 25 * 60
BREAK_SECS = 5 * 60


class PomodoroApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Pomodoro Day58")
        self.root.resizable(False, False)

        self.state = "listo"  # "trabajo", "descanso"
        self.remaining = WORK_SECS
        self.timer_id: str | None = None

        self.build_ui()
        self.update_display()

    def build_ui(self) -> None:
        main = ttk.Frame(self.root, padding=20)
        main.grid()

        self.status_var = tk.StringVar(value="Listo para trabajar")
        self.time_var = tk.StringVar()

        ttk.Label(main, textvariable=self.status_var, font=("Segoe UI", 12, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(0, 10)
        )
        ttk.Label(main, textvariable=self.time_var, font=("Consolas", 28, "bold")).grid(
            row=1, column=0, columnspan=2, pady=(0, 15)
        )

        start_btn = ttk.Button(main, text="Start", command=self.start)
        reset_btn = ttk.Button(main, text="Reset", command=self.reset)
        start_btn.grid(row=2, column=0, padx=5, ipadx=10)
        reset_btn.grid(row=2, column=1, padx=5, ipadx=10)

    def start(self) -> None:
        # Si ya hay temporizador corriendo, no iniciar otro.
        if self.timer_id:
            return
        self.state = "trabajo"
        self.remaining = WORK_SECS
        self.tick()

    def reset(self) -> None:
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        self.state = "listo"
        self.remaining = WORK_SECS
        self.status_var.set("Listo para trabajar")
        self.update_display()

    def tick(self) -> None:
        mins, secs = divmod(self.remaining, 60)
        self.time_var.set(f"{mins:02d}:{secs:02d}")

        if self.remaining == 0:
            self.swap_phase()
            return

        self.remaining -= 1
        self.timer_id = self.root.after(1000, self.tick)

    def swap_phase(self) -> None:
        # Cambia entre trabajo y descanso, reanuda automaticamente.
        if self.state == "trabajo":
            self.state = "descanso"
            self.remaining = BREAK_SECS
            self.status_var.set("Descanso: 5 minutos")
        else:
            self.state = "trabajo"
            self.remaining = WORK_SECS
            self.status_var.set("Trabajo: 25 minutos")
        self.timer_id = None
        self.tick()

    def update_display(self) -> None:
        mins, secs = divmod(self.remaining, 60)
        self.time_var.set(f"{mins:02d}:{secs:02d}")


def main() -> None:
    root = tk.Tk()
    PomodoroApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
