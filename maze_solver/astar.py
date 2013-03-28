# astar.py
# trying draft version

import time, sys, heapq
import numpy as np
import pygame as pg
from pg_part import *
#import cv2
from operator import attrgetter
from pygame.locals import *


''' source - red
    wall   - black
    target - blue
    path   - green '''
# --------------------------------------------------------------------------------------- #
# -------------------------          class CELL              ---------------------------- #
# --------------------------------------------------------------------------------------- #

class Cell(object):
    #a very simple class simply used to store information
    def __init__(self, x,y,reachable):
        self.x, self.y = x,y
        self.g, self.h, self.f = 0,0,0
        self.reachable = reachable
        self.parent = None

    def cell_xy(self):
        return (self.x,self.y)
    
    def cell_info(self):
        return "({0},{1}), g = {2}, h= {3}, f= {4}, wall = {5}, parent = {6})".format(self.x,self.y,self.g,self.h,self.f,self.reachable,self.parent)

    def __str__(self):
        return "Cell({0},{1})".format(self.x,self.y)
# --------------------------------------------------------------------------------------- #
# -------------------------          class GRID              ---------------------------- #
# --------------------------------------------------------------------------------------- #
class Grid(object):
    def __init__(self,grid_size):
        self.grid_size = grid_size
        self.open_cells = []
        self.closed_cells = set()
        self.cells = []
        self.cell_array = []
        

    def init_grid(self,walls=[]):
        #self.start = start
        #self.end = end
        self.walls = walls
        for i in xrange(self.grid_size):
            for j in xrange(self.grid_size):
                if (i,j) in self.walls:
                    reachable = False
                else:
                    reachable = True

                self.cells.append(Cell(i,j,reachable))
        self.cell_array = np.array(self.cells).reshape((self.grid_size,self.grid_size))

    def cell_from_xy(self,x,y):
        """ get the cell from its x,y values"""
        return self.cell_array.item((x,y))

    def get_h(self,cell,target = Cell(10,10,True)):
        """Gets the estimated length of the path from a node
        using the Manhatten Method.
        @param cell - cell in consideration
        @param end_cell - target
        @returns the manhattan distance."""
    
        return ( abs(cell.x-target.x) + abs(cell.y-target.y) )

    def get_adjcells(self,cell):
        """ gets the adjacent cells of a cell"""
        adj_cells = []
        cells_xy = []
        if cell.x > 0:
            adj_cells.append(self.cell_array.item((cell.x-1,cell.y)))
        if cell.x < self.grid_size - 1:
            adj_cells.append(self.cell_array.item((cell.x+1,cell.y)))
        if cell.y > 0:
            adj_cells.append(self.cell_array.item((cell.x,cell.y-1)))
        if cell.y < self.grid_size - 1:
            adj_cells.append(self.cell_array.item((cell.x,cell.y+1)))
        return adj_cells

    def minimum_f_cell(self):
        """ return the cell with minimum f_score from open cells"""
        return sorted(self.open_cells,key = lambda cell: cell.f)[0]
    





# --------------------------------------------------------------------------------------- #
# -------------------------          other functions         ---------------------------- #
# --------------------------------------------------------------------------------------- #

def retrace_path(target,closed_cells):
    path = []
    closed_cells = list(closed_cells)
    cell = target
    while (True):
        closed_cells.remove(cell)
        path.append(cell)
        cell = cell.parent
        if cell == None : # break loop if start cell
            #path.append(cell)
            break
    return path
    #for x in path:
    #    print x, x.parent

    

# --------------------------------------------------------------------------------------- #
# -------------------------          original A* function    ---------------------------- #
# --------------------------------------------------------------------------------------- #

def process(start,target,grid,walls,screen):
    
    """ Original A* algorithm """

##    pg.init(); pg.display.set_caption("A* Maze")
##    #grid = creategrid(dim)
##    screen = pg.display.set_mode((1000,700))
##    
##    screen.fill((255,255,255))
##    for r in xrange(1,100):
##        pg.draw.line(screen,(0,0,0),(r*10,0),(r*10,1000),1)
##        pg.draw.line(screen,(0,0,0),(0,r*10),(1000,r*10),1)
##    for wall in walls:
##        x,y = wall
##        rect = pg.Rect(x*10,y*10,10,10)
##        pg.draw.rect(screen,(0,0,0),rect)
##    pg.display.update()


    
    found_path = False
    route = []
    start.h = grid.get_h(start,target)
    start.g = 0
    start.f = 2*start.h+start.g
    grid.open_cells.append(start)                       # first push start to open_cells
    cells_processed = 1
    
    while(grid.open_cells != []):       # if open_cells is not empty
        #
        # Below line is the sorting according to f and h
        #
        grid.open_cells = sorted(grid.open_cells,key = attrgetter('f','h','y'))
        current_cell = grid.open_cells.pop(0)
        grid.closed_cells.add(current_cell)             # add start to closed cells
        color = np.random.randint(0,256,3).tolist()
        draw_cell(screen,current_cell,(0,0,255))
        
        adj_cells = grid.get_adjcells(current_cell) # get the adjacent cells of start and put them in open cells
        if found_path == True:
            break

        for cell in adj_cells:
            if cell.cell_xy() == target.cell_xy() and found_path == False: # if cell is target, job done
                target.parent = current_cell
                grid.closed_cells.add(target)
                route = retrace_path(target,grid.closed_cells)
                for cell in route:
                    draw_cell(screen,cell,(0,255,0))
                cells_processed += 1
                found_path = True
                
            elif cell not in grid.closed_cells and cell.reachable == True and found_path == False: # or check if cell in closed_cells or walls
                draw_cell(screen,cell,(255,0,0))
                cell.h = grid.get_h(cell,target)                # update the values of cell
                cell.g = current_cell.g+1
                cell.f = 2*cell.h + cell.g
                
                if cell not in grid.open_cells:                 # if cell not in open_cells, add it, update parent
                    cells_processed += 1
                    grid.open_cells.append(cell)
                    cell.parent = current_cell
                    
                else:                                           # or update the already present one.
                    old_cell = grid.open_cells[grid.open_cells.index(cell)] # present is the cell already in open cells
                    if cell.f < old_cell.f:                     # if new.f < old.f, replace old.parent by new.parent
                        old_cell.parent = current_cell                   
        pg.time.delay(50)



    print "cells_processed = ", cells_processed

    
    return route


def MainGui():
    #walls = ((0, 5), (1, 0), (1, 1), (1, 5), (2, 3),(3, 1), (3, 2), (3, 5), (4, 1), (4, 4), (5, 1),(19,20),(20,19))
    walls = []
    #walls = ((0,1),(1,1),(1,0))
    grid = Grid(500)

    #grid.init_grid(walls)
    pg.init(); pg.display.set_caption("A* Maze")
    #grid = creategrid(dim)
    screen = pg.display.set_mode((1000,700))
    
    screen.fill((255,255,255))
    for wall in walls:
        x,y = wall
        rect = pg.Rect(x*10,y*10,10,10)
        pg.draw.rect(screen,(0,0,0),rect)

    draw_grid(screen)
    
    pg.display.update()    
    start_track = False
    while True:
        events = pg.event.get()

        if start_track == False:
            for e in events:
                mousex = (pg.mouse.get_pos()[0])/10
                mousey = (pg.mouse.get_pos()[1])/10
                if e.type == KEYDOWN:
                    if e.key == K_ESCAPE:
                        pg.quit()
                        sys.exit()
                    elif (e.key == K_s):        # hold mouse and press s to set source
                        start = Cell(mousex,mousey,True)
                        draw_cell(screen,start,(255,0,0))
                    elif (e.key == K_t):        # hold mouse and press t to set target
                        target = Cell(mousex,mousey,True)
                        draw_cell(screen,target,(0,0,255))
                    elif (e.key == K_SPACE):    # press SPACE to find the track
                        start_track = True
                    elif (e.key == K_c):        # press c to clear window
                        screen.fill((255,255,255))
                        draw_grid(screen)
                        pg.display.update()

                elif e.type == MOUSEBUTTONDOWN:
                    if pg.mouse.get_pressed()[0] == 1:
                        walls.append([mousex,mousey])
                        pg.draw.rect(screen,(0,0,0),(mousex*10,mousey*10,10,10))
                        

        if start_track == True:  
            grid.init_grid(walls)
            path = process(start,target,grid,walls,screen)
            start_track = False
            del start,target
            #grid.open_cells = [],grid.closed_cells = set()
        
        draw_grid(screen)
        
        pg.display.update()





     

    
if __name__ == '__main__':
    #start = Cell(0,0,True)
    #test = Cell(5,5,True)
    #target = Cell(20,20,True)
    # walls = ((0, 5), (1, 0), (1, 1), (1, 5), (2, 3),(3, 1), (3, 2), (3, 5), (4, 1), (4, 4), (5, 1),(19,20),(20,19))
    # #walls = []
    # #walls = ((0,1),(1,1),(1,0))
    # grid = Grid(500)

    # grid.init_grid(walls)

    #path = process(start,target,grid,walls)

    #print path

    MainGui()






