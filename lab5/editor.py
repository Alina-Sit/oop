from shapes import registered, create

N = 128
FILE_HEADER = "# MyEditor shapes v1"


class MyEditor:
    _creating = False

    def __init__(self):
        if not MyEditor._creating:
            raise RuntimeError("MyEditor - Singleton: використовуйте MyEditor.instance()")
        self.pcshape = [None] * N
        self.count = 0
        self.current_key = "rectangle"
        self.current_shape = None
        self.selected = None
        self._listeners = []

    @staticmethod
    def instance():
        factory = MyEditor.instance
        if not hasattr(factory, "static_obj"):
            MyEditor._creating = True
            try:
                factory.static_obj = MyEditor()
            finally:
                MyEditor._creating = False
        return factory.static_obj

    def __copy__(self):
        raise TypeError("Singleton не можна копіювати")

    def __deepcopy__(self, memo):
        raise TypeError("Singleton не можна копіювати")

    def add_listener(self, listener):
        self._listeners.append(listener)

    def _notify(self, event):
        for listener in list(self._listeners):
            listener(event)

    def type_names(self):
        return [(cls.KEY, cls.NAME) for cls in registered()]

    def set_type(self, key):
        self.current_key = key

    def shapes(self):
        return self.pcshape[:self.count]

    def is_full(self):
        return self.count >= N

    def on_lbdown(self, x, y):
        if self.is_full():
            return False
        self.current_shape = create(self.current_key)
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
        self.pcshape[self.count] = self.current_shape
        self.count += 1
        self.current_shape = None
        self.selected = None
        self._notify("shapes")

    def select(self, index):
        if index is not None and not (0 <= index < self.count):
            index = None
        if index != self.selected:
            self.selected = index
            self._notify("selection")

    def remove(self, index):
        if not (0 <= index < self.count):
            return False
        for i in range(index, self.count - 1):
            self.pcshape[i] = self.pcshape[i + 1]
        self.count -= 1
        self.pcshape[self.count] = None
        self.selected = None
        self._notify("shapes")
        return True

    def clear(self):
        self.pcshape = [None] * N
        self.count = 0
        self.current_shape = None
        self.selected = None
        self._notify("shapes")

    def rows(self):
        result = []
        for i, shape in enumerate(self.shapes(), start=1):
            result.append((i, shape.NAME, shape.start[0], shape.start[1], shape.end[0], shape.end[1]))
        return result

    def repaint(self, canvas):
        canvas.delete("all")
        for shape in self.shapes():
            shape.show(canvas)
        if self.selected is not None:
            x1, y1, x2, y2 = self.shapes()[self.selected].bbox()
            pad = 5
            canvas.create_rectangle(
                x1 - pad, y1 - pad, x2 + pad, y2 + pad,
                outline="red", width=2, dash=(6, 3), tags="selection"
            )

    def save(self, path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(FILE_HEADER + "\n")
            for shape in self.shapes():
                key, x1, y1, x2, y2 = shape.to_record()
                f.write(f"{key} {x1} {y1} {x2} {y2}\n")
        return self.count

    def load(self, path):
        loaded = []
        skipped = 0
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                try:
                    key, *numbers = line.split()
                    x1, y1, x2, y2 = (int(v) for v in numbers)
                    shape = create(key)
                except (ValueError, KeyError):
                    skipped += 1
                    continue
                shape.set_start((x1, y1))
                shape.set_end((x2, y2))
                loaded.append(shape)
        loaded = loaded[:N]
        self.pcshape = loaded + [None] * (N - len(loaded))
        self.count = len(loaded)
        self.current_shape = None
        self.selected = None
        self._notify("shapes")
        return len(loaded), skipped
