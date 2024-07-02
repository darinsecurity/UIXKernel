import numpy as np
from OpenGL.GL import *
import glfw
import time

# Window dimensions
width, height = 800, 600

# Framebuffer dimensions
fb_width, fb_height = 480, 360

# Function to create random RGB565 data
def create_random_rgb565_data(width, height):
    # Generate random data for RGB565
    data = np.random.randint(0, 65536, size=(height, width), dtype=np.uint16)
    return data

# Function to initialize OpenGL settings
def init_opengl():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_TEXTURE_2D)
    global texture_id
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glBindTexture(GL_TEXTURE_2D, 0)

# Function to display the framebuffer
def display():
    glClear(GL_COLOR_BUFFER_BIT)
    
    # Generate random framebuffer data
    framebuffer_data = create_random_rgb565_data(fb_width, fb_height)
    
    # Convert RGB565 to RGB888
    r = ((framebuffer_data >> 11) & 0x1F) * 255 // 31
    g = ((framebuffer_data >> 5) & 0x3F) * 255 // 63
    b = (framebuffer_data & 0x1F) * 255 // 31
    rgb_data = np.dstack((r, g, b)).astype(np.uint8)
    
    # Bind and update texture
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, fb_width, fb_height, 0, GL_RGB, GL_UNSIGNED_BYTE, rgb_data)
    
    # Render the texture to a quad
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex2f(-1.0, -1.0)
    glTexCoord2f(1.0, 0.0)
    glVertex2f(1.0, -1.0)
    glTexCoord2f(1.0, 1.0)
    glVertex2f(1.0, 1.0)
    glTexCoord2f(0.0, 1.0)
    glVertex2f(-1.0, 1.0)
    glEnd()
    
    glBindTexture(GL_TEXTURE_2D, 0)

# Function to handle window resizing
def reshape(window, w, h):
    global width, height
    width, height = w, h
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    #gluOrtho2D(-1.0, 1.0, -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)

# Main function to set up the GLFW window and start the main loop
def main():
    if not glfw.init():
        return

    window = glfw.create_window(width, height, "Framebuffer Example with PyOpenGL", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    init_opengl()

    glfw.set_window_size_callback(window, reshape)

    while not glfw.window_should_close(window):
        display()
        glfw.swap_buffers(window)
        glfw.poll_events()
        #time.sleep(1.0 / 60.0)

    glfw.terminate()

if __name__ == "__main__":
    main()
