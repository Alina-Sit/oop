from point import Point2D
from line import Line2D
from rectangle import Rectangle2D
from elipse import Ellipse2D
from line_circles import LineWithCircles
from cube import CubeShape

N = 128

SHAPES = [
    ("point", "Крапка", Point2D),
    ("line", "Лінія", Line2D),
    ("rectangle", "Прямокутник", Rectangle2D),
    ("ellipse", "Еліпс", Ellipse2D),
    ("line_circles", "Лінія з кружечками", LineWithCircles),
    ("cube", "Каркас куба", CubeShape),
]


class MyEditor:
    def __init__(self):
        self.pcshape = [None] * N
        self.count = 0
        self.classes = {key: cls for key, _, cls in SHAPES}
        self.current_key = "rectangle"
        self.current_shape = None

    def set_type(self, key):
        self.current_key = key

    def is_full(self):
        return self.count >= N

    def on_lbdown(self, x, y):
        if self.is_full():
            return False
        self.current_shape = self.classes[self.current_key]()
        self.current_shape.set_start((x, y))
        return True

    def on_mouse_move(self, canvas, x, y):
        if self.current_shape:
            self.current_shape.show_rubber(canvas, (x, y))

    def on_lbup(self, canvas, x, y):
        if not self.current_shape:
            return
        canvas.delete("rubber")
        self.current_shape.set_end((x, y))
        self.current_shape.show(canvas)
        self.pcshape[self.count] = self.current_shape
        self.count += 1
        self.current_shape = None

    def clear(self):
        self.pcshape = [None] * N
        self.count = 0
        self.current_shape = None

    def repaint(self, canvas):
        canvas.delete("all")
        for shape in self.pcshape[:self.count]:
            shape.show(canvas)
