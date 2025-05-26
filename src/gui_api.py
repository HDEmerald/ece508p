import tkinter as tk
from tkinter import colorchooser, simpledialog, messagebox
import random as r

class Layer:
    def __init__(self, name: str, bg_color: str="#FFFFFF", layer_hidden: bool=False):
        self.name = name
        self.bg_color = bg_color
        self.text_color = "black" if not layer_hidden else "lightgrey"
        self.layer_hidden = layer_hidden

    def toggle_hide(self):
        self.text_color = "black" if self.layer_hidden else "lightgrey"
        self.layer_hidden = not self.layer_hidden

    def text_colors(self):
        return (self.text_color,self.bg_color)
    
    def is_hidden(self):
        return self.layer_hidden

class LayersBar:
    def __init__(self, root):
        self.layers = {}
        self.curr_idx = None
        self.layer_menu_idx = -1

        self.root = root
        self.frame = tk.Frame(root)

        # layer list header
        self.header = tk.Frame(self.frame)
        self.label = tk.Label(self.header,text="Layers",justify='left')
        self.label.pack(side=tk.LEFT)
        self.del_button = tk.Button(self.header,text="-",width=1,height=1,
                                    command=self.delete_layer)
        self.del_button.pack(side=tk.LEFT,anchor=tk.W)
        self.add_button = tk.Button(self.header,text="+",width=1,height=1,
                                    command=self.add_layer)
        self.add_button.pack(side=tk.LEFT,anchor=tk.W)
        self.hide_button = tk.Button(self.header,text="H",width=1,height=1,
                                     command=self.hide_layer)
        self.hide_button.pack(side=tk.LEFT,anchor=tk.W)
        self.header.pack()

        # list body/scroll bar
        self.scroll = tk.Scrollbar(self.frame,orient=tk.VERTICAL)
        self.list = tk.Listbox(self.frame,yscrollcommand=self.scroll.set,selectmode=tk.SINGLE,
                               activestyle='underline')
        self.list.bind("<Button-1>",self.sel_layer)
        self.list.bind("<B1-Motion>",self.drag_layer)
        self.scroll.config(command=self.list.yview)
        self.scroll.pack(side=tk.RIGHT,fill=tk.Y)
        self.list.pack(side=tk.RIGHT,fill=tk.Y)

        # right-click layer menu
        self.layer_menu = tk.Menu(self.frame,tearoff=False)
        self.layer_menu.add_command(label="Change Color",command=self.change_layer_color)
        self.layer_menu.add_command(label="Rename Layer",command=self.change_layer_name)
        self.list.bind("<Button-3>",self.show_layer_menu)

        self.frame.pack(side=tk.RIGHT,fill=tk.Y)

    def sel_layer(self, event):
        self.curr_idx = self.list.nearest(event.y)

    def drag_layer(self, event):
        idx = self.list.nearest(event.y)
        layer = self.list.get(idx)
        text_colors = self.layers[layer].text_colors()
        if idx < self.curr_idx:
            self.list.delete(idx)
            self.list.insert(idx+1,layer)
            self.list.itemconfig(idx+1,fg=text_colors[0],bg=text_colors[1])
        elif idx > self.curr_idx:
            self.list.delete(idx)
            self.list.insert(idx-1,layer)
            self.list.itemconfig(idx-1,fg=text_colors[0],bg=text_colors[1])

        self.curr_idx = idx

    def show_layer_menu(self, event):
        self.layer_menu_idx = self.list.nearest(event.y)
        if self.layer_menu_idx != -1:
            self.layer_menu.tk_popup(event.x_root,event.y_root)
            return True
        else:
            return False

    def change_layer_color(self):
        idx = self.layer_menu_idx
        layer = self.list.get(idx)
        rgb, bg_color = colorchooser.askcolor(title=f"Select Color for {layer}")
        self.list.itemconfig(idx,bg=bg_color)
        self.layers[layer].bg_color = bg_color
        return True

    def change_layer_name(self):
        idx = self.layer_menu_idx
        old_name = self.list.get(idx)
        bg_color = self.list.itemcget(idx,"background")
        hidden_status = self.layers[old_name].is_hidden()

        new_name = simpledialog.askstring("Input", f"New name for {old_name}")

        if new_name in self.list.get(0,tk.END) and new_name != old_name:
            messagebox.showerror("Layer Rename Error","Error: Layer name already exists!")
            return False
        elif new_name is not None:
            # delete old entry
            del self.layers[old_name]
            self.list.delete(idx)
            # add renamed entry
            if self.add_layer(idx,new_name,bg_color,hidden_status):
                return True
        else:
            # simply no change to layer name
            return True

    def rand_color(self):
        # create a random color hexcode (6-hexadecimal digits)
        color = hex(r.randint(0,0xFFFFFF)).replace("0x","")
        while len(color) < 6:
            color = "0" + color
        return "#" + color

    def delete_layer(self, idx: int=-1, del_cursor: bool=True):
        # if a layer is selected, delete it
        end_idx = self.list.index(tk.END)
        if del_cursor:
            try: idx = self.list.curselection()[0]
            except: idx = None

        if idx == None:
            # nothing to delete... do nothing
            return True
        
        name = self.list.get(idx)
        if idx >= 0 and idx <= end_idx and name != "":
            del self.layers[name]
            self.list.delete(idx)
        elif idx < 0 or idx > end_idx:
            print(f"Error: Invalid idx in LayersBar.delete_layer()... idx = {idx} last index = {end_idx}")
            return False
        else:
            print(f"Error: Empty name in LayersBar.delete_layer()...")
            return False

    
    def add_layer(self, idx=-1, name: str="", bg_color: str="", hidden_status: bool=False):
        # make sure layer name is not taken
        end_idx = self.list.index(tk.END)
        if name == "":
            temp_idx = 0
            name = f"Layer{temp_idx}"
            while name in self.list.get(0,tk.END):
                temp_idx += 1
                name = f"Layer{temp_idx}"

        # assign a random color if none given
        if bg_color == "":
            bg_color = self.rand_color()

        # put layer in the right place
        if idx == -1:
            idx = end_idx
            self.list.insert(tk.END, name)
            self.list.itemconfig(tk.END,bg=bg_color)
            new_layer = Layer(name,bg_color,hidden_status)
            self.layers.update({name : new_layer})
        elif idx >= 0 and idx <= end_idx:
            self.list.insert(idx, name)
            for i,j in enumerate(self.list.get(0,tk.END)): 
                if j == name: 
                    idx = i
                    break
            self.list.itemconfig(idx,bg=bg_color)
            new_layer = Layer(name,bg_color,hidden_status)
            self.layers.update({name : new_layer})
        else:
            print(f"Error: Invalid idx in LayersBar.add_layer()... idx = {idx}")
            return False

        # make sure layer hidden status aligns with text color
        if hidden_status == True:
            self.list.itemconfig(idx,fg="lightgrey")

        return True

    # TODO Add layer hiding functionality
    def hide_layer(self):
        # if a layer is not selected, exit with no changes
        idx = self.list.curselection()
        if not idx:
            return False
        
        # toggle layer to be hidden/shown
        layer = self.list.get(idx)
        self.layers[layer].toggle_hide()
        text_color = self.layers[layer].text_colors()[0]
        self.list.itemconfig(idx,fg=text_color)
        return True

class MenuBar:
    def __init__(self, root):
        self.root = root
        self.menu = tk.Menu(root,relief=tk.FLAT,bg="white")
        self.root.config(menu=self.menu)
        
        # TODO Add functionality for File sub-menus
        # file sub-menu
        self.file = tk.Menu(self.menu,tearoff=0,relief=tk.RAISED)
        self.menu.add_cascade(label="File",menu=self.file)
        self.file.add_command(label="Open") #,command=openFile)
        self.file.add_command(label="Save")
        self.file.add_separator()
        self.file.add_command(label="Exit",command=quit)

        # TODO Add Edit sub-menus
        # TODO Add functionality for Edit sub-menus
        # edit sub-menu
        self.edit = tk.Menu(self.menu,tearoff=0,relief=tk.RAISED)
        self.menu.add_cascade(label="Edit",menu=self.edit)

        # TODO Add View sub-menus
        # TODO Add functionality for View sub-menus
        # view sub-menu
        self.view = tk.Menu(self.menu,tearoff=0,relief=tk.RAISED)
        self.menu.add_cascade(label="View",menu=self.view)