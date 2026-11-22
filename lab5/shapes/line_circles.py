from .base import register
from .line import Line2D
from .elipse import Ellipse2D


@register("line_circles", "Лінія з кружечками", order=50)
class LineWithCircles(Line2D, Ellipse2D):
    LINE_COLOR = "navy"
    ELLIPSE_OUTLINE = "navy"
    ELLIPSE_FILL = "orange"
    CIRCLE_RADIUS = 8

    def bbox(self):
        r = self.CIRCLE_RADIUS
        x1, x2 = sorted((self.start[0], self.end[0]))
        y1, y2 = sorted((self.start[1], self.end[1]))
        return x1 - r, y1 - r, x2 + r, y2 + r

    def show_rubber(self, canvas, current_point, tag="rubber"):
        canvas.delete(tag)
        if not self.start:
            return
        r = self.CIRCLE_RADIUS
        canvas.create_line(
            self.start[0], self.start[1], current_point[0], current_point[1],
            fill=self.RUBBER_COLOR, dash=self.RUBBER_DASH, tags=tag
        )
        for cx, cy in (self.start, current_point):
            canvas.create_oval(
                cx - r, cy - r, cx + r, cy + r,
                outline=self.RUBBER_COLOR, dash=self.RUBBER_DASH, tags=tag
            )

    def show(self, canvas):
        r = self.CIRCLE_RADIUS
        Line2D.show(self, canvas)
        for cx, cy in (self.start, self.end):
            self._show_part(Ellipse2D, (cx, cy), (cx + r, cy + r), canvas)
