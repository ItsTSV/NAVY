from fractal_drawer import FractalDrawer
from matplotlib import pyplot as plt


if __name__ == "__main__":
    mandelbrot_draw = FractalDrawer(set_type="mandelbrot")
    mandelbrot_draw.animate_zoom()
    julia_draw = FractalDrawer(set_type="julia")
    julia_draw.animate_zoom()