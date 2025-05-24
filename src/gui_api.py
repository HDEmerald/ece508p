import tkinter as tk

class LayersBar:
    def __init__(self, root):
        self.curr_idx = None
        self.layer_hidden = {}

        self.root = root
        self.frame = tk.Frame(root)

        # layer list header
        self.header = tk.Frame(self.frame)
        self.label = tk.Label(self.header,text="Layers",justify='left')
        self.label.pack(side=tk.LEFT)
        self.del_button = tk.Button(self.header,text="-",width=1,height=1,command=self.delete)
        self.del_button.pack(side=tk.LEFT,anchor=tk.W)
        self.add_button = tk.Button(self.header,text="+",width=1,height=1,command=self.add)
        self.add_button.pack(side=tk.LEFT,anchor=tk.W)
        self.hide_button = tk.Button(self.header,text="H",width=1,height=1,command=self.hide)
        self.hide_button.pack(side=tk.LEFT,anchor=tk.W)
        self.header.pack()

        # TODO Add checkboxs for each layer
        # list body/scroll bar
        self.scroll = tk.Scrollbar(self.frame,orient=tk.VERTICAL)
        self.list = tk.Listbox(self.frame,yscrollcommand=self.scroll.set,selectmode=tk.SINGLE)
        self.list.bind("<Button-1>",self.sel_item)
        self.list.bind("<B1-Motion>",self.drag_item)
        self.scroll.config(command=self.list.yview)
        self.scroll.pack(side=tk.RIGHT,fill=tk.Y)
        self.list.pack(side=tk.RIGHT,fill=tk.Y)

        self.frame.pack(side=tk.RIGHT,fill=tk.Y)

    def sel_item(self, event):
        self.curr_idx = self.list.nearest(event.y)

    def drag_item(self, event):
        idx = self.list.nearest(event.y)
        if idx < self.curr_idx:
            x = self.list.get(idx)
            self.list.delete(idx)
            self.list.insert(idx+1, x)
            self.curr_idx = idx
        elif idx > self.curr_idx:
            x = self.list.get(idx)
            self.list.delete(idx)
            self.list.insert(idx-1, x)
            self.curr_idx = idx

    def delete(self):
        idx = self.list.index(tk.ANCHOR)
        del self.layer_hidden[self.list.get(idx)]
        self.list.delete(tk.ANCHOR)
    
    def add(self):
        end_idx = self.list.index(tk.END)
        self.list.insert(tk.END, f"Layer{end_idx}")
        self.layer_hidden.update({self.list.get(tk.END) : False})

    # TODO Add layer hiding functionality
    def hide(self):
        layer = self.list.get(tk.ANCHOR)
        if not self.layer_hidden[layer]:
            self.layer_hidden[layer] = True
            self.list.itemconfig(tk.ANCHOR,foreground="lightgrey")
        else:
            self.layer_hidden[layer] = False
            self.list.itemconfig(tk.ANCHOR,foreground="black")

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