import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def mandelbrot(size, zoom, iterations, color_scheme):
    xmin, xmax, ymin, ymax = -2.0/zoom, 1.0/zoom, -1.5/zoom, 1.5/zoom
    x, y = np.linspace(xmin, xmax, size), np.linspace(ymin, ymax, size)
    c = x + y[:, None]*1j
    z = c
    fractal = np.zeros((size, size))
    for i in range(iterations):
        z = z*z + c
        fractal += (abs(z) < 2)
    if color_scheme == "Rainbow":
        fractal = rainbow_colormap(fractal)
    else:
        fractal = grayscale_colormap(fractal)
    return Image.fromarray(np.uint8(fractal))


def julia(size, zoom, iterations, color_scheme, c):
    xmin, xmax, ymin, ymax = -1.5/zoom, 1.5/zoom, -1.5/zoom, 1.5/zoom
    x, y = np.linspace(xmin, xmax, size), np.linspace(ymin, ymax, size)
    z = x + y[:, None]*1j
    fractal = np.zeros((size, size))
    for i in range(iterations):
        z = z*z + c
        fractal += (abs(z) < 2)
    if color_scheme == "Rainbow":
        fractal = rainbow_colormap(fractal)
    else:
        fractal = grayscale_colormap(fractal)
    return Image.fromarray(np.uint8(fractal))


def rainbow_colormap(fractal):
    fractal = np.log(fractal + 1)
    fractal /= fractal.max()
    fractal = np.uint8(plt.cm.rainbow(fractal) * 255)
    return fractal


def grayscale_colormap(fractal):
    fractal = np.log(fractal + 1)
    fractal /= fractal.max()
    fractal = np.uint8(plt.cm.gray(fractal) * 255)
    return fractal


st.title("Fractal Generator Game")

# Select the fractal type
fractal_type = st.selectbox("Select a fractal type", ["Mandelbrot", "Julia"])

# Select the fractal size
size = st.slider("Select the fractal size", min_value=100, max_value=1000, value=500)

# Select the fractal zoom
zoom = st.slider("Select the fractal zoom", min_value=1, max_value=10, value=1)

# Select the fractal iterations
iterations = st.slider("Select the fractal iterations", min_value=1, max_value=50, value=20)

# Select the color scheme
color_scheme = st.selectbox("Select a color scheme", ["Rainbow", "Grayscale"])

# Get the fractal parameters
c = st.text_input("Enter the value of c (for Julia fractals only)", value="-0.4 + 0.6j")
c = complex("".join(c.split()))

# Generate the fractal
if fractal_type == "Mandelbrot":
    img = mandelbrot(size, zoom, iterations, color_scheme)
else:
    img = julia(size, zoom, iterations, color_scheme, c)

# Show the fractal
st.image(img)

