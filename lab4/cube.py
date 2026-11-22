from rectangle import Rectangle2D
from line import Line2D


class CubeShape(Rectangle2D, Line2D):
    RECT_OUTLINE = "darkgreen"
    RECT_FILL = ""
    LINE_COLOR = "darkgreen"
    DEPTH_RATIO = 0.3

    def _geometry(self, p1, p2):
        x1, x2 = sorted((p1[0], p2[0]))
        y1, y2 = sorted((p1[1], p2[1]))
        d = max(8, round(self.DEPTH_RATIO * min(x2 - x1, y2 - y1)))
        front = ((x1, y1), (x2, y2))
        back = ((x1 + d, y1 - d), (x2 + d, y2 - d))
        edges = [
            ((x1, y1), (x1 + d, y1 - d)),
            ((x2, y1), (x2 + d, y1 - d)),
            ((x1, y2), (x1 + d, y2 - d)),
            ((x2, y2), (x2 + d, y2 - d)),
        ]
        return front, back, edges

    def show_rubber(self, canvas, current_point, tag="rubber"):
        canvas.delete(tag)
        if not self.start:
            return
        front, back, edges = self._geometry(self.start, current_point)
        for (a, b) in (front, back):
            canvas.create_rectangle(
                a[0], a[1], b[0], b[1],
                outline=self.RUBBER_COLOR, dash=self.RUBBER_DASH, tags=tag
            )
        for (a, b) in edges:
            canvas.create_line(
                a[0], a[1], b[0], b[1],
                fill=self.RUBBER_COLOR, dash=self.RUBBER_DASH, tags=tag
            )

    def show(self, canvas):
        front, back, edges = self._geometry(self.start, self.end)
        self._show_part(Rectangle2D, front[0], front[1], canvas)
        self._show_part(Rectangle2D, back[0], back[1], canvas)
        for (a, b) in edges:
            self._show_part(Line2D, a, b, canvas)
