from gui_api import *
import tkinter as tk

# instantiate main window
root = tk.Tk()
root.title('Photolithography Tool')
root.geometry("720x640")
root.minsize(500,500)

# window icon
logo = tk.PhotoImage(file='img/burger.png')
root.iconphoto(False, logo)

# populate main window
Menu = MenuBar(root)
Canvas = tk.Canvas(root,width=500,height=500,bg="white")
Canvas.pack(fill="both",expand=True)
Layers = LayersBar(Canvas)

root.mainloop()