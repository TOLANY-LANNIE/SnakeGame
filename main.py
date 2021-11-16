import pygame
import random
import sys

from pygame.locals import *

# Constant variables
FPS = 5
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
DARKGRAY = (40, 40, 40)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0  # syntactic sugar: index of the snake's head

RUNNING = True

pygame.mixer.init()
# Load all sound files
pygame.mixer.music.load("audio/mixkit-infected-vibes-157.mp3")
pygame.mixer.music.play(-1, 0.0)

eat_apple = pygame.mixer.Sound("audio/mixkit-retro-game-notification-212.wav")
eat_apple.set_volume(0.5)
collision_sound = pygame.mixer.Sound("audio/mixkit-sad-game-over-trombone-471.wav")
collision_sound.set_volume(0.5)


def main():
    global SCREEN, CLOCK, BASICFONT
    # Setup for sounds. Defaults are good.

    pygame.init()

    # game title and icon
    pygame.display.set_caption('Snake Game')
    icon = pygame.image.load("img/snakeIcon.png")
    pygame.display.set_icon(icon)

    SCREEN = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    CLOCK = pygame.time.Clock()  # fps

    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()


# display gir of the screen
def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE):  # draw vertical lines
        pygame.draw.line(SCREEN, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
        for y in range(0, WINDOWHEIGHT, CELLSIZE):  # draw horizontal lines
            pygame.draw.line(SCREEN, DARKGRAY, (0, y), (WINDOWWIDTH, y))


def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    SCREEN.blit(pressKeySurf, pressKeyRect)


# DISPLAY "Snake Game" ON THE START SCREEN
def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf = titleFont.render('Snake Game!', True, DARKGREEN, WHITE)

    degrees1 = 0
    while True:
        SCREEN.fill(WHITE)
        rotatedSurf1 = pygame.transform.rotate(titleSurf, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        SCREEN.blit(rotatedSurf1, rotatedRect1)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get()  # clear event queue
            return
        pygame.display.update()
        CLOCK.tick(40)
        degrees1 += 3  # rotate by 3 degrees each frame


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def terminate():
    pygame.quit()
    sys.exit()


def runGame():
    # Set a random start point.
    pygame.mixer.music.unpause()
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    snakeCoords = [{'x': startx, 'y': starty},
                   {'x': startx - 1, 'y': starty},
                   {'x': startx - 2, 'y': starty}]
    direction = RIGHT

    # Start the apple in a random place.
    apple = getRandomLocation()

    while RUNNING:  # main game loop
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_SPACE:
                    pause()
                elif event.key == K_ESCAPE:
                    terminate()

        # check if the snake has hit itself or the edge
        if snakeCoords[HEAD]['x'] == -1 or snakeCoords[HEAD]['x'] == CELLWIDTH or snakeCoords[HEAD]['y'] == -1 or \
                snakeCoords[HEAD]['y'] == CELLHEIGHT:
            collision_sound.play()
            return  # game over
        for snakeBody in snakeCoords[1:]:
            if snakeBody['x'] == snakeCoords[HEAD]['x'] and snakeBody['y'] == snakeCoords[HEAD]['y']:
                collision_sound.play()
                return  # game over

        # check if snake has eaten an apple
        if snakeCoords[HEAD]['x'] == apple['x'] and snakeCoords[HEAD]['y'] == apple['y']:
            # don't remove snake's tail segment
            eat_apple.play()
            apple = getRandomLocation()  # set a new apple somewhere
        else:
            del snakeCoords[-1]  # remove snake's tail segment

        # move the snake by adding a segment in the direction it is moving
        if direction == UP:
            newHead = {'x': snakeCoords[HEAD]['x'], 'y': snakeCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': snakeCoords[HEAD]['x'], 'y': snakeCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': snakeCoords[HEAD]['x'] - 1, 'y': snakeCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': snakeCoords[HEAD]['x'] + 1, 'y': snakeCoords[HEAD]['y']}
        snakeCoords.insert(0, newHead)
        SCREEN.fill(BGCOLOR)
        drawGrid()
        drawSnake(snakeCoords)
        drawApple(apple)
        drawScore(len(snakeCoords) - 3)
        drawSpeed(FPS)
        pygame.display.update()
        CLOCK.tick(FPS)


# to randomly position the  the apple of the screen
def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}


def drawSnake(snakeCoords):
    for coord in snakeCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        snakeSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(SCREEN, DARKGREEN, snakeSegmentRect)
        snakeInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(SCREEN, GREEN, snakeInnerSegmentRect)


def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 100)
    gameOverSurf = gameOverFont.render('Game Over!', True, RED)
    startSurf = gameOverFont.render('Start Again?', True, WHITE)
    gameOverRect = gameOverSurf.get_rect()
    startGameRect = startSurf.get_rect()
    gameOverRect.midtop = (WINDOWWIDTH / 2, 10)
    startGameRect.midtop = (WINDOWWIDTH / 2, gameOverRect.height + 10 + 25)

    SCREEN.blit(gameOverSurf, gameOverRect)
    SCREEN.blit(startSurf, startGameRect)
    pygame.mixer.music.pause()
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress()  # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get()  # clear event queue
            return


def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    SCREEN.blit(scoreSurf, scoreRect)


def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    apple = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(SCREEN, RED, apple)


def pause():
    font = pygame.font.Font('freesansbold.ttf', 80)
    pauseSurf = font.render('Game Paused!', True, WHITE)
    pauseRect = pauseSurf.get_rect()
    pauseRect.midtop = (WINDOWWIDTH / 2, WINDOWHEIGHT/2)
    SCREEN.blit(pauseSurf, pauseRect)
    pygame.mixer.music.pause()
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(5000)
    checkForKeyPress()  # clear out any key presses in the event queue
    pygame.mixer.music.unpause()


def drawSpeed(FPS):
    speedSurf = BASICFONT.render('Speed: %s' % (FPS), True, WHITE)
    speedRect = speedSurf.get_rect()
    speedRect.topleft = (WINDOWWIDTH - 120, 40)
    SCREEN.blit(speedSurf, speedRect)


if __name__ == '__main__':
    main()
