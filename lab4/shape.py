from abc import ABC, abstractmethod


class Shape(ABC):
    RUBBER_COLOR = "black"
    RUBBER_DASH = (4, 2)

    def __init__(self):
        self.start = None
        self.end = None

    def set_start(self, point):
        self.start = point

    def set_end(self, point):
        self.end = point

    @abstractmethod
    def show(self, canvas):
        raise NotImplementedError

    def show_rubber(self, canvas, current_point, tag="rubber"):
        canvas.delete(tag)
        if self.start:
            canvas.create_line(
                self.start[0], self.start[1],
                current_point[0], current_point[1],
                fill=self.RUBBER_COLOR, dash=self.RUBBER_DASH, tags=tag
            )

    def _show_part(self, part_class, start, end, canvas):
        saved = (self.start, self.end)
        self.start, self.end = start, end
        try:
            part_class.show(self, canvas)
        finally:
            self.start, self.end = saved
