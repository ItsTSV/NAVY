import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors, colormaps
import imageio


class FractalDrawer:
    """Class for generating and displaying Fractals."""

    def __init__(
        self,
        set_type="mandelbrot",
        max_iter=100,
        resolution=600,
        color_map="hsv",
        zoom_factor=0.75,
        zoom_center=complex(-1.6, 0),
    ):
        """Initializes either Mandelbrot or Julia fractal and its parameters.

        Attributes:
            set_type: str, either "Mandelbrot" or "Julia"
            max_iter: int, maximum amount of iterations per point
            resolution: int, width and height of the image
            c_const: complex, const used to draw Julia set
            x_bounds: [float, float], range of x axes values
            y_bounds: [float, float], range of y axes values
            zoom_center: complex, center of the zoom
            color_map: string, https://matplotlib.org/stable/users/explain/colors/colormaps.html
        """
        self.set_type = set_type
        self.max_iter = max_iter
        self.resolution = resolution
        self.color_map = color_map
        self.zoom_factor = zoom_factor

        if color_map not in list(colormaps):
            raise ValueError(f"Invalid color_map: {color_map}")

        if set_type == "mandelbrot":
            self.x_bounds = [-2, 1]
            self.y_bounds = [-1, 1]
            self.zoom_center = zoom_center
        elif set_type == "julia":
            self.x_bounds = [-1.5, 1.5]
            self.y_bounds = [-1.5, 1.5]
            self.zoom_center = complex(-0.7, -0.3)
        else:
            raise ValueError("Invalid set_type")

        self.c_const = complex(-0.8, 0.156)
        self.fig, self.ax = plt.subplots()
        self.fig.canvas.mpl_connect("button_press_event", self.zoom_on_click)

    def mandelbrot(self, c):
        """Computes number of iterations before the point *escapes* from Mandelbrot set"""
        z = 0
        for n in range(self.max_iter):
            if abs(z) > 2:
                return n
            z = z * z + c
        return self.max_iter

    def julia(self, z):
        """Computes number of iterations before the point *escapes* from Julia set"""
        c = self.c_const
        for n in range(self.max_iter):
            if abs(z) > 2:
                return n
            z = z * z + c
        return self.max_iter

    def generate_image(self):
        """Generates image of selected fractal.

        First, an image containing zeros is created. The algorithm then iterates through every pixel of the image,
        computing whether it belongs to the set or not. After that, the values are normalized into <0, 1> range
        and transferred to HSV format.
        """
        width, height = self.resolution, self.resolution
        image = np.zeros((height, width))
        x = np.linspace(self.x_bounds[0], self.x_bounds[1], width)
        y = np.linspace(self.y_bounds[0], self.y_bounds[1], height)

        for i in range(height):
            for j in range(width):
                zx = x[j]
                zy = y[i]
                z = complex(zx, zy)
                if self.set_type == "mandelbrot":
                    image[i, j] = self.mandelbrot(z)
                else:
                    image[i, j] = self.julia(z)

        norm = colors.Normalize(vmin=0, vmax=self.max_iter)
        colormap = plt.cm.get_cmap(self.color_map)
        return colormap(norm(image))

    def draw(self):
        """Draws image of a fractal using Matplotlib."""
        self.ax.clear()
        img = self.generate_image()
        self.ax.imshow(img, extent=(*self.x_bounds, *self.y_bounds), origin="lower")
        self.ax.axis("off")
        self.fig.canvas.draw()
        plt.pause(0)

    def zoom_step(self, zoom_center):
        """Zooms into the fractal around a specific point by reducing x/y bounds."""
        x_range = self.x_bounds[1] - self.x_bounds[0]
        y_range = self.y_bounds[1] - self.y_bounds[0]

        x_center, y_center = zoom_center.real, zoom_center.imag
        new_x_range = x_range * self.zoom_factor
        new_y_range = y_range * self.zoom_factor

        self.x_bounds = [x_center - new_x_range / 2, x_center + new_x_range / 2]
        self.y_bounds = [y_center - new_y_range / 2, y_center + new_y_range / 2]

    def zoom_on_click(self, event):
        """Zooms into the fractal on mouse click -- might take some time ;)"""
        if event.inaxes is not None:
            x = event.xdata
            y = event.ydata
            zoom_center = complex(x, y)
            self.zoom_step(zoom_center)
            self.draw()

    def generate_gif(self, frames=100):
        """Creates a GIF of the fractal zooming in."""
        images = []

        for i in range(frames):
            print(f"Frame {i + 1}/{frames}")
            img = self.generate_image()
            self.zoom_step(self.zoom_center)
            images.append((img * 255).astype(np.uint8))
            self.draw()
        plt.close(self.fig)

        imageio.mimsave(f"{self.set_type}_zoom.gif", images, fps=12)
