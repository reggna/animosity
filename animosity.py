import sys
import pygame
from pygame.locals import * # For QUIT, K_ESCAPE, &c.

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
GRAY = pygame.Color(125, 125, 125)
WINDOW_SIZE = (1280,720)

class Button():
    def __init__(self, font, text, pos):
        self.text = text
        self._font = font
        self._pos = pos

    def render(self, surface):
        rect = pygame.Rect(self._pos, self._font.size(self.text))
        self._color = GRAY if (rect.collidepoint(pygame.mouse.get_pos())) else WHITE
        button = self._font.render(self.text, False, self._color)
        surface.blit(button, rect)

    def IsHighlighted(self):
        return self._color == GRAY

class Mode():
    def render(self, window):
        pass
    def HandleEvent(self, event):
        return self


class Menu(Mode):
    def __init__(self, pos, font):
        self.buttons = []
        self.pos = pos
        self.font = font

    def AddButton(self, text):
        pos = (self.pos[0], self.pos[1] + (self.font.get_height() * (len(self.buttons))))
        button = Button(self.font, text, pos)
        self.buttons.append(button)

    def render(self, window):
        for button in self.buttons:
            button.render(window)

    def GetHighlightedButton(self):
        for button in self.buttons:
            if button.IsHighlighted():
                return button
        return None

class MainMenu(Menu):
    def __init__(self):
        Menu.__init__(self, (100, 100), pygame.font.Font(None, 32))
        self.AddButton("Start new game")
        self.AddButton("Options")
        self.AddButton("Exit")

    def HandleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            button = self.GetHighlightedButton()
            if button != None:
                if button.text == "Start new game":
                    return Game()
                elif button.text == "Exit":
                    return None
        return self

class Card():
    def __init__(self, x, y, value):
        self._font = pygame.font.Font(None, 24)
        self._x = x
        self._y = y
        self._width = 40
        self._height = 90
        self._value = value

    def render(self, surface):
        card_rect = pygame.Rect(self._x, self._y, self._width, self._height)
        self._color = GRAY if (card_rect.collidepoint(pygame.mouse.get_pos())) else WHITE
        pygame.draw.rect(surface, self._color, [self._x, self._y, self._width, self._height])
        pygame.draw.rect(surface, BLACK, [self._x + 1, self._y + 1, self._width - 2, self._height - 2])
        text_rect = pygame.Rect((self._x + self._width/(4-(self._value>9)), self._y + self._height/3), self._font.size(str(self._value)))
        surface.blit(self._font.render(str(self._value), False, self._color), text_rect)

class Game(Mode):
    def __init__(self):
        self._card = Card(10, 20, 10)
        self._card2 = Card(200, 20, 9)

    def render(self, surface):
        self._card.render(surface)
        self._card2.render(surface)

def run():
    pygame.init()
    window = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("animosity")
    fpsClock = pygame.time.Clock()

    mainMenu = MainMenu()
    currentMode = mainMenu

    while True:
        window.fill(BLACK)
        currentMode.render(window)

        for event in pygame.event.get():
            currentMode = currentMode.HandleEvent(event)
            if currentMode == None or event.type == QUIT:
                pygame.quit()
                return 0
        pygame.display.update()
        fpsClock.tick(30)

if __name__ == "__main__":
    sys.exit(run())
