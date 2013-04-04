import astar as st

start = st.Cell(0,0,True)
test = st.Cell(5,5,True)
target = st.Cell(6,6,True)
walls = ((0, 5), (1, 0), (1, 1), (1, 5), (2, 3),(3, 1), (3, 2), (3, 5), (4, 1), (4, 4), (5, 1))

grid = st.Grid(6)

grid.init_grid(start,target,walls)

st.process(start,target,grid)

