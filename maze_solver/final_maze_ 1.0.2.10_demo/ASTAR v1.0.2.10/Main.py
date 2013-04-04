""" GUI support file for the A* implementation

Green color is the background
Brown color corresponds to walls

When a path is created:
    Blue squares: nodes on the open list
    Red squares: nodes on the closed list
    Grey squares: shows the best path in 1st layer
    Yellow squares: shows the best path in 2nd layer

"""

import pygame
import sys
from pygame.locals import *
from astarcolor import create_path

########################################################################################
#
#                       class SOURCE                                                   #               
#
########################################################################################

class Source(object):
    def __init__(self, loc,image, screen):
        self.rloc = (loc[0]*10, loc[1]*10)  #'real' location on screen
        self.loc = loc                      # (x,y) position
        self.path = []                      # path to the target
        self.image = image                  # shows image of source
        self.screen = screen

    def set_path(self, grid1,grid2, end,targetImage):
        """
        function        : sets a path for the source to follow
        @ grid1         : first layer
        @ grid2         : second layer
        @ end           : target node
        @ targetImage   : image of target
        """

        #create a path using A* 
        self.path = create_path(self.loc,end,grid1,grid2,self.screen,False,targetImage)
        grid1[self.rloc[0]/10][self.rloc[1]/10] = False # make the source as a wall for next path
        selfPathLength = len(self.path)

        #To delete the already formed line to avoid from further calculation
        for i in range(0,selfPathLength):               
            grid1[self.path[i][0]][self.path[i][1]] = False
        
        if selfPathLength == 0:
            # if no path found, draw the grid
            for r in xrange(1,100):
                pygame.draw.line(self.screen,(0,0,0),(r*10,0),(r*10,1000),1)
                pygame.draw.line(self.screen,(0,0,0),(0,r*10),(1000,r*10),1)
                pygame.display.flip()

            # try to find the path in second layer
            self.path = create_path(self.loc,end,grid1,grid2,self.screen,True,targetImage)
            grid2[self.rloc[0]/10][self.rloc[1]/10] = False   # make the source as a wall for next path

            selfPathLength = len(self.path)
            
            #To delete the already formed line to avoid from further calculation
            for i in range(0,selfPathLength):
                grid2[self.path[i][0]][self.path[i][1]] = False
        
        pygame.display.flip()

    def draw_source(self):
        """draw the source on the screen, based on his 'real' coordinates"""
        self.screen.blit(self.image, (self.rloc[0], self.rloc[1]))

###########################################################################################################
 
def creategrid(dim):
    """ This function makes the screen to a 2D array of small squares """
    x,y = dim[0]/10-2, dim[1]/10-2
    grid = []
    for gx in xrange(x+2):
        row = []
        # make border of grid as walls 
        for gy in xrange(y+2):
            if gx == 0 or gy == 0 or gx == x+1 or gy == y+1:
                row.append(False)
            else:
                row.append(True)
        grid.append(row)
    return grid

def update(screen, grid, source = None):
    """ redraw the source, then update the screen """
    if source != None:
        pygame.draw.rect(screen, (100,255,100),(source.rloc[0],source.rloc[1],10,10))
        source.draw_source()
    # draw the grid
    for r in xrange(1,100):
        pygame.draw.line(screen,(0,0,0),(r*10,0),(r*10,1000),1)
        pygame.draw.line(screen,(0,0,0),(0,r*10),(1000,r*10),1)
    pygame.display.update()

def draw_all(screen, grid, source = None):
    """Draws the entire screen"""
    for x in xrange(len(grid)):
        for y in xrange(len(grid[x])):
            #draw either walls or grass
            if grid[x][y] == True:
                pygame.draw.rect(screen, (100,255,100), (x*10, y * 10, 10, 10))
            elif grid[x][y] == False:
                pygame.draw.rect(screen, (150,100,50) , (x*10, y * 10, 10, 10))

    for r in xrange(1,100):
        pygame.draw.line(screen,(0,0,0),(r*10,0),(r*10,1000),1)
        pygame.draw.line(screen,(0,0,0),(0,r*10),(1000,r*10),1)
    #draw the source and update the entire screen
    if source != None:
        source.draw_source()
    pygame.display.flip()


def change(screen, grid, deleting, mx, my):
    "either draws or erases a wall"
    grid[mx][my] = deleting
    if deleting: pygame.draw.rect(screen,(100,255,100),(mx*10, my*10,10,10))
    else       : pygame.draw.rect(screen,(150,100,50) ,(mx*10, my*10,10,10))
    pygame.display.update(mx*10, my * 10, 10, 10)
    return grid

def main(dim):
    """ main program to run """
    
    #load the source and target images
    image = pygame.image.load('source.bmp')
    targetImage = pygame.image.load("targ.bmp")

    # initialise pygame display
    pygame.init(); pygame.display.set_caption("A* Maze")
    screen = pygame.display.set_mode((dim[0], dim[1])) #initialize the screen for the display

    # create first and second layers
    grid1 = creategrid(dim)
    grid2 = creategrid(dim)
    
    source = None #Initialize the source object
    
    #we aren't drawing or deleting. This is for drawing/deleting the walls
    drawing = deleting = False

    #draw everything on the screen
    draw_all(screen,grid1)

    startingNode = True    # This flag decides first click to source and next to target
    
    clock = pygame.time.Clock()  # provides delay functions

    #main loop
    while True:
        
        clock.tick(1000)#limits the speed of the operation

        events = pygame.event.get() #get the inputs
        for e in events:            #processes key/mouse inputs
            
            #getting the mouse position
            mousex = (pygame.mouse.get_pos()[0])/10
            mousey = (pygame.mouse.get_pos()[1])/10
            
            if e.type == MOUSEBUTTONDOWN:
                #left mouse button pressed
                #An active node at which a left click occured will be considered as a source/target node.  
                if pygame.mouse.get_pressed()[0] == 1 and startingNode == True and grid1[mousex][mousey]!= False:
                    startingNode = False
                    source = Source((mousex,mousey),image, screen)
                    update(screen, grid1,source)
                    continue
                
                #right mouse button pressed, right click will draw a wall or delete
                elif pygame.mouse.get_pressed()[2] == 1:
                    #if we click on a wall, then we are deleting, else we start drawing
                    if grid1[mousex][mousey] == True:
                        drawing = True
                    else:
                        deleting = True

                # next left click select target and set a new path for the source
                elif source != None and pygame.mouse.get_pressed()[0] == 1:
                    if grid1[mousex][mousey]!= False and (mousex,mousey)!=source.loc:
                        screen.blit(targetImage, (mousex*10,mousey*10))
                        update(screen, grid1,source)
                        source.set_path(grid1,grid2,(mousex,mousey),targetImage)
                        startingNode = True

            #stop deleting/drawing walls
            elif e.type == MOUSEBUTTONUP:
                drawing = deleting = False

            #escape to quit
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE: pygame.quit();  sys.exit()
        
        if source != None:
            update(screen, grid1, source)

        if   drawing  == True: grid1 = change(screen, grid1,False, mousex,mousey)
        elif deleting == True: grid1 = change(screen, grid1, True, mousex,mousey)

if __name__ == "__main__":
    main((1000,700))
