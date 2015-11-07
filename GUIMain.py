from Tkinter import *

class GUIMain(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def onCanvasClick(event):
        print 'Got canvas click', event.x, event.y, event.widget

    def onObjectClick(event):
        print 'Got object click', event.x, event.y, event.widget

    def onTokenClick(event):
        print 'onTokenClick', event.x, event.y, event.widget

    def onTokenButtonPress(self, event):
        print 'onTokenButtonPress', event.x, event.y, event.widget
        self._drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def onTokenButtonRelease(self, event):
        print 'onTokenButtonRelease', event.x, event.y, event.widget
        self._drag_data["item"] = None
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0

    def onTokenMotion(self, event):
        print 'onTokenMotion', event.x, event.y, event.widget
        delta_x = event.x - self._drag_data["x"]
        delta_y = event.y - self._drag_data["y"]
        self.canvas.move(self._drag_data["item"], delta_x, delta_y)
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def _create_token(self, coord, fill, outline = "#000000"):
        (x, y) = coord
        self.canvas.create_rectangle(x, y, x+20, y+20, fill=fill, outline=outline, tags="token")

    def createWidgets(self):
        self.menubar = Menu(self)
        self.master.config(menu=self.menubar)

        self.fileMenubar = Menu(self.menubar, tearoff=0)
        self.fileMenubar.add_command(label="New")
        self.fileMenubar.add_command(label="Open")
        self.fileMenubar.add_command(label="Save")
        self.fileMenubar.add_command(label="Save As...")
        self.menubar.add_cascade(label="File", menu=self.fileMenubar)

        self.editMenubar = Menu(self.menubar, tearoff=0)
        self.editMenubar.add_command(label="Group")
        self.editMenubar.add_command(label="Ungroup")
        self.editMenubar.add_command(label="Rename")
        self.menubar.add_cascade(label="Edit", menu=self.editMenubar)

        self.select = Button(self)
        self.select["text"] = "Select"
        self.select["width"] = 15
        self.select.grid(row=0, column=0)
        self.associationLine = Button(self)
        self.associationLine["text"] = "Association Line"
        self.associationLine["width"] = 15
        self.associationLine.grid(row=1, column=0)
        self.generalizationLine = Button(self)
        self.generalizationLine["text"] = "Generalization Line"
        self.generalizationLine["width"] = 15
        self.generalizationLine.grid(row=2, column=0)
        self.compositionLine = Button(self)
        self.compositionLine["text"] = "Composition Line"
        self.compositionLine["width"] = 15
        self.compositionLine.grid(row=3, column=0)
        self.classGraph = Button(self)
        self.classGraph["text"] = "Class"
        self.classGraph["width"] = 15
        self.classGraph.grid(row=4, column=0)
        self.useCase = Button(self)
        self.useCase["text"] = "Use Case"
        self.useCase["width"] = 15
        self.useCase.grid(row=5, column=0)

        self._drag_data = {"x": 0, "y": 0, "item": None}
        self.canvas = Canvas(self, width=800, height=600)
        self.canvas.pack(fill='both', expand=True)
        self.canvas.grid(row=0, column=1, columnspan=7, rowspan=6)
        self._create_token((50, 20), fill="yellow")
        self._create_token((70, 40), fill="red")
        self._create_token((90, 60), fill="green")

        self.canvas.tag_bind('token', '<Button-1>', self.onTokenClick)
        self.canvas.tag_bind('token', '<ButtonPress-1>', self.onTokenButtonPress)
        self.canvas.tag_bind('token', '<ButtonRelease-1>', self.onTokenButtonRelease)
        self.canvas.tag_bind('token', '<B1-Motion>', self.onTokenMotion)
        
if __name__ == '__main__':
    root = Tk()
    app = GUIMain(master=root)
    app.mainloop()
