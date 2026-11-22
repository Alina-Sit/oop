from .base import Shape, register


@register("point", "Крапка", order=10)
class Point2D(Shape):
    RADIUS = 3

    def show_rubber(self, canvas, current_point, tag="rubber"):
        canvas.delete(tag)

    def bbox(self):
        x, y = self.end if self.end else self.start
        r = self.RADIUS
        return x - r, y - r, x + r, y + r

    def show(self, canvas):
        x1, y1, x2, y2 = self.bbox()
        canvas.create_oval(x1, y1, x2, y2, outline="black", fill="black")
