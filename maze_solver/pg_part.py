import pygame as pg
import numpy as np
from astar import *

black = (0,0,0)
green = (0,255,0)
red = (255,0,0)
blue = (0,0,255)
white = (255,255,255)

pg.init()

def draw_grid(surface):
    size = surface.get_size()[0]
    for r in xrange(1,size):
        pg.draw.line(surface,black,(r*10,0),(r*10,size),1)
        pg.draw.line(surface,black,(0,r*10),(size,r*10),1)

class Screen(object):
    def __init__(self,dim,block_size):
        self.dim = dim
        self.block_size = block_size
        self.display = pg.display.set_mode(dim,0,32)
        pg.display.set_caption("Astar algorithm")
        self.display.fill(white)
        draw_grid(self.display)
        pg.display.update()

    def draw_path(self,path,wall):
        for cell in path:
            cell_rect = pg.rect.Rect(cell.x*10,cell.y*10,10,10)
            pg.draw.rect(self.display,red,cell_rect)
        for cell in wall:
            cell_rect = pg.rect.Rect(cell[0]*10,cell[1]*10,10,10)
            pg.draw.rect(self.display,blue,cell_rect)
        pg.display.update()
        #real = pg.transform.flip(self.surface,False,True)
        #return real

if __name__ == "__main__":
    start = Cell(20,20,True)
    test = Cell(5,5,True)
    target = Cell(49,49,True)
    walls = ((0, 5), (1, 0), (1, 1), (1, 5), (2, 3),(3, 1), (3, 2), (3, 5), (4, 1), (4, 4), (5, 1))
    #walls = []
    #walls = ((0,1),(1,1),(1,0))
    grid = Grid(500)

    grid.init_grid(start,target,walls)
    import time
    t = time.time()
    path = lee_process(start,target,grid)
    print time.time() - t
    #print path
    screen = Screen((500,500),10)
    screen.draw_path(path,walls)
    pg.time.delay(2000)
    pg.quit()
    

