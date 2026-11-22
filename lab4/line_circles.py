from line import Line2D
from elipse import Ellipse2D


class LineWithCircles(Line2D, Ellipse2D):
    LINE_COLOR = "navy"
    ELLIPSE_OUTLINE = "navy"
    ELLIPSE_FILL = "orange"
    CIRCLE_RADIUS = 8

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
