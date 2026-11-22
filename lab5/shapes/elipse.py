from .base import Shape, register


@register("ellipse", "Еліпс", order=40)
class Ellipse2D(Shape):
    ELLIPSE_OUTLINE = "black"
    ELLIPSE_FILL = "pink"

    def _bounds(self, current_point):
        cx, cy = self.start
        dx = abs(current_point[0] - cx)
        dy = abs(current_point[1] - cy)
        return (cx - dx, cy - dy, cx + dx, cy + dy)

    def bbox(self):
        return self._bounds(self.end)

    def show_rubber(self, canvas, current_point, tag="rubber"):
        canvas.delete(tag)
        if self.start:
            x1, y1, x2, y2 = self._bounds(current_point)
            canvas.create_oval(
                x1, y1, x2, y2,
                outline=self.RUBBER_COLOR, dash=self.RUBBER_DASH, tags=tag
            )

    def show(self, canvas):
        x1, y1, x2, y2 = self._bounds(self.end)
        canvas.create_oval(
            x1, y1, x2, y2,
            outline=self.ELLIPSE_OUTLINE, fill=self.ELLIPSE_FILL
        )
