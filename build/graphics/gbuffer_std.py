class FrameBuffer:
    def __init__(self, args):
        self.width = args.get('width')
        self.height = args.get('height')
        self.format = ["RGB565", 16]

        # position to the bottom left corner
        self.pos_x = 0
        self.pos_y = 0

        # opacity from 0 to 255
        self.opacity = 0

        self.frame_array = bytearray(self.width*self.height*int(self.format[1]/2))

    def fill(self, c):
        for i in range(len(self.frame_array)):
            self.frame_array[i] = c

    def pixel(self, x, y, c=None):
        index = (y * self.width + x) * int(self.format[1]/2)
        if c is None:
            return self.frame_array[index]
        self.frame_array[index] = c

    def hline(self, x, y, w, c):
        for i in range(w):
            self.pixel(x + i, y, c)

    def vline(self, x, y, h, c):
        for i in range(h):
            self.pixel(x, y + i, c)

    def line(self, x1, y1, x2, y2, c):
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            self.pixel(x1, y1, c)
            if x1 == x2 and y1 == y2:
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

    def rect(self, x, y, w, h, c, f=False):
        if f:
            for i in range(h):
                self.hline(x, y + i, w, c)
        else:
            self.hline(x, y, w, c)
            self.hline(x, y + h - 1, w, c)
            self.vline(x, y, h, c)
            self.vline(x + w - 1, y, h, c)

    def ellipse(self, x, y, xr, yr, c, f=False, m=0b1111):
        # Midpoint ellipse algorithm
        a2 = xr * xr
        b2 = yr * yr
        fa2 = 4 * a2
        fb2 = 4 * b2

        # First set of points
        sigma = 2 * b2 + a2 * (1 - 2 * yr)
        x0 = 0
        y0 = yr

        while b2 * x0 <= a2 * y0:
            if m & 0b0001:
                self.pixel(x + x0, y - y0, c)
                self.pixel(x - x0, y - y0, c)
            if m & 0b0010:
                self.pixel(x - x0, y + y0, c)
                self.pixel(x + x0, y + y0, c)
            if f:
                self.line(x - x0, y - y0, x + x0, y - y0, c)
                self.line(x - x0, y + y0, x + x0, y + y0, c)
            if sigma >= 0:
                sigma += fa2 * (1 - y0)
                y0 -= 1
            sigma += b2 * ((4 * x0) + 6)
            x0 += 1

        # Second set of points
        sigma = 2 * a2 + b2 * (1 - 2 * xr)
        x0 = xr
        y0 = 0

        while a2 * y0 <= b2 * x0:
            if m & 0b0001:
                self.pixel(x + x0, y - y0, c)
                self.pixel(x - x0, y - y0, c)
            if m & 0b0010:
                self.pixel(x - x0, y + y0, c)
                self.pixel(x + x0, y + y0, c)
            if f:
                self.line(x + x0, y - y0, x + x0, y + y0, c)
                self.line(x - x0, y - y0, x - x0, y + y0, c)
            if sigma >= 0:
                sigma += fb2 * (1 - x0)
                x0 -= 1
            sigma += a2 * ((4 * y0) + 6)
            y0 += 1

    def poly(self, x, y, coords, c, f=False):
        n = len(coords) // 2

        # Draw the outline
        for i in range(n):
            x0, y0 = coords[2*i], coords[2*i + 1]
            x1, y1 = coords[2*((i + 1) % n)], coords[2*((i + 1) % n) + 1]
            self.line(x + x0, y + y0, x + x1, y + y1, c)

        if f:
            # Fill polygon using scanline fill algorithm
            def edge_table(coords):
                edges = []
                for i in range(n):
                    x0, y0 = coords[2*i], coords[2*i + 1]
                    x1, y1 = coords[2*((i + 1) % n)], coords[2*((i + 1) % n) + 1]
                    if y0 != y1:
                        if y0 > y1:
                            x0, y0, x1, y1 = x1, y1, x0, y0
                        edges.append((y0, y1, x0, (x1 - x0) / (y1 - y0)))
                return sorted(edges)

            edges = edge_table(coords)
            if not edges:
                return

            y_min = edges[0][0]
            y_max = max(edge[1] for edge in edges)

            active_edges = []
            current_y = y_min

            while current_y < y_max:
                while edges and edges[0][0] == current_y:
                    active_edges.append(edges.pop(0)[1:])
                active_edges = [edge for edge in active_edges if edge[0] != current_y]

                active_edges.sort(key=lambda edge: edge[1])
                for i in range(0, len(active_edges), 2):
                    x_start = int(active_edges[i][1])
                    x_end = int(active_edges[i+1][1])
                    self.hline(x + x_start, y + current_y, x_end - x_start, c)

                current_y += 1
                for edge in active_edges:
                    edge = (edge[0], edge[1] + edge[2])
