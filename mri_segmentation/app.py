import tkinter as tk
from tkinter import ttk
import threading
import time

from reacTk.widget.label import Label, LabelState
from reacTk.widget.canvas import Canvas, CanvasState
from reacTk.widget.canvas.image import Image, ImageState
from widget_state import NumberState, ObjectState, StringState

from .scale import Scale, ScaleState
from .state import AppState


class SliceScale(ttk.Frame):

    def __init__(
        self, parent: tk.Widget, slice: NumberState, image: ObjectState
    ) -> None:
        super().__init__(parent)

        self.slice = slice
        self.image = image
        self.timeout = 0.1

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=4)
        self.rowconfigure(0, weight=1)

        self.button = ttk.Button(self, command=self.on_button, text="Start")
        self.button.grid(row=0, column=0, sticky="e")

        self.scale = Scale(
            self,
            ScaleState(
                self.slice,
                min_value=0,
                max_value=1,
                length=368,
                orientation="horizontal",
            ),
        )
        self.scale.grid(row=0, column=1)
        self.image.on_change(
            lambda _: self.scale.state.max.set(self.image.value.shape[0] - 1),
            trigger=True
        )

        self.run_loop = False
        self.loop_thread: threading.Thread = None
        self.on_button()

        self.scale.scale.config(command=self.on_scale)

    def on_scale(self, *_):
        # Stop loop if the scale is controlled manually
        self.run_loop = False
        self.loop_thread = None

    def on_button(self):
        self.run_loop = not self.run_loop
        self.button.config(text="Stop" if self.run_loop else "Start")
        if self.run_loop and self.loop_thread is None:
            self.loop_thread = threading.Thread(target=self.loop)
            self.loop_thread.start()
        else:
            self.run_loop = False
            self.loop_thread = None

    def loop(self):
        while self.run_loop:
            try:
                self.after(
                    0,
                    lambda: self.slice.set(
                        (self.slice.value + 1) % self.image.value.shape[0]
                    ),
                )
            except RuntimeError:
                break
            time.sleep(self.timeout)


class App(ttk.Frame):

    def __init__(self, parent: tk.Widget, state: AppState) -> None:
        super().__init__(parent)

        self.state = state

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=7)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(1, weight=1)

        self.canvas = Canvas(self, CanvasState())
        self.canvas.grid(column=0, row=0, sticky="nswe")
        self.image = Image(self.canvas, ImageState(self.state.slice_image))

        self.slice_scale = SliceScale(self, self.state.slice, self.state.mri)
        self.slice_scale.grid(column=0, row=1, sticky="nswe")


        self.label_state = StringState("")
        self.state.volume.on_change(lambda _: self.label_state.set(f"Liver volume: {self.state.volume.value:.3f} Liter"), trigger=True) 
        self.volume_label = Label(self, self.label_state)
        self.volume_label.grid(column=0, row=2)
