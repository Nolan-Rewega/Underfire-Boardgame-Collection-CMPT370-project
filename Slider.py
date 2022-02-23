import pygame as pg

class slider():
    """
    Purpose: Makes a slider object (Can't have both an image and text)
    Pre-conditions:
        :param display: the current pygame.display for the window
        :param x: the x coordinate of the slider
        :param y: the y coordinate of the slider
        :param width: the width of the slider
        :param height: the height of the slider
        :param percentage: the percentage of the bar filled (ex. 60 is 60%)
    """
    def __init__(self, display, x, y, width, height, percentage):
        self.display = display
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.percentage = percentage
        self.clicked = False
        # Colours for slider
        self.sliderColour = (128, 128, 128)
        self.barColour = (0, 0, 0)
        self.bgSliderColour = (255, 255, 255)
        self.action = False

        # Checks input to see if they are proper input
        self.__inputCheck()

    def __inputCheck(self):
        if self.x < 0 or self.y < 0:
            raise Exception("Error: x and y coordinates for slider are negative")
        if self.width <= 0 or self.height <= 0:
            raise Exception("Error: width and height for slider are 0 or negative")
        if self.percentage > 100 or self.percentage < 0:
            raise Exception("Error: percentage for slider is either above 100 or below 0")


    def draw(self):
        """
        Purpose: Draws a slider to the display and checks if the slider is clicked
        Return: True if the slider was clicked, False otherwise
        """
        self.action = False

        # Get mouse position
        pos = pg.mouse.get_pos()

        # Get width from percentage of bar filled
        sliderWidth = int((self.percentage / 100) * self.width)

        # Add outline to slider
        outlineRect = pg.Rect(self.x - 2, self.y - 2, self.width + 4, self.height + 4)
        pg.draw.rect(self.display, (0, 0, 0), outlineRect)

        # Create rect objects for slider
        bgSliderRect = pg.Rect(self.x, self.y, self.width, self.height)
        pg.draw.rect(self.display, self.bgSliderColour, bgSliderRect)

        sliderRect = pg.Rect(self.x, self.y, sliderWidth, self.height)
        barRect = pg.Rect(self.x + sliderWidth - self.width//30, self.y, self.width//15, self.height)

        # Check if mouse over slider and if clicked
        if bgSliderRect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1:
                self.clicked = True
                pg.draw.rect(self.display, self.sliderColour, pg.Rect(self.x, self.y, pos[0] - self.x, self.height))
                pg.draw.rect(self.display, self.barColour, pg.Rect(pos[0] - self.width//30, self.y, self.width//15, self.height))
            elif pg.mouse.get_pressed()[0] == 0 and self.clicked == True:
                self.clicked = False
                self.action = True
                self.percentage = int(((pos[0] - self.x) / self.width) * 100)
            else:
                pg.draw.rect(self.display, self.sliderColour, sliderRect)
                pg.draw.rect(self.display, self.barColour, barRect)
        # If mouse is clicked but mouse is not over slider
        elif pg.mouse.get_pressed()[0] == 1 and self.clicked:
            self.clicked = False
            self.action = True
            if pos[0] >= (self.x + self.width):
                self.percentage = 100
            elif pos[0] <= self.x:
                self.percentage = 0
            else:
                self.percentage = int(((pos[0] - self.x) / self.width) * 100)
        # Else if no user input on the slider
        else:
            pg.draw.rect(self.display, self.sliderColour, sliderRect)
            pg.draw.rect(self.display, self.barColour, barRect)

        return self.action

    def clickCheck(self):
        """
        :return: True if slider was clicked/moved, false otherwise
        """
        return self.action

    def getPercentage(self):
        """
        :return: The amount of the bar filled
        """
        return self.percentage


if __name__ == '__main__':
    # Make window
    pg.init()
    display = pg.display.set_mode((600, 600))
    pg.display.set_caption('slider.py test')
    font = pg.font.SysFont('Constantia', 30)

    print("Running Slider Test")

    # Make slider objects
    bar1 = slider(display, 75, 100, 90, 70, 0)
    bar2 = slider(display, 75, 200, 180, 50, 100)
    bar3 = slider(display, 75, 300, 400, 50, 34)

    # Test non working sliders
    try:
        bar4 = slider(display, -1, 10, 90, 70, 0)
    except Exception:
        pass
    else:
        print("Did not get Exception for negative x")

    try:
        bar5 = slider(display, 10, 10, 0, 70, 0)
    except Exception:
        pass
    else:
        print("Did not get Exception for zero width")

    try:
        bar6 = slider(display, 10, 10, 90, 70, -1)
    except Exception:
        pass
    else:
        print("Did not get Exception for less than zero percentage")

    try:
        bar7 = slider(display, 10, 10, 90, 70, 101)
    except Exception:
        pass
    else:
        print("Did not get Exception for less than zero percentage")

    # Make a counter int
    counter1 = bar1.getPercentage()
    counter2 = bar2.getPercentage()
    counter3 = bar3.getPercentage()

    # Testing while loop to keep window running
    run = True
    while run:
        display.fill((200, 200, 200))

        # Draw sliders
        bar1.draw()
        bar2.draw()
        bar3.draw()

        # Slider returns true if the slider has been dragged
        if bar1.clickCheck():
            # Can get the percentage of the bar filled from this method
            counter1 = bar1.getPercentage()
            print('bar1: ', counter1)
        if bar2.clickCheck():
            counter2 = bar2.getPercentage()
            print('bar2: ', counter2)
        if bar3.clickCheck():
            counter3 = bar3.getPercentage()
            print('bar3: ', counter3)

        # Turns the counter int into a image and then displays it on the display
        counterImage = font.render(str(counter1), True, (255, 0, 0))
        display.blit(counterImage, (450, 100))
        counterImage = font.render(str(counter2), True, (255, 0, 0))
        display.blit(counterImage, (450, 200))
        counterImage = font.render(str(counter3), True, (255, 0, 0))
        display.blit(counterImage, (510, 300))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        pg.display.update()
    pg.quit()
    print("Tests Complete")