from Tkinter import *
import math

# TODO Unselect object
# TODO Group objects
# TODO Ungroup objects
# TODO Change object name


def enum(**enums):
    return type('Enum', (), enums)


def dist(coord1, coord2):
    (x1, y1) = coord1
    (x2, y2) = coord2
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

class Port:
    def __init__(self, uml_object, coord):
        self.uml_object = uml_object
        self._coord = coord

    def get_coord(self):
        return self._coord

    def set_coord(self, coord):
        self._coord = coord

    def update_coord(self):
        self.uml_object.update_coords()


class Line:
    def __init__(self, canvas,
                 start_port, end_port,
                 arrow=NONE, arrow_shape=(8, 10, 3)):
        self.item = None
        self.canvas = canvas
        self.start_port = start_port
        self.end_port = end_port
        self.arrow = arrow
        self.arrow_shape = arrow_shape
        self.draw()

    def draw(self):
        if hasattr(self, 'item') and type(self.item) is not None:
            self.canvas.delete(self.item)
        self.start_port.update_coord()
        self.end_port.update_coord()
        (start_x, start_y) = self.start_port.get_coord()
        (end_x, end_y) = self.end_port.get_coord()
        self.item = self.canvas.create_line(
                start_x, start_y,
                end_x, end_y,
                arrowshape=self.arrow_shape,
                arrow=self.arrow,
                tags="line"
            )


class UmlObject:
    def __init__(self, canvas, widget, uml_pair):
        self._center = self._top = self._bottom = self._left = self._right = None
        self.focus_point = []
        self.canvas = canvas
        self.widget = widget
        self.uml_pair = uml_pair
        self.uml_pair[self.widget] = self
        self.create_ports()

    def create_ports(self):
        bound = self.canvas.bbox(self.widget)
        self._center = Port(self, ((bound[2]+bound[0])/2, (bound[3]+bound[1])/2))
        self._top = Port(self, ((bound[2]+bound[0])/2, bound[1]))
        self._bottom = Port(self, ((bound[2]+bound[0])/2, bound[3]))
        self._left = Port(self, (bound[0], (bound[1]+bound[3])/2))
        self._right = Port(self, (bound[2], (bound[1]+bound[3])/2))
        self.focus_point = [self._center, self._top, self._bottom, self._left, self._right]

    def update_coords(self):
        bound = self.canvas.bbox(self.widget)
        self._center.set_coord(((bound[2]+bound[0])/2, (bound[3]+bound[1])/2))
        self._top.set_coord(((bound[2]+bound[0])/2, bound[1]))
        self._bottom.set_coord(((bound[2]+bound[0])/2, bound[3]))
        self._left.set_coord((bound[0], (bound[1]+bound[3])/2))
        self._right.set_coord((bound[2], (bound[1]+bound[3])/2))

    def get_nearest_port(self, coord):
        nearest_port = self._center
        nearest_dist = dist(self._center.get_coord(), coord)
        for port in self.focus_point:
            tmp_dist = dist(port.get_coord(), coord)
            if tmp_dist < nearest_dist:
                nearest_dist = tmp_dist
                nearest_port = port
        return nearest_port


class GUIMain(Frame):
    def __init__(self, master=None):
        self.uml_object_list = []
        self.uml_line_list = []
        self.uml_pair = {}
        Frame.__init__(self, master)
        self.grid()
        self.create_widgets()
        self.mode = None
        self.arrow_type = NONE

    def select_mode(self):
        print 'SELECT mode'
        self.mode = None

    def create_association_line(self):
        print 'LINE mode'
        self.mode = "line"
        self.arrow_type = NONE

    def create_generalization_line(self):
        print 'LINE mode'
        self.mode = "line"
        self.arrow_type = LAST

    def on_background_click(self, event):
        self.canvas.delete('focusPoint')

    def on_canvas_click(self, event):
        print 'onCanvasClick', event.x, event.y, event.widget
        self.mode = None

    def _add_focus_point(self, selected_item):
        self.canvas.delete("focusPoint")
        bound = self.canvas.bbox(selected_item)
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

    def on_token_button_press(self, event):
        print 'onTokenButtonPress', event.x, event.y, event.widget
        find_closest_list = self.canvas.find_closest(event.x, event.y)
        closest_uml = self.uml_pair[find_closest_list[0]]
        self._drag_data["item"] = find_closest_list[0]
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y
        self._drag_data["start_port"] = closest_uml.get_nearest_port((event.x, event.y))
        self._add_focus_point(self._drag_data["item"])
        if self.mode == "line":
            for i in range(len(find_closest_list)):
                if self.canvas.gettags(find_closest_list[i]) == "focusPoint":
                    self._drag_data["item"] = find_closest_list[i]
                    bound = find_closest_list[i]
                    self._drag_data["x"] = (bound[2] + bound[0])/2
                    self._drag_data["y"] = (bound[3] + bound[1])/2
                    break

    def on_token_button_release(self, event):
        print 'onTokenButtonRelease', event.x, event.y, event.widget
        if self.mode == "line":
            closest_item = self.canvas.find_closest(event.x, event.y)[0]
            start_port = self._drag_data["start_port"]
            end_port = self.uml_pair[closest_item].get_nearest_port((event.x, event.y))
            self.uml_line_list.append(Line(self.canvas, start_port, end_port))
        self._drag_data["item"] = None
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0
        for i in self.uml_line_list:
            i.draw()

    def on_token_motion(self, event):
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
            for i in self.uml_line_list:
                i.draw()

    def _create_token(self, coord, length=100, fill="black", outline="#000000", tags="token"):
        (x, y) = coord
        return self.canvas.create_rectangle(
            x, y,
            x+length, y+length,
            fill=fill,
            outline=outline,
            tags=tags
        )

    def _create_circle_token(self, coord, length=100, fill="black", outline="#000000", tags="token"):
        (x, y) = coord
        return self.canvas.create_oval(
            x, y,
            x+length, y+length,
            fill=fill,
            outline=outline,
            tags=tags
        )

    def create_widgets(self):
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

        self.select = Button(self, command=self.select_mode)
        self.select["text"] = "Select"
        self.select["width"] = 15
        self.select.grid(row=0, column=0)
        self.associationLine = Button(self, command=self.create_association_line)
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

        self.canvas.create_rectangle(0, 0, 800, 600, fill='#FFF', outline='#FFF', tags='background')

        token_01 = UmlObject(self.canvas, self._create_token((10, 10), fill="yellow"), self.uml_pair)
        token_02 = UmlObject(self.canvas, self._create_token((110, 110), fill="red"), self.uml_pair)
        token_03 = UmlObject(self.canvas, self._create_token((210, 210), fill="green"), self.uml_pair)
        token_04 = UmlObject(self.canvas, self._create_circle_token((310, 310), fill="blue"), self.uml_pair)
        line_01 = Line(self.canvas, token_01._bottom, token_02._left)
        line_02 = Line(self.canvas, token_02._bottom, token_03._left, arrow_shape=(16, 8, 6), arrow=LAST)
        line_03 = Line(self.canvas, token_03._bottom, token_04._left)
        line_04 = Line(self.canvas, token_04._bottom, token_01._left)
        self.uml_object_list.append(token_01)
        self.uml_object_list.append(token_02)
        self.uml_object_list.append(token_03)
        self.uml_object_list.append(token_04)
        self.uml_line_list.append(line_01)
        self.uml_line_list.append(line_02)
        self.uml_line_list.append(line_03)
        self.uml_line_list.append(line_04)

        self.canvas.tag_bind('token', '<ButtonPress-1>', self.on_token_button_press)
        self.canvas.tag_bind('token', '<ButtonRelease-1>', self.on_token_button_release)
        self.canvas.tag_bind('token', '<B1-Motion>', self.on_token_motion)
        self.canvas.tag_bind('background', '<Button-1>', )

if __name__ == '__main__':
    root = Tk()
    app = GUIMain(master=root)
    app.mainloop()
