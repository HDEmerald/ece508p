import tkinter as tk
from PIL import Image, ImageTk

# main window
root = tk.Tk()
root.title('Photolithography Tool')
root.geometry("720x640")

# window icon
logo = tk.PhotoImage(file='img/burger.png')
root.iconphoto(False, logo)

canvas = tk.Canvas(root, width=500, height=500, bg="white")
#canvas.grid(columnspan=3, rowspan=3)
#canvas.pack(padx=20, pady=20)

btn = tk.Button(root, text="Button")
btn.grid(row=0, column=0)

root.mainloop()