from fractal_drawer import FractalDrawer


if __name__ == "__main__":
    mandelbrot = FractalDrawer(set_type="mandelbrot", color_map="viridis")
    mandelbrot.draw()
    julia = FractalDrawer(set_type="julia")
    julia.draw()
