import time
import pygame
from pygame.locals import *
from operator import itemgetter

########################################################################################
#
#                       class NODE                                                     #               
#                   structure of a cell
########################################################################################
class node(object):
    # structure to store information about a cell
    def __init__(self, x, y, parent, gscore, fscore):
        self.x, self.y = x,y # position on the grid
        self.parent = parent # pointer to a parent node
        self.gscore = gscore # gscore (movement cost)
        self.fscore = fscore # h score(estimated cost)
        self.closed = False  # on closed list? y/n

def getdircost(loc1,loc2):
    """ cost to next cell """
    if loc1[0] - loc2[0] != 0 and loc1[1] - loc2[1] != 0:
        return 15 # diagonal movement
    else:
        return 10 # horizontal/vertical movement

def geth(start,end):
    """Gets the estimated length of the path from a node
    using the Manhatten Method."""
    return (abs(end[0]-start[0])+abs(end[1]-start[1])) * 10

def get_points(node):
    "gets the points to draw an arrow from a child to a parent"
    L = 4
    start =  (node.parent.x,node.parent.y)
    end = ()
    ex =  node.x
    ey =  node.y
  
    if start ==(ex-1,ey)  : end = (ex*10-L, ey*10)
    elif start == (ex,ey-1): end = (ex*10, ey*10-L)
    elif start == (ex,ey+1): end = (ex*10, ey*10+L)
    elif start == (ex+1,ey): end = (ex*10+L, ey*10)

    return ((ex*10+5,ey*10+5),(end[0]+5,end[1]+5))

def draw_arrow((start,end), screen):
    "draw an arrow"
    #each arrow starts at a child and points to its parent
    pygame.draw.line(screen, (255,255,255),(start),(end))
    sides = ((0,0),(0,0))

    # draw arrow heads    
    if start[0] > end[0] and start[1] == end[1]:#arrow left
        sides = ((2,-2),(2,2))
    if start[0] == end[0] and start[1] > end[1]:#arrow up
        sides = ((-2,2),(2,2))
    if start[0] < end[0] and start[1] == end[1]:#arrow right
        sides = ((-2,2),(-2,-2))
    if start[0] == end[0] and start[1] < end[1]:#arrow down
        sides = ((-2,-2),(2,-2))
                 
    pygame.draw.line(screen, (255,255,255),(end),(end[0]+sides[0][0],end[1]+sides[0][1]))
    pygame.draw.line(screen, (255,255,255),(end),(end[0]+sides[1][0],end[1]+sides[1][1]))

def create_path(s, end, grid1,grid2,screen,isSecondLayer,targetImage):
    "Creates the shortest path between s (start) and end."
    if isSecondLayer == False:
        grid = grid1
    else:
        grid = grid2
    
    # the node_status_array list is a 2d list of node status
    # None means the node has not been checked yet
    # a node object for a value means it is on the open list
    # a False value means that it is on the closed list
    node_status_array = [[None for y in xrange(len(grid[x]))] for x in xrange(len(grid))]

    #n is the current best node on the open list, starting with the source
    n = node(s[0],s[1], None,0, 0)

    openl = []
    closedList = []         #list to be redrawn to green
    count = 0               #stores number of cells processed
    start_time = time.time()

    while (n.x, n.y) != end:
        # search for adjacent cells
        for x in xrange(n.x -1, n.x +2):
            for y in xrange(n.y -1 , n.y + 2):
                #the checked node can't be our central node
                if (x,y) != (n.x,n.y):
		    #To ignore the diagonal nodes
                    if x == n.x or y == n.y:
                        # if checked node is not a wall
                        if grid[x][y] == True:	

                            if node_status_array[x][y] != None:     # is node either in openlist or closed list
                                if node_status_array[x][y].closed == False: # is node not in closed list

                                    #get cost of the new path made from switching parents
                                    new_cost = getdircost((n.x,n.y),(x,y)) + n.gscore

                                    # if the path from the current node is shorter
                                    if new_cost <= node_status_array[x][y].gscore:
                                        h = geth((x,y),end)
                                        newf = new_cost + h
                                      
                                        #find the index of the node to change in the open list
                                        index = openl.index([node_status_array[x][y].fscore,h,node_status_array[x][y]])

                                        #update the node to include this new change
                                        openl[index][2] = node(x,y, n,new_cost, newf)
                                        
                                        #update the node_status_array list and the fscore list in the list
                                        openl[index][0] = newf
                                        openl[index][1] = h
                                        node_status_array[x][y] = openl[index][2]
                                        
                                        #drawing blue nodes
                                        if isSecondLayer != True and grid2[x][y] == True:
                                            pygame.draw.rect(screen,(0,0,255),(x*10,y*10,10,10))
                                            draw_arrow(get_points(node_status_array[x][y]),screen)
                                            pygame.display.update(x*10,y*10,10,10)
                                            
                                        elif isSecondLayer == True and grid1[x][y] == True:
                                            pygame.draw.rect(screen,(0,0,255),(x*10,y*10,10,10))
                                            draw_arrow(get_points(node_status_array[x][y]),screen)
                                            pygame.display.update(x*10,y*10,10,10)

                            #if the node is not a wall and not on the closed list
                            #then simply add it to the open list
                            else:            
                                h = geth((x,y),end)
                                
                                #movement score gets the direction cost added to the parent's directional cost
                                g = getdircost((n.x,n.y),(x,y)) + n.gscore

                                node_status_array[x][y] = node(x, y, n, g, g+h)

                                openl.append([g+h,h,node_status_array[x][y]])

                                #drawing blue nodes
                                if isSecondLayer != True and grid2[x][y] == True:
                                    pygame.draw.rect(screen,(0,0,255),(x*10,y*10,10,10))
                                    draw_arrow(get_points(node_status_array[x][y]),screen)
                                elif isSecondLayer == True and grid1[x][y] == True:
                                    pygame.draw.rect(screen,(0,0,255),(x*10,y*10,10,10))
                                    draw_arrow(get_points(node_status_array[x][y]),screen)
                                pygame.display.update(x*10,y*10,10,10)

        #if the length of the open list is zero(all nodes on closed list)
        #then return an empty path list
        if len(openl) == 0: 
            n = None
            break

        ##############
        # sort the openlist for f and then h, and get the minimum one
        openl = sorted(openl,key = itemgetter(0,1))
        n = openl.pop(0)
        count = count +1
        n = n[2]
        ##############

        # Closed list in red color

        if isSecondLayer != True and grid2[n.x][n.y] == True:
            pygame.time.wait(20)
            #draw some stuff
            pygame.draw.rect(screen, (255,255,255),(s[0]*10,s[1]*10,10,10))
            pygame.display.update(s[0]*10,s[1]*10,10,10)
            #drawing red nodes
            pygame.draw.rect(screen,(255,100,0),(n.x*10,n.y*10,10,10))
            draw_arrow(get_points(n),screen)
            pygame.display.update(n.x*10,n.y*10,10,10)
        elif isSecondLayer == True and grid1[n.x][n.y] == True:
            #draw some stuff
            pygame.draw.rect(screen, (255,255,255),(s[0]*10,s[1]*10,10,10))
            pygame.display.update(s[0]*10,s[1]*10,10,10)
            #drawing red nodes
            pygame.draw.rect(screen,(255,100,0),(n.x*10,n.y*10,10,10))
            draw_arrow(get_points(n),screen)
            pygame.time.wait(20)
            pygame.display.update(n.x*10,n.y*10,10,10)        
        #remove from the 'closed' list
        node_status_array[n.x][n.y].closed = True
        closedList.append(n);
	

    #Now we have our path, we just need to trace it
    #trace the parent of every node until the beginning is reached
    openListCount = len(openl)
    count = count + openListCount
    print "total cells processed : " ,count
    closedListCount = len(closedList)
    moves = []
    isTarget = True   # to blit target once again
    if n!= None:
        while (n.x,n.y) != s:
            moves.insert(0,(n.x,n.y))
	    if(isSecondLayer): # second layer
                if isTarget:
                    screen.blit(targetImage, (n.x*10,n.y*10))
                    isTarget = False
                else:    
                    pygame.draw.rect(screen,(255,255,0),(n.x*10,n.y*10,10,10))
	    elif grid2[n.x][n.y] == True:
                if isTarget:
                    screen.blit(targetImage, (n.x*10,n.y*10))
                    isTarget = False
                else:
                    pygame.draw.rect(screen,(200,200,200),(n.x*10,n.y*10,10,10))
            pygame.display.update(n.x*10-20,n.y*10-20,40,40)
	    closedList.remove(n)
	    closedListCount = len(closedList)
            pygame.time.wait(20)
            n = n.parent        #trace back to the previous node

        end_time = time.time()
        print "total_time taken : ", end_time - start_time

    # Turn back all red and blue squares back to green
    for i in range (0, openListCount):
        n = min(openl)
        openl.remove(n)
        n = n[2]
        if grid2[n.x][n.y] == True and grid1[n.x][n.y] == True:
            pygame.draw.rect(screen,(100,255,100),(n.x*10,n.y*10,10,10))
            pygame.display.update(n.x*10,n.y*10,10,10)	
    
    for i in range (0, closedListCount):
        n = min(closedList)
        closedList.remove(n)
        if grid2[n.x][n.y] == True and grid1[n.x][n.y] == True:
            pygame.draw.rect(screen,(100,255,100),(n.x*10,n.y*10,10,10))
            pygame.display.update(n.x*10,n.y*10,10,10)	

    closedList = None 
    openl = None 
    node_status_array = None 
    
    return moves 
