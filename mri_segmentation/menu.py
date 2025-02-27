"""
Components of the menu bar.
"""

import os
import tkinter as tk
from tkinter import filedialog

import SimpleITK as sitk

from .state import app_state, AppState
from .util import read_image


class MenuBar(tk.Menu):
    """
    Menu bar of the app.
    """

    def __init__(self, root: tk.Tk):
        super().__init__(root)

        root.option_add("*tearOff", False)
        root["menu"] = self

        self.menu_file = MenuFile(self, root)


class MenuFile(tk.Menu):
    """
    The File menu containing options to
      * open an image
      * save the current state
      * restore the state
    """

    def __init__(self, menu_bar: tk.Menu, root: tk.Tk):
        super().__init__(menu_bar)

        menu_bar.add_cascade(menu=self, label="File")

        # add commands
        self.add_command(label="Open", command=self.open)
        self.add_command(label="Load Segmentation", command=self.load_segmentation)
        self.add_command(label="Save Segmentation", command=self.save_segmentation)

    def open(self):
        dirname = filedialog.askdirectory()
        if not dirname:
            return

        app_state.mri_dir.set(dirname)

    def load_segmentation(self):
        filename = filedialog.askopenfilename()
        if not filename:
            return

        sitk_mask = read_image(filename)
        app_state.sitk_mask.set(sitk_mask)

    def save_segmentation(self):
        filename = filedialog.asksaveasfilename()
        if not filename:
            return

        filename, _ = os.path.splitext(filename)
        filename = filename + ".nii.gz"
        sitk.WriteImage(app_state.sitk_mask.value, filename)
