# My first 'serious' project, nothing special just a little
# Minesweeper game made using the pygame module.
# It may lack some features and may be rather boring
# and bland...but ok, its fine for me, Im still learning.
# A special thanks for my friend Sahil Verma for, ehm, well,
# discussing with me about this project.
import pygame, sys, random, os
from queue import Queue
pygame.init()
flag = pygame.image.load('minesweeper_images/redflag1.png')
grayTile = pygame.image.load('minesweeper_images/graytile.png')
grayerTile = pygame.image.load('minesweeper_images/grayertile.png')
strokeTile = pygame.image.load('minesweeper_images/stroketile.png')
scoreSpaceRect1 = pygame.image.load('minesweeper_images/scoreSpaceRect1.png')
scoreSpaceRect2 = pygame.image.load('minesweeper_images/scoreSpaceRect2.png')
flagCountRect = pygame.image.load('minesweeper_images/flagCountRect.png')
transparentImage = pygame.image.load('minesweeper_images/transparentRect.png')
generalTile1 = pygame.image.load('minesweeper_images/generalTile1.png')
generalTile2 = pygame.image.load('minesweeper_images/generalTile2.png')
restart = pygame.image.load('minesweeper_images/restart.png')
restartHover = pygame.image.load('minesweeper_images/restartHover.png')
reset = pygame.image.load('minesweeper_images/reset.png')
resetHover = pygame.image.load('minesweeper_images/resetHover.png')
mine = pygame.image.load('minesweeper_images/mine.png')
FPSCLOCK = pygame.time.Clock()
FPS = 40
TILESIZE = 27
GAP = 4 # gap btw 2 tiles
PADDING = 8

def main():
    global GRID, BOMBS, SIZE, BOMB, WIN, SCREEN_WIDTH, SCREEN_HEIGHT, TOTAL_FLAGS
    (SCREEN_WIDTH, SCREEN_HEIGHT) = (menuSelection[0][0], menuSelection[0][1])
    SIZE = (menuSelection[1][0], menuSelection[1][1]) # GRID SIZE
    BOMB = menuSelection[2] # no of BOMBS in the game
    TOTAL_FLAGS = BOMB
    WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    if sys.platform in ["WIN32", "WIN64"]:
        os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.display.set_caption('Minesweeper')
    WIN.fill((255, 255, 255))
    running = True
    clicked = False
    noClick = True # to register the first click
    mouseBut = None
    startTime = 0
    resetButHovered = None
    GRID = initalize_tiles()
    while running == True:
        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT or\
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and (pygame.mouse.get_pressed()[0] == 1 or
                                            pygame.mouse.get_pressed()[2] == 1):
                clicked = True
                mouseBut = 0 if pygame.mouse.get_pressed()[0] == 1 else 1
                if resetButHovered != None:
                    main()
                if mouse_hover() and noClick: # will be called only at the first click on a tile
                    if mouseBut == 0:
                        startTime = pygame.time.get_ticks()
                        BOMBS = bomb_gen(pygame.mouse.get_pos())
                        noClick = False
        resetButHovered = score_space(startTime) # manages the score space-> time, flags, reset button etc
        if clicked:
            bombClicked = tile_clicked(mouseBut)
        allTilesOpen = display_tiles() # opens up all the neighbouring tiles, return True if won
        if mouse_hover() and clicked:
            if bombClicked == 'Bomb':
                running = False
                end_animation('YOU LOSE', startTime)
        if allTilesOpen == True:
            running = False
            timeFreeze = (pygame.time.get_ticks() - startTime) // 1000
            end_animation('YOU WIN', timeFreeze)
        pygame.display.flip()
        WIN.fill((255,255,255))
        FPSCLOCK.tick(30)

def score_space(startTime):
    """
    This fun() was added later and is used to manage all the working in the score space.
    Takes in as parameter the time pygame.init() was called to manage the seconds part
    Returns the mouse coordinates if Reset button is hovered, to register a reset if clicked
    """
    resetBut1 = pygame.Rect(179, 30, 115, 39) # Reset buttom for level EASY
    resetBut2 = pygame.Rect(340, 30, 115, 39) # Reset buttom for levels MEDIUM AND HARD
    resetHovered = False
    mouse_pos = pygame.mouse.get_pos()
    if (SCREEN_WIDTH, SCREEN_HEIGHT) == (322,410):
        WIN.blit(scoreSpaceRect1, (PADDING, PADDING, 771, 80))
        if resetBut1.collidepoint(mouse_pos):
            WIN.blit(resetHover, (179, 30))
            resetHovered = True
        else:
            WIN.blit(reset, (179, 30))
        text_to_screen(WIN, PADDING + 30, PADDING + 19, 'FLAGS:', SIZE=18, color=(255, 255, 255))
        text_to_screen(WIN, PADDING + 30, PADDING + 40, 'TIME:', SIZE=18, color=(255, 255, 255))
        text_to_screen(WIN, PADDING + 100, PADDING + 19, TOTAL_FLAGS, SIZE=18, color=(255, 255, 255))
        if startTime == 0:
            text_to_screen(WIN, PADDING + 100, PADDING + 40, startTime, SIZE=18, color=(255, 255, 255))
        else:
            seconds = (pygame.time.get_ticks() - startTime) // 1000
            text_to_screen(WIN, PADDING + 100, PADDING + 40, seconds, SIZE=18, color=(255, 255, 255))

    else:
        WIN.blit(scoreSpaceRect2, (PADDING, PADDING, 771, 80))
        text_to_screen(WIN, PADDING + 40, PADDING + 25, 'FLAGS:', SIZE=20, color=(255, 255, 255))
        text_to_screen(WIN, PADDING + 650, PADDING + 25, 'TIME:', SIZE=20, color=(255, 255, 255))
        text_to_screen(WIN, PADDING + 120, PADDING + 25, TOTAL_FLAGS, SIZE=20, color=(255, 255, 255))
        WIN.blit(reset, (340, 30))
        if resetBut2.collidepoint(mouse_pos):
            WIN.blit(resetHover, (340, 30))
            resetHovered = True
        else:
            WIN.blit(reset, (340, 30))
        if startTime == 0:
            text_to_screen(WIN, PADDING + 710, PADDING + 25, startTime, SIZE=20, color=(255, 255, 255))
        else:
            seconds = (pygame.time.get_ticks() - startTime) // 1000
            text_to_screen(WIN, PADDING + 710, PADDING + 25, seconds, SIZE=20, color=(255, 255, 255))
    if resetHovered:
        return mouse_pos
    else:
        return None

def end_animation(message, timeFreeze):
    """
    This is called when the game is over.
    Accepts message for losing or WINning, timeFreeze to note the time the game was won.
    """
    global menuSelection
    restartBut1 = pygame.Rect(113,27, 116, 43)
    restartBut2 = pygame.Rect(335, 30, 116, 43)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and (pygame.mouse.get_pressed()[0] == 1):
                mouse_pos = pygame.mouse.get_pos()
                if (SCREEN_WIDTH, SCREEN_HEIGHT) == (322, 410):
                    if restartBut1.collidepoint(mouse_pos):
                        menuSelection = main_menu()
                        main()
                else:
                    if restartBut2.collidepoint(mouse_pos):
                        menuSelection = main_menu()
                        main()
        mouse_pos = pygame.mouse.get_pos()
        WIN.fill((255,255,255))
        display_bomb()
        if (SCREEN_WIDTH, SCREEN_HEIGHT) == (322,410):
            WIN.blit(scoreSpaceRect1, (PADDING, PADDING, 771, 80))
            WIN.blit(transparentImage, (104, 120))
            if restartBut1.collidepoint(mouse_pos):
                WIN.blit(restartHover, (113, 27))
            else:
                WIN.blit(restart, (113,27))
            if message == 'YOU LOSE':
                text_to_screen(WIN, 124, 130, message, color=(255, 255, 255), SIZE=19)
            else:
                text_to_screen(WIN, 133, 130, message, color=(255, 255, 255), SIZE=19)
                text_to_screen(WIN, PADDING + 15, PADDING + 30, 'TIME:', SIZE=18, color=(255, 255, 255))
                text_to_screen(WIN, PADDING + 70, PADDING + 30, timeFreeze, SIZE=18, color=(255, 255, 255))
        else:
            WIN.blit(scoreSpaceRect2, (PADDING, PADDING, 771, 80))
            WIN.blit(transparentImage,(327, 160))
            if restartBut2.collidepoint(mouse_pos):
                WIN.blit(restartHover, (335, 30))
            else:
                WIN.blit(restart, (335, 30))
            if message == 'YOU LOSE':
                text_to_screen(WIN, 350, 170, message, color=(255, 255, 255), SIZE=19)
            else:
                text_to_screen(WIN, 358, 170, message, color=(255, 255, 255), SIZE=19)
                text_to_screen(WIN, PADDING + 650, PADDING + 25, 'TIME:', SIZE=20, color=(255, 255, 255))
                text_to_screen(WIN, PADDING + 710, PADDING + 25, timeFreeze, SIZE=20, color=(255, 255, 255))
        pygame.display.update()

def tile_clicked(mouseBut):
    """
    Is called when a tile is clicked. Returns 'bomb' message if a bomb is clicked
    or calls for checking the neighbour checking
    """
    coords = find_clicked_coords()
    if coords != None:
        (x, y) = coords
        if mouseBut == 0:
            if GRID[x][y]['bomb'] == True:
                return 'Bomb'
            else:
                total_clicked_tiles = count_neighbours(coords)
        else:
            if GRID[x][y]['flag'] == False:
                 GRID[x][y]['flag'] = True
            else:
                GRID[x][y]['flag'] = False

def initalize_tiles():
    """
    Called when the  GRID is to be formed. Returns the created GRID
    """
    global GRID
    GRID = [[None for x in range(SIZE[0])] for y in range(SIZE[1])]
    for x in range(SIZE[1]):
        for y in range(SIZE[0]):
            GRID[x][y] = {
                            'state': 'notClicked',
                            'BOMBSAround': 0,
                            'flag': False,
                            'bomb': False,
                            'rect': pygame.Rect(PADDING + y*TILESIZE + y*GAP, PADDING + x*TILESIZE
                                        + x*GAP + 88, TILESIZE, TILESIZE),
                            'coords': (PADDING + y*TILESIZE + y*GAP,
                                        PADDING + x*TILESIZE + x*GAP + 88)
                            }
    return GRID

def display_tiles():
    """
    The main display part, this fun() displays the tiles along with their states.
    Return True is the game is won.
    """
    clicked_tile_count = 0
    global TOTAL_FLAGS
    TOTAL_FLAGS = BOMB
    for x in range(SIZE[1]):
        for y in range(SIZE[0]):
            if GRID[x][y]['state'] == 'notClicked':
                WIN.blit(grayerTile, GRID[x][y]['rect'])
            else:
                WIN.blit(grayTile, GRID[x][y]['rect'])
            if GRID[x][y]['BOMBSAround'] > 0 and GRID[x][y]['bomb'] == False:
                text_to_screen(WIN, GRID[x][y]['coords'][0]+TILESIZE*(1/3),
                               GRID[x][y]['coords'][1]+TILESIZE*(1/7), GRID[x][y]['BOMBSAround'])
            if GRID[x][y]['flag'] == True:
                if GRID[x][y]['state'] == 'notClicked':
                    TOTAL_FLAGS -= 1
                    newFlagPosition = ((GRID[x][y]['coords'][0]+(1/4)*TILESIZE),
                                       GRID[x][y]['coords'][1]+(1/7)*TILESIZE)
                    WIN.blit(flag, newFlagPosition)

            if GRID[x][y]['state'] == 'clicked':
                clicked_tile_count += 1
    if clicked_tile_count == (SIZE[0]*SIZE[1] - BOMB):
        return True

def bomb_gen(pos):
    """
    Used to generate the BOMBS randomly. This is called when the first clicks is called.
    Takes position of the click and return the bomb list.
    """
    (x,y) = find_clicked_coords()
    BOMBSGenerated = 0
    bomb = []
    tiles3x3 = [(x,y), (x-1,y), (x+1,y), (x, y-1), (x, y+1), (x-1, y-1), (x+1, y+1), (x-1, y+1), (x+1, y-1)]
    for index in range(len(tiles3x3)):
        if -1 < tiles3x3[index][0] < SIZE[1] and -1 < tiles3x3[index][1] < SIZE[0]:
            tiles3x3[index] = tiles3x3[index][0]*SIZE[0] + tiles3x3[index][1]
    while BOMBSGenerated < BOMB:
        randomBomb = random.randint(0,SIZE[0]*SIZE[1])
        if not(randomBomb in tiles3x3 or randomBomb in bomb):
            bomb.append(randomBomb)
            BOMBSGenerated += 1
    for x in range(SIZE[1]):
        for y in range(SIZE[0]):
            if (x*SIZE[0]+y) in bomb:
                GRID[x][y]['bomb'] = True
    return bomb

def mouse_hover():
    """
    Returns True when a valid tile is hovered
    """
    coords = find_clicked_coords()
    if coords != None:
        x, y = coords[0], coords[1]
        if GRID[x][y]['state'] == 'notClicked':
            if GRID[x][y]['flag'] == False:
                WIN.blit(grayTile, GRID[x][y]['rect'])
            return True

def find_clicked_coords():
    """
    Returns the coordinates of the tile clicked. This fun() can be made more efficient.
    """
    pos = pygame.mouse.get_pos()
    coords = None
    flag = False
    for x in range(SIZE[1]):
        for y in range(SIZE[0]):
            if GRID[x][y]['rect'].collidepoint(pos):
                coords = (x, y)
                flag = True
                break
        if flag == True:
            break
    return coords

def count_neighbours(coords):
    """
    This fun() is used to unravel or open the neighbouring tiles if valid. In this
    both a queue and recursion is used although its possible to do with only any of the 2.
    Both are used just for the heck of it. Has minimal effect on performance, but probably
    significant effect on readability. May change in the future.
    """
    flag = False
    (x,y) = coords
    queue1 = Queue(maxsize=SIZE[0]*SIZE[1])
    countBomb = 0
    GRID[x][y]['state'] = 'clicked'
    def tile_reveal(coords):
        """
        This fun() is the one called recursively.
        """
        (x,y) = coords
        countBomb = 0
        queue2 = Queue(maxsize=SIZE[0]*SIZE[1])
        for i in range(-1, 2): # this nested for loops is used to check the 8 tiles around it
            for j in range(-1,2):
                (x1,y1) = (x+i, y+j)
                if (-1 < y1 < SIZE[0]) and (-1 < x1 < SIZE[1]) and (i,j) != 0:
                    if GRID[x1][y1]['bomb'] == False:
                        if GRID[x1][y1]['state'] == 'notClicked':
                            queue2.put((x1, y1))
                    else:
                        countBomb += 1
        if countBomb == 0: # if 8 surrounding BOMBSa are not BOMBS they are pushed into the main queue
            while not queue2.empty():
                i = queue2.get(0)
                GRID[i[0]][i[1]]['state'] = 'clicked'
                queue1.put(i)
            GRID[x][y]['BOMBSAround'] = 0
        else:
            GRID[x][y]['BOMBSAround'] = countBomb
        GRID[x][y]['state'] = 'clicked'
        if not queue1.empty():
            tile_reveal(queue1.get(0))
        else:
            return None
    tile_reveal(coords)

def main_menu():
    """
    The main menu fun(), used to register the selections, and returns them.
    """
    global SCREEN_WIDTH, SCREEN_HEIGHT
    (SCREEN_WIDTH, SCREEN_HEIGHT) = (322, 410)
    WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    if sys.platform in ["WIN32", "WIN64"]:
        os.environ["SDL_VIDEO_CENTERED"] = "1"
    WIN.fill((255,255,255))
    levels = {
        'easy' : {
            'windowsize' : (322,410),
            'gridsize' : (10,10)
        },

        'medium' : {
            'windowsize' : (787,410),
            'gridsize' : (25,10)
        },

        'hard' : {
            'windowsize' : (787,534),
            'gridsize'  : (25,14)
        }

    }
    easyRect = pygame.Rect((86, 95, 150, 30))
    mediumRect = pygame.Rect((86, 155, 150, 30))
    hardRect = pygame.Rect((86, 215, 150, 30))
    menuSelection = None
    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] == 1:
                if easyRect.collidepoint(mouse_pos):
                    menuSelection = (levels['easy']['windowsize'], levels['easy']['gridsize'],20,WIN)
                elif mediumRect.collidepoint(mouse_pos):
                    menuSelection = (levels['medium']['windowsize'], levels['medium']['gridsize'],50,WIN)
                elif hardRect.collidepoint(mouse_pos):
                    menuSelection = (levels['hard']['windowsize'], levels['hard']['gridsize'],70,WIN)

        WIN.blit(generalTile1, (86, 95))
        if easyRect.collidepoint(mouse_pos):
            WIN.blit(generalTile2, (86, 95))
        text_to_screen(WIN, 136,100, 'EASY', color=(230, 230, 230), SIZE=18)
        WIN.blit(generalTile1, (86, 155))
        if mediumRect.collidepoint(mouse_pos):
            WIN.blit(generalTile2, (86, 155))
        text_to_screen(WIN, 122, 159, 'MEDIUM', color=(230, 230, 230), SIZE=18)
        WIN.blit(generalTile1, (86, 215))
        if hardRect.collidepoint(mouse_pos):
            WIN.blit(generalTile2, (86, 215))
        text_to_screen(WIN, 135, 219, 'HARD', color=(230, 230, 230), SIZE=18)
        if menuSelection != None:
            return menuSelection
        pygame.display.update()
        FPSCLOCK.tick(30)

def text_to_screen(WIN, x, y, n, font_type='Arial', color=(0,0,0),SIZE=int(TILESIZE *(3/5))):
    """
    This fun() displays the fonts, takes in the detail of it and displays it accordingly.
    x,y is the coordinates, and n is the text.
    """
    text = str(n)
    font = pygame.font.SysFont(font_type, SIZE)
    text = font.render(text, True, color)
    WIN.blit(text, (x, y))

def display_bomb():
    """
    Used to blit the mines or BOMBS
    """
    for x in range(SIZE[1]):
        for y in range(SIZE[0]):
            WIN.blit(grayTile, GRID[x][y]['coords'])
            if (x*SIZE[0]+y) in BOMBS:
                WIN.blit(mine, (GRID[x][y]['coords'][0]+4, GRID[x][y]['coords'][1]+4))

menuSelection = main_menu()
main()
