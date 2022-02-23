import pygame as pg
from Button import button

class dropBox():

    def __init__(self, display, x, y, width, height, font, textList, initialText=None):
        """
        Purpose: Makes a dropBox object (Can't have both an image and textList)
        Pre-conditions:
            :param display: the current pygame.display for the window
            :param x: the x coordinate of the dropBox
            :param y: the y coordinate of the dropBox
            :param width: the width of the dropBox
            :param height: the height of the dropBox
            :param font: font of the textList inside of the dropBox
            :param textList: list of strings for the dropBox
            :param initialText: the initial text to be displayed in the box
        """
        self.display = display
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.textList = textList
        self.clicked = False
        self.font = font
        self.action = False
        self.optionList = []

        # Find initial text
        if initialText is None:
            self.textDisplayed = textList[0]
        else:
            self.textDisplayed = initialText

        # Create button for dropBox
        img = pg.image.load('Assets/triangle.jpg').convert_alpha()
        self.dropButton = button(self.display, (self.x + self.width - (self.width // 4)), self.y, int(self.width // 4),
                                 int(self.height), (200, 200, 200), (0, 0, 0), image=img)

        # Create buttons for each available text option and make a list of them
        for index in range(len(self.textList)):
            self.optionList.append(button(self.display, self.x, self.y + (self.height * (index + 1)), self.width, self.height,
                                (200, 200, 200), (0, 0, 0), font=self.font, text=self.textList[index]))

        # Checks input to see if they are proper input
        self.__inputCheck()

    def __inputCheck(self):
        if self.x < 0 or self.y < 0:
            raise Exception("Error: x and y coordinates for dropBox are negative")
        if self.width <= 0 or self.height <= 0:
            raise Exception("Error: width and height for dropBox are 0 or negative")
        if self.font is None:
            raise Exception("Error: No font given for dropBox")
        if len(self.textList) <= 0:
            raise Exception("Error: No strings given in textList for dropBox")


    def draw(self):
        """
        Purpose: Draws a dropBox to the display and checks if the dropBox is clicked
        Return: True if the dropBox was clicked, False otherwise
        """
        self.action = False

        # Add outline to dropBox
        outlineRect = pg.Rect(self.x - 2, self.y - 2, self.width + 4, self.height + 4)
        pg.draw.rect(self.display, (0, 0, 0), outlineRect)

        # Create rect object for dropBox
        dropBoxRect = pg.Rect(self.x, self.y, self.width - (self.width//4), self.height)
        pg.draw.rect(self.display, (255, 255, 255), dropBoxRect)

        # Draw button
        self.dropButton.draw()

        # Check if dropButton is clicked, if so then open up drop menu
        if self.dropButton.clickCheck():
            self.clicked = True

        # Check if dropButton is clicked, if so then open up drop menu
        if self.clicked:
            # Draw Buttons for each available text option
            for index in range(len(self.optionList)):
                self.optionList[index].draw()
                if self.optionList[index].clickCheck():
                    self.textDisplayed = self.textList[index]
                    self.action = True
                    self.clicked = False

        # Add text to dropBox
        # Turns text into image, scales it to fit in dropBox, then displays
        textImage = self.font.render(self.textDisplayed, True, (0, 0, 0))
        textTransform = pg.transform.scale(textImage, (int((self.width - (self.width//4))/1.1), int(self.height/1.1)))
        textHeight = textTransform.get_height()
        self.display.blit(textTransform, (self.x, self.y + int(self.height / 2) - int(textHeight / 2)))

        return self.action

    def isChanged(self):
        """
        :return: True if dropBox was changed, false otherwise
        """
        return self.action


    def getValue(self):
        """
        :return: Returns the string that was selected
        """
        return self.textDisplayed


if __name__ == '__main__':
    # Make window
    pg.init()
    display = pg.display.set_mode((600, 600))
    pg.display.set_caption('dropBox.py test')
    font = pg.font.Font(pg.font.get_default_font(), 30)

    print("Running DropBox Test")

    # Make dropBox objects
    resolution = dropBox(display, 50, 75, 200, 70, font, ['480p', '720p', '1080p'])
    difficulty = dropBox(display, 350, 75, 200, 70, font, ['Easy', 'Normal', 'Hard', 'Impossible'])

    # Test non working dropBoxes
    try:
        bar4 = dropBox(display, -1, 10, 90, 70, font, ['test1', 'test2'])
    except Exception:
        pass
    else:
        print("Did not get Exception for negative x")

    try:
        bar5 = dropBox(display, 10, 10, 0, 70, font, ['test1', 'test2'])
    except Exception:
        pass
    else:
        print("Did not get Exception for zero width")

    try:
        bar6 = dropBox(display, 10, 10, 90, 70, None, ['test1', 'test2'])
    except Exception:
        pass
    else:
        print("Did not get Exception for no font")

    try:
        bar7 = dropBox(display, 10, 10, 0, 70, font, [])
    except Exception:
        pass
    else:
        print("Did not get Exception for textList with length of zero")

    # Testing while loop to keep window running
    run = True
    while run:
        display.fill((200, 200, 200))

        # Draw the dropBoxs
        resolution.draw()
        difficulty.draw()

        # If returns true when the dropBox has been changed
        if resolution.isChanged():
            print(resolution.getValue())
        if difficulty.isChanged():
            print(difficulty.getValue())

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        pg.display.update()
    pg.quit()
    print("Tests Complete")