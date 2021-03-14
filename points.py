from random import randint
from time import time_ns

#=========================================================================
#A point class with x, y coordinate and distance between function
#=========================================================================
class Point():
    def __init__(self, line):
        self.x, self.y = map(float, line.split(","))

    def __str__(self):
        return f"({self.x},{self.y})"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(self.x) + hash(self.y)

    def dist(self, other):
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2

#=========================================================================
#Generate 100 random points
#:return: None (creates "points.csv" file)
#=========================================================================
def generate():
    with open("points.csv", "w") as f:
        for i in range(100):
            x = randint(-200, 200)
            y = randint(-200, 200)
            f.write(f"{x},{y}\n")

#=========================================================================
#Load points from a file
#:return: A list of points
#=========================================================================
def load():
    with open("points.csv") as f:
        return [Point(line) for line in f]

#=========================================================================
#Brute force comparison of points
#:param points: A list of points
#:return: A list of tuples (point, closest)
#=========================================================================
def closest(points):
    pairs = []
    for a in points:
        # Some big number
        closest = 99999
        best = None
        for b in points:
            # A point is 0 from itself, so ignore the point
            if a is b:
                continue
            # Find the distance
            dist = a.dist(b)
            # If it is closest update
            if dist < closest:
                closest = dist
                best = b
        # Store the point and it's closest neighbor
        pairs.append((a, best))
    return pairs

#=========================================================================
#Return all the points around the grid point
#:param point: The point itself
#:param g: The grid
#:param x: The x index
#:param y: The y index
#:return: Yields each point that is close
#=========================================================================
def near(point, g, x, y):
    for other in g[x, y]:
        # Don't return the actual point
        if other is not point:
            yield other
    # Yield all the points in the cells around the point
    yield from g.get((x-1,y-1),[])
    yield from g.get((x,y-1),[])
    yield from g.get((x+1,y-1),[])
    yield from g.get((x-1,y),[])
    yield from g.get((x+1,y),[])
    yield from g.get((x-1,y+1),[])
    yield from g.get((x,y+1),[])
    yield from g.get((x+1,y+1),[])


#=========================================================================
#Find the closest point to each point on the list
#:param points: A list of points
#:return: A list of tuples (point, closest)
#=========================================================================
def grid(points):
    # Find the extents for the grid
    minX, minY, maxX, maxY = 999999, 999999, -999999, -999999
    for point in points:
        minX = min(minX, point.x)
        maxX = max(maxX, point.x)
        minY = min(minY, point.y)
        maxY = max(maxY, point.y)
    divX = (maxX - minX) / 8
    divY = (maxY - minY) / 8

    # Create the grid, and store the points on the grid
    g = {}
    for point in points:
        x = int((point.x - minX) / divX)
        y = int((point.y - minY) / divY)
        key = x, y
        point.key = key
        if key not in g:
            g[key] = []
        g[key].append(point)

    # Find the closest point to each point
    pairs = []
    for point in points:
        x, y = point.key
        closest = 99999
        best = None
        # Check in the surrounding area
        for other in near(point, g, x, y):
            dist = point.dist(other)
            if dist < closest:
                closest = dist
                best = other
        # Store the closest point found
        pairs.append((point, best))
    return pairs

#=========================================================================
#Compare the lists to check if they are equal
#param list1: The reference implementation
#param list2: The optimized implementation
#return: True if they are the same
#=========================================================================
def compare(list1, list2):
    same = True
    for i, (a, b) in enumerate(zip(list1, list2)):
        if a != b:
            # It is possible we have a different combination, but if the distance is the same it is still valid
            if a[0].dist(a[1]) != b[0].dist(b[1]):
                print(f"Different at #{i}, expected {a} distance {a[0].dist(a[1])} got {b} distance {b[0].dist(b[1])}")
                same = False
    return same

#=========================================================================
#Main
#:return: None
#=========================================================================
def main():

    # Load the points from the file
    points = load()

    # Get time in nanoseconds
    start = time_ns()
    raw = closest(points)
    # Get the time taken for the brute force
    raw_time = time_ns() - start
    print("Brute:", raw_time)
    print(raw)
    print("\n")

    # Get time in nanoseconds
    start = time_ns()
    fast = grid(points)
    # Get the time taken for the grid search
    fast_time = time_ns() - start
    print("Fast:", fast_time)
    print(fast)
    print("\n")
    

    # Make sure that the fast version returned the same results as the brute force one
    print("Same result from brute force and fast?")
    print(compare(raw, fast))

if __name__ == "__main__":
    main()
