# Closest Points problem

The problem is find the closest point to each point in a series of 100 points.
I generated a series of points with coordinates between -200 and 200 on the
x, y axis, and saved them to a csv file so that the results can be replicated.

The points are loaded from a csv file, and are kept in the original order and
then the closest point to that point is found (it is not necessarily symmetrical
a may be closest to b, but the closest point to b may be c).

The program uses brute force and compares each the distance (squared) between
each point (there is no need to take the square root to get the actual distance
since we are just interested in the closest and avoiding the square root saves
time). This is an order O(n^2) operation.

I tried a number of divide and conquer versions of the algorithm but the one I
settled with involves dividing the area into a grid of 8 x 8 cells which means
that each point is in a cell with approximately 1 other point. Checking the
cell and the surrounding cells (if you are on the left of cell, you might be
closer to a point in the cell to the left than the points in the same cell).

I wrote a comparison function to check the divide and conquer approach gave
the same results, and they varied slightly from the brute force version, but
that is probably because there was a point that was equidistant from 2 points,
and the brute force picked a different equidistant point. The function returns
in approximately 3 seconds, so about 4 times faster than the brute force. 
With more than 100 points you could extend the grid so that you get approximately 
2 per cell to improve the performance even further.

# Instruction
1. Put this command below onto the terminal to run the program:
    ```python points.py```
    
2. See results on the terminal