from shape import Shape


class Line2D(Shape):
    LINE_COLOR = "black"

    def show_rubber(self, canvas, current_point, tag="rubber"):
        Shape.show_rubber(self, canvas, current_point, tag)

    def show(self, canvas):
        canvas.create_line(
            self.start[0], self.start[1],
            self.end[0], self.end[1],
            fill=self.LINE_COLOR, width=1
        )
