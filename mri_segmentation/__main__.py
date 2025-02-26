import os
os.environ["TOTALSEG_HOME_DIR"] = os.path.join(os.getcwd(), ".totalsegmentator")
print(os.environ["TOTALSEG_HOME_DIR"])

import tkinter as tk
from tkinter import ttk

from .app import App
from .state import AppState

#TODO:
#  * Basteln einer GUI
#    * SliceView von MR inkl. Maske
#    * Button, um das automatische durchlaufen der Slices zu aktivieren
#  * Öffnen von einem Bild als Dicom über einen Ordner
#  * Anwendung von TotalSegmentator ohne Zwischenzugriff auf GUI

root = tk.Tk()
root.title("MRI Segmentation")
root.bind("<Key-q>", lambda _: exit(0))
root.columnconfigure(0, weight=1, minsize=768)
root.rowconfigure(0, weight=1, minsize=768)

style = ttk.Style()
style.theme_use("clam")

state = AppState()

app = App(root, state)
app.grid(row=0, column=0, sticky="nswe")

root.mainloop()
