import pygame as pg

class button():

    def __init__(self, display, x, y, width, height, buttonColours, textColours, font=None, text=None, image=None):
        """
        Purpose: Makes a button object (Can't have both an image and text)
        Pre-conditions:
            :param display: the current pygame.display for the window
            :param x: the x coordinate of the button
            :param y: the y coordinate of the button
            :param width: the width of the button
            :param height: the height of the button
            :param buttonColours: 3 colours (r,g,b) that go from 0-255
            :param textColours: 3 colours (r,g,b) that go from 0-255
            :param font: font of the text inside of the button (only needed when using text)
            :param text: the text inside of the button (optional)
            :param image: the image of the button (optional)
        """
        self.display = display
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.image = image
        self.clicked = False
        self.buttonColour = list(buttonColours)
        self.hoverColour = list(buttonColours)
        self.clickColour = list(buttonColours)
        self.textColour = textColours
        self.font = font
        self.action = False

        # Calculate the hover and click colours
        for index in range(len(buttonColours)):
            if (self.buttonColour[index] <= 190):
                self.hoverColour[index] += 30
            else:
                self.hoverColour[index] = 255

            if (self.buttonColour[index] >= 30):
                self.clickColour[index] -= 30
            else:
                self.clickColour[index] = 0
        self.buttonColour = tuple(self.buttonColour)
        self.hoverColour = tuple(self.hoverColour)
        self.clickColour = tuple(self.clickColour)

        # Checks input to see if they are proper input
        self.__inputCheck()

    def __inputCheck(self):
        if self.x < 0 or self.y < 0:
            raise Exception("Error: x and y coordinates for button are negative")
        if self.width <= 0 or self.height <= 0:
            raise Exception("Error: width and height for button are 0 or negative")
        if self.buttonColour is None:
            raise Exception("Error: no buttonColour for button given")
        if self.textColour is None:
            raise Exception("Error: no textColour for button given")
        if (self.text is not None) and (self.font is None):
            raise Exception("Error: no font given for text button")
        if (self.text is None) and (self.image is None):
            raise Exception("Error: no text or image given for button")


    def draw(self):
        """
        Purpose: Draws a button to the display and checks if the button is clicked
        Return: True if the button was clicked, False otherwise
        """
        self.action = False

        # Get mouse position
        pos = pg.mouse.get_pos()

        # Create rect object for button
        buttonRect = pg.Rect(self.x, self.y, self.width, self.height)

        # Add outline to button
        outlineRect = pg.Rect(self.x - 2, self.y - 2, self.width + 4, self.height + 4)
        pg.draw.rect(self.display, (0, 0, 0), outlineRect)

        # Check if mouse over button and if clicked
        if buttonRect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1:
                self.clicked = True
                pg.draw.rect(self.display, self.clickColour, buttonRect)
            elif pg.mouse.get_pressed()[0] == 0 and self.clicked == True:
                self.clicked = False
                self.action = True
            else:
                pg.draw.rect(self.display, self.hoverColour, buttonRect)
        else:
            pg.draw.rect(self.display, self.buttonColour, buttonRect)

        # Add text to button
        if self.text is not None:
            # Turns text into image, scales it to fit in button, then displays
            textImage = self.font.render(self.text, True, self.textColour)
            textTransform = pg.transform.scale(textImage, (int(self.width/1.1), int(self.height/1.1)))
            textLen = textTransform.get_width()
            textHeight = textTransform.get_height()
            self.display.blit(textTransform, (self.x + int(self.width / 2) - int(textLen / 2), self.y + int(self.height / 2) - int(textHeight / 2)))
        # If a image is given then add image to button
        elif self.image is not None:
            imageTransform = pg.transform.scale(self.image, (self.width - 4, self.height - 4))
            self.display.blit(imageTransform, (self.x + 2, self.y + 2))

        return self.action

    def clickCheck(self):
        """
        :return: True if button was clicked, false otherwise
        """
        return self.action


if __name__ == '__main__':
    # Make window
    pg.init()
    display = pg.display.set_mode((600, 600))
    pg.display.set_caption('button.py test')
    font = pg.font.Font(pg.font.get_default_font(), 30)

    print("Running Button Test")

    # Load an image
    img = pg.image.load('Assets/Bubbles.jpg').convert_alpha()

    # Colours for buttons and text
    colour = (25, 190, 225)
    tc = (255, 255, 255)

    # Make button objects
    again = button(display, 75, 200, 90, 40, colour, tc, font, 'Play Again?')
    quit = button(display, 325, 200, 180, 70, (0,200,0), (200, 0, 0), font, 'Quit?')
    down = button(display, 75, 350, 180, 40, colour, tc, font, 'Down')
    up = button(display, 325, 350, 180, 40, colour, tc, font, 'Up')
    # How to make a button with an image
    imageButton = button(display, 10, 10, 92, 54, colour, tc, image=img)

    # Make a counter int
    counter = 0

    # Testing while loop to keep window running
    run = True
    while run:
        display.fill((200, 200, 200))

        # Draw the buttons
        again.draw()
        quit.draw()
        down.draw()
        up.draw()
        imageButton.draw()

        # Test non working dropBoxes
        try:
            button6 = button(display, -1, 10, 90, 70, colour, tc, font, 'test1')
        except Exception:
            pass
        else:
            print("Did not get Exception for negative x")

        try:
            button7 = button(display, 10, 10, 0, 70, colour, tc, font, 'test1')
        except Exception:
            pass
        else:
            print("Did not get Exception for zero width")

        try:
            button8 = button(display, 10, 10, 90, 70, None, tc, font, 'test1')
        except Exception:
            pass
        else:
            print("Did not get Exception for no buttonColour")

        try:
            button9 = button(display, 10, 10, 90, 70, colour, None, font, 'test1')
        except Exception:
            pass
        else:
            print("Did not get Exception for no textColour")

        try:
            button10 = button(display, 10, 10, 90, 70, colour, tc, None, 'test1')
        except Exception:
            pass
        else:
            print("Did not get Exception for no font for text button")

        try:
            button11 = button(display, 10, 10, 90, 70, colour, tc, font)
        except Exception:
            pass
        else:
            print("Did not get Exception for no text or image given")

        # If returns true when the button has been clicked
        if again.clickCheck():
            print('Again')
            counter = 0
        if quit.clickCheck():
            print('Quit')
            run = False
        if down.clickCheck():
            print('Down')
            counter -= 1
        if up.clickCheck():
            print('Up')
            counter += 1
        if imageButton.clickCheck():
            print('Hidden EasterEgg! :)')

        # Turns the counter int into a image and then displays it on the display
        counterImage = font.render(str(counter), True, (255, 0, 0))
        display.blit(counterImage, (280, 450))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        pg.display.update()
    pg.quit()
    print("Tests Complete")