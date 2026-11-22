from abc import ABC, abstractmethod

_registry = {}


def register(key, name, order=100):
    def wrap(cls):
        cls.KEY = key
        cls.NAME = name
        cls.ORDER = order
        _registry[key] = cls
        return cls
    return wrap


def registered():
    return sorted(_registry.values(), key=lambda c: c.ORDER)


def create(key):
    return _registry[key]()


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

    def bbox(self):
        x1, x2 = sorted((self.start[0], self.end[0]))
        y1, y2 = sorted((self.start[1], self.end[1]))
        return x1, y1, x2, y2

    def to_record(self):
        return (self.KEY, self.start[0], self.start[1], self.end[0], self.end[1])

    def _show_part(self, part_class, start, end, canvas):
        saved = (self.start, self.end)
        self.start, self.end = start, end
        try:
            part_class.show(self, canvas)
        finally:
            self.start, self.end = saved
