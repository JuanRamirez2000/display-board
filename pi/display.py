from rgbmatrix import RGBMatrix, RGBMatrixOptions

def get_matrix():
    """Configure and return the LED matrix object."""
    options = RGBMatrixOptions()
    options.rows = 32
    options.cols = 32
    options.chain_length = 1
    options.parallel = 1
    options.hardware_mapping = 'regular'  # change to 'adafruit-hat' if using that board
    options.gpio_slowdown = 2             # increase to 3 or 4 if display looks glitchy
    return RGBMatrix(options=options)

def render_pixels(pixels):
    """
    Take a flat list of 1024 [R, G, B] values and paint them on the matrix.
    Think of it like stamping a 32x32 photo onto the board one pixel at a time.
    """
    matrix = get_matrix()
    canvas = matrix.CreateFrameCanvas()

    for index, rgb in enumerate(pixels):
        x = index % 32   # column (0-31)
        y = index // 32  # row    (0-31)
        canvas.SetPixel(x, y, rgb[0], rgb[1], rgb[2])

    matrix.SwapOnVSync(canvas)  # push the full frame at once, prevents flickering