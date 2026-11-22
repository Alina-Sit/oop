from .base import Shape, register


@register("rectangle", "Прямокутник", order=30)
class Rectangle2D(Shape):
    RECT_OUTLINE = "black"
    RECT_FILL = ""

    def show_rubber(self, canvas, current_point, tag="rubber"):
        canvas.delete(tag)
        if self.start:
            canvas.create_rectangle(
                self.start[0], self.start[1],
                current_point[0], current_point[1],
                outline=self.RUBBER_COLOR, dash=self.RUBBER_DASH, tags=tag
            )

    def show(self, canvas):
        canvas.create_rectangle(
            self.start[0], self.start[1],
            self.end[0], self.end[1],
            outline=self.RECT_OUTLINE, fill=self.RECT_FILL
        )
