import tkinter as tk
from tkinter import colorchooser, simpledialog, messagebox
import random as r

def is_hex(str):
    try:
        int(str, 16)
        return True
    except:
        return False

class Rectangle:
    def __init__(self, x1: int, y1: int, x2: int, y2: int, id: int, color: str):        
        if color[0] != '#' or len(color) != 7 or not is_hex(color[1:]):
            raise ValueError("Rectangle.color must be in the folowing format: #XXXXXX (X = hex-digit)")

        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.id = id
        self.color = color

        # TODO Implement ability to change rect color
        #def change_color(self):

class Layer:
    def __init__(self, name: str, bg_color: str="#FFFFFF", layer_hidden: bool=False):
        if bg_color[0] != '#' or len(bg_color) != 7 or not is_hex(bg_color[1:]):
            raise ValueError("Rectangle.color must be in the folowing format: #XXXXXX (X = hex-digit)")
        
        self.name = name
        self.bg_color = bg_color
        self.text_color = "black" if not layer_hidden else "lightgrey"
        self.layer_hidden = layer_hidden

        self.rects = {}

    def toggle_hide(self):
        self.text_color = "black" if self.layer_hidden else "lightgrey"
        self.layer_hidden = not self.layer_hidden

    def text_colors(self):
        return (self.text_color,self.bg_color)
    
    def is_hidden(self):
        return self.layer_hidden
    
    def rect_exists(self, x: int, y: int):
        id  = None
        for rect in self.rects.values():
            in_x = (x >= rect.x1 and x <= rect.x2)
            in_y = (y >= rect.y1 and y <= rect.y2)
            if in_x and in_y:
                id = rect.id
        return id

    def add_rect(self, x1: int, y1: int, x2: int, y2: int, id: int):
        rect = Rectangle(x1,y1,x2,y2,id,self.bg_color)
        self.rects.update({id : rect})

    def del_rect(self, id: int):
        del self.rects[id]

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

    # TODO Implement ability to change canvas rect color as well
    def change_layer_color(self):
        # Ask for desired color
        idx = self.layer_menu_idx
        layer = self.list.get(idx)
        rgb, bg_color = colorchooser.askcolor(title=f"Select Color for {layer}")

        # change layer color
        self.list.itemconfig(idx,bg=bg_color)
        self.layers[layer].bg_color = bg_color

        # change layers geometry color too
        rect_ids = list(self.layers[layer].rects.keys())
        for id in rect_ids:
            self.root.itemconfigure(id,fill=bg_color)
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
            # add renamed entry
            self.add_layer(idx,new_name,bg_color,hidden_status)
            # move rects to new layer entry
            self.layers[new_name].rects = self.layers[old_name].rects
            # delete old entry
            del self.layers[old_name]
            self.list.delete(idx+1)
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
        # delete what is selected or by idx?
        end_idx = self.list.index(tk.END)
        if del_cursor:
            try: idx = self.list.curselection()[0]
            except: idx = None

        if idx == None:
            # nothing to delete... do nothing
            return True
        
        # delete the target layer (and its associated geometry)
        layer = self.list.get(idx)
        if idx >= 0 and idx <= end_idx and layer != "":
            rect_ids = list(self.layers[layer].rects.keys())
            if len(rect_ids) > 0:
                response = messagebox.askquestion("Deleting Layer","Are you sure you want to delete this populated layer?")
                if response == "no":
                    return
            for id in rect_ids:
                self.root.delete(id)
            del self.layers[layer]
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

        # hide/reveal any rectangles in the layer
        rect_ids = list(self.layers[layer].rects.keys())
        layer_state = "hidden" if self.layers[layer].is_hidden() else "normal"
        for id in rect_ids:
            self.root.itemconfigure(id,state=layer_state)
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

class Window:
    def __init__(self):
        # instantiate main window
        self.root = tk.Tk()
        self.root.title("Photolithography Tool")
        self.root.geometry("1000x600")
        self.root.minsize(500,500)

        # window icon
        self.logo = tk.PhotoImage(file='img/burger.png')
        self.root.iconphoto(False, self.logo)

        # populate main window
        self.menubar = MenuBar(self.root)
        self.canvas = tk.Canvas(self.root,width=800,height=600,bg="white")
        self.layersbar = LayersBar(self.canvas)
        self.canvas.bind("<Button>",self.canvas_click)
        self.canvas.pack(fill="both",expand=True)

        # variables for control
        self.B1_clicked = False
        self.B1_click_x = 0
        self.B1_click_y = 0

    def mainloop(self):
        self.root.mainloop()

    def create_rect(self, layer: str, x1: int, y1: int, x2: int, y2: int, color: str):
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1

        id = self.canvas.create_rectangle(x1,y1,
                                          x2,y2,
                                          fill=color,
                                          outline="black")
        self.layersbar.layers[layer].add_rect(x1,y1,
                                              x2,y2,
                                              id)
        
    def delete_rect(self, layer: str, x: int, y: int):
        rect_id = self.layersbar.layers[layer].rect_exists(x,y)
        if rect_id != None:
            self.canvas.delete(rect_id)
            self.layersbar.layers[layer].del_rect(rect_id)

    def canvas_click(self, event):
        try: layer_idx = self.layersbar.list.curselection()[0]
        except: return # if no layer is selected, do nothing

        layer = self.layersbar.list.get(layer_idx)
        layer_color = self.layersbar.list.itemcget(layer_idx,"bg")

        if event.num == 1: # If it was a left click...
            if self.B1_clicked == False:
                self.B1_click_x = event.x
                self.B1_click_y = event.y
                self.B1_clicked = True
            else:
                self.create_rect(layer,
                                 self.B1_click_x,
                                 self.B1_click_y,
                                 event.x,
                                 event.y,
                                 layer_color)
                self.B1_clicked = False
        elif event.num == 3: # Else if it was a right click...
            self.B1_clicked = False
            self.delete_rect(layer,event.x,event.y)
