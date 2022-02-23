from Window import Window

# create the window object
g = Window()

# run the window object
while g.running:
    # display the screen after each frame
    g.current_screen.display_screen()

    if g.playing:
        g.current_screen.play()
