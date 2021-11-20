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

try:  # Load all sound files
    pygame.mixer.music.load("audio/mixkit-infected-vibes-157.mp3")
    pygame.mixer.music.play(-1, 0.0)
    eat_apple = pygame.mixer.Sound("audio/mixkit-retro-game-notification-212.wav")
    eat_apple.set_volume(0.5)
    collision_sound = pygame.mixer.Sound("audio/mixkit-sad-game-over-trombone-471.wav")
    collision_sound.set_volume(0.5)
    # Load all sound files
    pygame.mixer.music.load("audio/mixkit-infected-vibes-157.mp3")
    pygame.mixer.music.play(-1, 0.0)
    eat_apple = pygame.mixer.Sound("audio/mixkit-retro-game-notification-212.wav")
    eat_apple.set_volume(0.5)
    collision_sound = pygame.mixer.Sound("audio/mixkit-sad-game-over-trombone-471.wav")
    collision_sound.set_volume(0.5)
except:
    pass


def main():
    global SCREEN, CLOCK, BASICFONT  # Variables that can be accessed by any function in the program

    pygame.init()

    pygame.display.set_caption('Snake Game')  # set game title
    icon = pygame.image.load("img/snakeIcon.png")  # game icon load image
    pygame.display.set_icon(icon)  # attach to icon to display

    SCREEN = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))  # set screen width and height
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)  # sent the font
    CLOCK = pygame.time.Clock()  # initialize game clock

    showStartScreen()  # call to  showStartScreen() function
    while True:
        runGame()  # call to  runGame() function
        showGameOverScreen()  # call to  showStartScreen() function


# display grid on the screen function
def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE):  # draw vertical lines
        pygame.draw.line(SCREEN, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
        for y in range(0, WINDOWHEIGHT, CELLSIZE):  # draw horizontal lines
            pygame.draw.line(SCREEN, DARKGRAY, (0, y), (WINDOWWIDTH, y))


# display Press a key to play.'  on the bottom right corner of the screen function
def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    SCREEN.blit(pressKeySurf, pressKeyRect)


# DISPLAY "Snake Game" ON THE START SCREEN
def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 90)
    titleSurf = titleFont.render('Snake Game!', True, DARKGREEN, WHITE)

    while True:
        SCREEN.fill(WHITE)  # set background to white
        titleRect = titleSurf.get_rect()  # create surf where the title will be written on
        titleRect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)  # align center of the screen
        SCREEN.blit(titleSurf, titleRect)  # attach to screen display

        drawPressKeyMsg()  # call function

        if checkForKeyPress():
            pygame.event.get()  # clear event queue
            return
        pygame.display.update()  # update game screen display
        CLOCK.tick(40)  # set game close to 40 fps


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()  # close game

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()  # close game if escape key is clicked
    return keyUpEvents[0].key  # return key even in list


# exit game function
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
    speed = FPS

    # Start the apple in a random place.
    apple = getRandomLocation()

    while RUNNING:  # main game loop
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT  # move left if  a or left key on keyboard is selected
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT  # move right if  d or right key on keyboard is selected
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP  # move up if  wor up key on keyboard is selected
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN  # move down if  s or down key on keyboard is selected
                elif event.key == K_SPACE:
                    pause()  # pause game for 2 send when space key in clicked on the keyboard
                elif event.key == K_p:
                    speed = speed + 1  # increase snake speed by 2 when p is clicked
                    drawSpeed(speed)  # call drawSpeed function to update the speed and value displayed on screen
                elif event.key == K_o:
                    speed = speed - 1  # decrease snake speed by 2 when o is clicked
                    drawSpeed(speed)  # call drawSpeed function to update the speed and value displayed on screen
                elif event.key == K_ESCAPE:
                    terminate()  # exit game

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
            newHead = {'x': snakeCoords[HEAD]['x'],
                       'y': snakeCoords[HEAD]['y'] - 1}  # move the snake by adding a segment in upward direction
        elif direction == DOWN:
            newHead = {'x': snakeCoords[HEAD]['x'],
                       'y': snakeCoords[HEAD]['y'] + 1}  # move the snake by adding a segment in downward direction
        elif direction == LEFT:
            newHead = {'x': snakeCoords[HEAD]['x'] - 1,
                       'y': snakeCoords[HEAD]['y']}  # move the snake by adding a segment in left direction
        elif direction == RIGHT:
            newHead = {'x': snakeCoords[HEAD]['x'] + 1,
                       'y': snakeCoords[HEAD]['y']}  # move the snake by adding a segment in right direction
        snakeCoords.insert(0, newHead)
        SCREEN.fill(BGCOLOR)  # fill screen background color
        drawGrid()  # draw grid
        drawSnake(snakeCoords)  # update snake coordinates
        drawApple(apple)  # draw apple on screen
        drawScore(len(snakeCoords) - 3)  # update score displayed on screen
        drawSpeed(speed)  # display game speed on screen
        pygame.display.update()  # update screen display


# function to randomly position the  the apple of the screen
def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}


# function to draw snake on the screen
def drawSnake(snakeCoords):
    for coord in snakeCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        snakeSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(SCREEN, DARKGREEN, snakeSegmentRect)
        snakeInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(SCREEN, GREEN, snakeInnerSegmentRect)


# function to display Game over message of the screen
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
    pygame.mixer.music.pause()  # pause background game music
    drawPressKeyMsg()  # call drawPressKeyMsg() function
    pygame.display.update()  # update display
    pygame.time.wait(500)
    checkForKeyPress()  # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get()  # clear event queue
            return


# function to display scores on the screen
def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    SCREEN.blit(scoreSurf, scoreRect)


# function to draw apple on the screen
def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    apple = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(SCREEN, RED, apple)


# pause function
def pause():
    font = pygame.font.Font('freesansbold.ttf', 80)
    pauseSurf = font.render('Game Paused!', True, WHITE)
    pauseRect = pauseSurf.get_rect()
    pauseRect.midtop = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
    SCREEN.blit(pauseSurf, pauseRect)
    pygame.mixer.music.pause()
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(5000)
    checkForKeyPress()  # clear out any key presses in the event queue
    pygame.mixer.music.unpause()


# function to display speed on the screen
def drawSpeed(fps):
    speedSurf = BASICFONT.render('Speed: %s' % fps, True, WHITE)
    speedRect = speedSurf.get_rect()
    speedRect.topleft = (WINDOWWIDTH - 120, 40)
    CLOCK.tick(fps)
    SCREEN.blit(speedSurf, speedRect)


if __name__ == '__main__':
    main()
