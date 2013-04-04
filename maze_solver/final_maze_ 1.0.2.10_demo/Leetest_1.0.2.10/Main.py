import pygame
import sys
from pygame.locals import *

from LeeColor import create_path



#This file gives a much more indepth look at the A* algorithm, allowing
#the user to see exacly how a search is made, and how paths are traced
#When a path is created:
#Blue squares: nodes on the open list
#Red squares: nodes on the closed list
#Grey/black squares: shows the best path



#each square has an arrow pointing to its parent square

class Source(object):
    def __init__(self, loc, image, screen):
        self.rloc = (loc[0]*10, loc[1]*10)#'real' location
        self.loc, self.path = loc, []
        self.image = pygame.image.load(image)
        self.goal = ()
        self.theta = self.changex = self.changey = 0
        self.wait = 0
        self.screen = screen

    def set_path(self, grid1,grid2, end,IsBlack):
        "sets a path for the source to follow"
        self.goal = end # reset the goal

        #create a path using A* 
        #draw stuff as well in these functions
        self.path = create_path(self.loc,end,grid1,grid2,self.screen,False,False)
        
        
        grid1[self.rloc[0]/10][self.rloc[1]/10] = False   # make the source as a wall for next path
        selfPathLength = len(self.path)
        for i in range(0,selfPathLength):#To delete the already formed line to avoid from further calculation
            grid1[self.path[i][0]][self.path[i][1]] = False
        
        if selfPathLength == 0:
            self.path = create_path(self.loc,end,grid1,grid2,self.screen,True,True)
            grid2[self.rloc[0]/10][self.rloc[1]/10] = False   # make the source as a wall for next path
            selfPathLength = len(self.path)
            for i in range(0,selfPathLength):#To delete the already formed line to avoid from further calculation
                grid2[self.path[i][0]][self.path[i][1]] = False
        
        pygame.display.flip()#update the screen

    def draw_source(self):
        #blit the dude on the screen, based on his 'real' coordinates
        self.screen.blit(self.image, (self.rloc[0], self.rloc[1]))
        

def creategrid(dim):
    #This function makes the screen to a 2D array of small squares
    x,y = dim[0]/10-2, dim[1]/10-2
    grid = []
    for gx in xrange(x+2):
        row = []
        for gy in xrange(y+2):
            if gx == 0 or gy == 0 or gx == x+1 or gy == y+1:
                row.append(False)
            else: row.append(True)
        grid.append(row)
    return grid

def update(screen, grid, source = None):
    #'erase' the source, draw him, then update the screen
    if source != None:
        pygame.draw.rect(screen, (100,255,100),(source.rloc[0],source.rloc[1],10,10))
        source.draw_source()
    #pygame.display.update((source.rloc[0]-20),(source.rloc[1]-20),40, 40)
    for r in xrange(1,100):
        pygame.draw.line(screen,(0,0,0),(r*10,0),(r*10,1000),1)
        pygame.draw.line(screen,(0,0,0),(0,r*10),(1000,r*10),1)
    pygame.display.update()

def draw_all(screen, grid, source = None):
    "Draws the entire screen"
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
    #initialize pygame, the display caption, and the screen
    pygame.init(); pygame.display.set_caption("A* Maze")
    grid1 = creategrid(dim)
    grid2 = creategrid(dim) # second layer.
    screen = pygame.display.set_mode((dim[0], dim[1]))#initialize the screen for the display
    source = None #Initialize the source object 
    #we aren't drawing or deleting. This is for drawing/deleting the walls
    drawing = deleting = False
    #draw everything on the screen
    draw_all(screen,grid1)
    startingNode = True
    IsBlack = True
    clock = pygame.time.Clock()
    while True:#main loop
        clock.tick(1000)#limits the speed of the operation

        events = pygame.event.get()#get the inputs
        for e in events: #processes key/mouse inputs
            #getting the mouse position
            mousex = (pygame.mouse.get_pos()[0])/10
            mousey = (pygame.mouse.get_pos()[1])/10

            
            
            if e.type == MOUSEBUTTONDOWN:
                #left mouse button pressed
                #An active node at at which a left click occured will be considered as a source/target node.  
                if pygame.mouse.get_pressed()[0] == 1 and startingNode == True and grid1[mousex][mousey]!= False:
                    startingNode = False
                    source = Source((mousex,mousey),"source.bmp", screen)
                    update(screen, grid1,source)
                    continue
                #right mouse button pressed
                #right click will draw a wall or delete
                elif pygame.mouse.get_pressed()[2] == 1:
                    #if we start by seleting a wall, then we are deleting
                    #else we start drawing
                    if grid1[mousex][mousey] == True:
                        drawing = True
                    else:
                        deleting = True

                #set a new path for the source
                elif source != None and pygame.mouse.get_pressed()[0] == 1:
                    if grid1[mousex][mousey]!= False and (mousex,mousey)!=source.loc:
                        update(screen, grid1,source)#redraw everythin
                        IsBlack = not(IsBlack)
                        source.set_path(grid1,grid2,(mousex,mousey),IsBlack)
                        startingNode = True
            #stop deleting/drawing walls
            elif e.type == MOUSEBUTTONUP:drawing = deleting = False

            elif e.type == KEYDOWN:

                #escape to quit
                if e.key == K_ESCAPE: pygame.quit();  sys.exit()

        
        
        if source != None:
            update(screen, grid1, source)

        if   drawing  == True: grid1 = change(screen, grid1,False, mousex,mousey)
        elif deleting == True: grid1 = change(screen, grid1, True, mousex,mousey)


if __name__ == "__main__": main((1000,700))
