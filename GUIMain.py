from Tkinter import *

class GUIMain(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
        self.mode = None

    def selectMode(self):
        print 'SELECT mode'
        self.mode = None

    def createAssociationLine(self):
        print 'LINE mode'
        self.mode = "line"

    def onCanvasClick(self, event):
        print 'onCanvasClick', event.x, event.y, event.widget
        self.mode = None

    def _add_focus_point(self, selectedItem):
        self.canvas.delete("focusPoint")
        bound = self.canvas.bbox(selectedItem)
        width = bound[2] - bound[0]
        height = bound[3] - bound[1]
        top = (bound[0] + width/2 - 3, bound[3])
        bottom = (bound[0] + width/2 - 3, bound[1]-6)
        left = (bound[0]-6, bound[1] + height/2 - 3)
        right = (bound[2], bound[1] + height/2 - 3)
        self._create_token(top, fill="black", tags="focusPoint", length=6)
        self._create_token(bottom, fill="black", tags="focusPoint", length=6)
        self._create_token(left, fill="black", tags="focusPoint", length=6)
        self._create_token(right, fill="black", tags="focusPoint", length=6)

    def onTokenButtonPress(self, event):
        print 'onTokenButtonPress', event.x, event.y, event.widget
        find_closest_list = self.canvas.find_closest(event.x, event.y)
        self._drag_data["item"] = find_closest_list[0]
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y
        self._add_focus_point(self._drag_data["item"])
        if self.mode == "line":
            for i in range(len(find_closest_list)):
                if self.canvas.gettags(find_closest_list[i]) == "focusPoint":
                    self._drag_data["item"] = find_closest_list[i]
                    bound = find_closest_list[i]
                    self._drag_data["x"] = (bound[2] + bound[0])/2
                    self._drag_data["y"] = (bound[3] + bound[1])/2
                    break


    def onTokenButtonRelease(self, event):
        print 'onTokenButtonRelease', event.x, event.y, event.widget
        if self.mode == "line":
            closest_item = self.canvas.find_closest(event.x, event.y)[0]
            bound = self.canvas.bbox(closest_item)
            (end_point_x, end_point_y) = ((bound[2] + bound[0])/2, (bound[3] + bound[1])/2)
            print 'LINE: (%d, %d) to (%d, %d)' % (
                self._drag_data["x"],
                self._drag_data["y"],
                end_point_x,
                end_point_y)
            self.canvas.create_line(
                self._drag_data["x"], 
                self._drag_data["y"],
                end_point_x,
                end_point_y,
                arrowshape=(8, 10, 3),
                arrow=LAST,
                tags="arrow"
            )
        self._drag_data["item"] = None
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0

    def onTokenMotion(self, event):
        print 'onTokenMotion', event.x, event.y, event.widget
        delta_x = event.x - self._drag_data["x"]
        delta_y = event.y - self._drag_data["y"]
        if self.mode == "line":
            print "LINE mode, no object moved."
        else:
            self.canvas.move("focusPoint", delta_x, delta_y)
            self.canvas.move(self._drag_data["item"], delta_x, delta_y)
            self._drag_data["x"] = event.x
            self._drag_data["y"] = event.y

    def _create_token(self, coord, length=100, fill="black", outline="#000000", tags="token"):
        (x, y) = coord
        self.canvas.create_rectangle(
            x, y,
            x+length, y+length,
            fill=fill,
            outline=outline,
            tags=tags
        )

    def _create_circle_token(self, coord, length=100, fill="black", outline="#000000", tags="token"):
        (x, y) = coord
        self.canvas.create_oval(
            x, y,
            x+length, y+length,
            fill=fill,
            outline=outline,
            tags=tags
        )

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

        self.select = Button(self, command=self.selectMode)
        self.select["text"] = "Select"
        self.select["width"] = 15
        self.select.grid(row=0, column=0)
        self.associationLine = Button(self, command=self.createAssociationLine)
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
        self._create_token((10, 10), fill="yellow")
        self._create_token((110, 110), fill="red")
        self._create_token((210, 210), fill="green")
        self._create_circle_token((310, 310), fill="blue")

        self.canvas.tag_bind('token', '<ButtonPress-1>', self.onTokenButtonPress)
        self.canvas.tag_bind('token', '<ButtonRelease-1>', self.onTokenButtonRelease)
        self.canvas.tag_bind('token', '<B1-Motion>', self.onTokenMotion)

if __name__ == '__main__':
    root = Tk()
    app = GUIMain(master=root)
    app.mainloop()
