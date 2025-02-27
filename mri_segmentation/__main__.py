import os
os.environ["TOTALSEG_HOME_DIR"] = os.path.join(os.getcwd(), ".totalsegmentator")
print(os.environ["TOTALSEG_HOME_DIR"])

import tkinter as tk
from tkinter import ttk

from .app import App
from .menu import MenuBar
from .state import app_state

root = tk.Tk()
root.title("MRI Segmentation")
root.bind("<Key-q>", lambda _: exit(0))
root.columnconfigure(0, weight=1, minsize=768)
root.rowconfigure(0, weight=1, minsize=768)

style = ttk.Style()
style.theme_use("clam")

menu_bar = MenuBar(root)

app = App(root)
app.grid(row=0, column=0, sticky="nswe")

# root.after(100, lambda: app_state.mri_dir.set("data/mr_orig/"))

root.mainloop()
