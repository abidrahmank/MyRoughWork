#a star with color
import time
import pygame
from pygame.locals import *
from operator import itemgetter
class node(object):
    #a very simple class simply used to store information
    def __init__(self, x, y, parent, gscore):
        self.x, self.y = x,y # position on the grid
        self.parent = parent # pointer to a parent node
        self.gscore = gscore # gscore (movement cost)
        self.closed = False  # on closed list? y/n

def getdircost(loc1,loc2):    
    if loc1[0] - loc2[0] != 0 and loc1[1] - loc2[1] != 0:
        return 14 # diagnal movement
    else:
        return 10 # horizontal/vertical movement

def get_h_score(start,end):
    """Gets the estimated length of the path from a node
    using the Manhatten Method."""
    #uses a heuristic function
    #return 0 #used if you want dijkstras (sp?) algorithm
    return (abs(end[0]-start[0])+abs(end[1]-start[1])) * 10

def get_points(node):
    "gets the points to draw an arrow from a child to a parent"
    L = 4
    start =  (node.parent.x,node.parent.y)
    end = ()
    ex =  node.x
    ey =  node.y
    
    if start == (ex-1,ey-1): end = (ex*10-L, ey*10-L)
    elif start ==(ex-1,ey)  : end = (ex*10-L, ey*10)
    elif start == (ex-1,ey+1): end = (ex*10-L, ey*10+L)
    elif start == (ex,ey-1): end = (ex*10, ey*10-L)
    elif start == (ex,ey+1): end = (ex*10, ey*10+L)
    elif start == (ex+1,ey+1): end = (ex*10+L, ey*10+L)
    elif start == (ex+1,ey): end = (ex*10+L, ey*10)
    elif start == (ex+1,ey-1): end = (ex*10+L, ey*10-L)
    return ((ex*10+5,ey*10+5),(end[0]+5,end[1]+5))

def draw_arrow((start,end), screen):
    "Calulates how to draw an arrow"
    #each arrow starts at a child and points to its parent
    
    pygame.draw.line(screen, (255,255,255),(start),(end))
    sides = ((0,0),(0,0))
    
    if start[0] > end[0] and start[1] == end[1]:#arrow left
        sides = ((2,-2),(2,2))
    if start[0] == end[0] and start[1] > end[1]:#arrow up
        sides = ((-2,2),(2,2))
    if start[0] < end[0] and start[1] == end[1]:#arrow right
        sides = ((-2,2),(-2,-2))
    if start[0] == end[0] and start[1] < end[1]:#arrow down
        sides = ((-2,-2),(2,-2))
    if start[0] > end[0] and start[1] > end[1]:#arrow up/left
        sides = ((2,0),(0,2))
    if start[0] < end[0] and start[1] > end[1]:#arrow up/right
        sides = ((-2,0),(0,2))
    if start[0] < end[0] and start[1] < end[1]:#arrow down/right
        sides = ((-2,0),(0,-2))
    if start[0] > end[0] and start[1] < end[1]:#arrow down/left
        sides = ((2,0),(0,-2))
                 
    pygame.draw.line(screen, (255,255,255),(end),(end[0]+sides[0][0],
                                                  end[1]+sides[0][1]))
    
    pygame.draw.line(screen, (255,255,255),(end),(end[0]+sides[1][0],
                                                  end[1]+sides[1][1]))

def create_path(s, end, grid1,grid2,screen,IsBlack, isSecondLayer):
    "Creates the shortest path between s (start) and end."
    if isSecondLayer == False:
        grid = grid1
    else:
        grid = grid2
    
    # the ons list is a 2d list of node status
    # None means the node has not been checked yet
    # a node object for a value means it is on the open list
    # a False value means that it is on the closed list
    ons = [[None for y in xrange(len(grid[x]))] for x in xrange(len(grid))]

    #n is the current best node on the open list, starting with the initial node
    n = node(s[0],s[1], None,0)

    #we store the fscores of the nodes and the nodes themselves in a binary heap
    
    #we don't want a binary heap here because it seems to be less consistent (don't know why exactly)
    #than a simple list.
    count = 0
    openl = []
    closedList = []#list to be redrawn to green
    geth = get_h_score
    start_time = time.time()
    while (n.x, n.y) != end:

        #search adjacent nodes
        #if the node is already on the open list, then
        #and change their pointer the the current node
        #if their path from current node is shorter than their
        #previous path from previous parent
        #if the node is not on the open list and is not a wall,
        #add it to the open list
        for x in xrange(n.x -1, n.x +2):
            for y in xrange(n.y -1 , n.y + 2):
                #the checked node can't be our central node
                if (x,y) != (n.x,n.y):
				#To ignore the diagonal nodes
				    if x == n.x or y == n.y:
						if grid[x][y] == True:	
                                                    #if the node is not on the closed list or open list
                                                    if ons[x][y] != None:
                                                            if ons[x][y].closed == False:
                                                                    #get cost of the new path made from switching parents
                                                                    #new_cost = getdircost((n.x,n.y),(x,y)) + n.gscore

                                                                    # if the path from the current node is shorter
                                                                    #if new_cost <= ons[x][y].gscore:
                                                                            #h = geth((x,y),end)
                                                                            #n + h

                                                                            
                                                                            #find the index of the node
                                                                            #to change in the open list
                                                                            index = openl.index([ons[x][y].gscore,
                                                                                                                     ons[x][y]])

                                                                           

                                                    #if the node is not a wall and not on the closed list
                                                    #then simply add it to the open list
                                                    else:

                                                                    
                                                                    h = geth((x,y),end)
                                                                    
                                                                    #movement score gets the direction cost
                                                                    #added to the parent's directional cost
                                                                    g = getdircost((n.x,n.y),(x,y)) + n.gscore

                                                                   

                                                                
                                                                    
                                                                    length = len(openl)
                                                                    
                                                                    ons[x][y] = node(x, y, n, g)
                                                                    #update the ons list and the
                                                                    #fscore list in the list
                                                                    #openl[length][0] = g
                                                                    #ons[x][y] = openl[length][1]
                                                                    openl.append([g,ons[x][y]])
                                                                    #drawing blue nodes
                                                                    if isSecondLayer != True and grid2[x][y] == True:
                                                                        pygame.draw.rect(screen,(0,0,255),(x*10,y*10,10,10))
                                                                        #draw_arrow(get_points(ons[x][y]),screen)
                                                                        pygame.display.update(x*10,y*10,10,10)
                                                                    elif isSecondLayer == True and grid1[x][y] == True:
                                                                        pygame.draw.rect(screen,(0,0,255),(x*10,y*10,10,10))
                                                                        #draw_arrow(get_points(ons[x][y]),screen)
                                                                        pygame.display.update(x*10,y*10,10,10)
        #if the length of the open list is zero(all nodes on closed list)
        #then return an empty path list

        #print "cells_processed = ", len(openl)                                                              
        if len(openl) == 0: 
            n = None
            break

        ##############
        #openl = sorted(openl,key = itemgetter(0,1))
        #n = min(openl)
        n = openl.pop(0)
        count = count + 1
        #openl.remove(n)
        n = n[1]
        ##############

        if isSecondLayer != True and grid2[n.x][n.y] == True:
            
            #draw some stuff
            pygame.draw.rect(screen, (255,255,255),(s[0]*10,s[1]*10,10,10))
            pygame.display.update(s[0]*10,s[1]*10,10,10)
            #drawing red nodes
            pygame.draw.rect(screen,(255,100,0),(n.x*10,n.y*10,10,10))
            #draw_arrow(get_points(n),screen)
            pygame.time.wait(20)
            pygame.display.update(n.x*10,n.y*10,10,10)
        elif isSecondLayer == True and grid1[n.x][n.y] == True:
            
            #draw some stuff
            pygame.draw.rect(screen, (255,255,255),(s[0]*10,s[1]*10,10,10))
            pygame.display.update(s[0]*10,s[1]*10,10,10)
            #drawing red nodes
            pygame.draw.rect(screen,(255,100,0),(n.x*10,n.y*10,10,10))
            #draw_arrow(get_points(n),screen)
            pygame.time.wait(20)
            pygame.display.update(n.x*10,n.y*10,10,10)        
        #remove from the 'closed' list
        ons[n.x][n.y].closed = True

	closedList.append(n);
	

    #Now we have our path, we just need to trace it
    #trace the parent of every node until the beginning is reached
    openListCount = len(openl)
    closedListCount = len(closedList)
    count = count +openListCount
    print "processed cells", count
    moves = []
    isPathFound  = False # flag used for multi layer
    if n!= None:
        while (n.x,n.y) != s:
            moves.insert(0,(n.x,n.y))
	    if(IsBlack): # second layer
                pygame.draw.rect(screen,(255,255,0),(n.x*10,n.y*10,10,10))
	    elif grid2[n.x][n.y] == True:
                pygame.draw.rect(screen,(200,200,200),(n.x*10,n.y*10,10,10))
            pygame.display.update(n.x*10-20,n.y*10-20,40,40)
	    closedList.remove(n)
	    closedListCount = len(closedList)
            pygame.time.wait(20)
            n = n.parent#trace back to the previous node
	#pygame.time.wait(10)
        end_time = time.time()
        print "total time taken : " , end_time - start_time
        
    # Turn back all red and blue squares back to green
    #if isSecondLayer != True:
    for i in range (0, openListCount):
    
        n = min(openl)
        #n = n[2]
        
        openl.remove(n)
        n = n[1]
        if grid2[n.x][n.y] == True and grid1[n.x][n.y] == True:
            pygame.draw.rect(screen,(100,255,100),(n.x*10,n.y*10,10,10))
            pygame.display.update(n.x*10,n.y*10,10,10)	
    
    for i in range (0, closedListCount):
        
        n = min(closedList)

        closedList.remove(n)
        if grid2[n.x][n.y] == True and grid1[n.x][n.y] == True:
            pygame.draw.rect(screen,(100,255,100),(n.x*10,n.y*10,10,10))
            pygame.display.update(n.x*10,n.y*10,10,10)	
    
    
    
    
    
    
    
    return moves 
