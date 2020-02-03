
class Node:
    def __init__(self,year,x,y, jaunt = None, parent = None):
        self.year = year
        self.x = x
        self.y = y
        self.jaunt = jaunt
        self.parent = None

    def __str__(self):                                  #for debugging
        return "Year: "+ str(self.year) + "\n"+ \
                "X: " + str(self.x) + "\n" + \
                "Y: " + str(self.y) + "\n" + \
                "Jaunt Year: " + str(self.jaunt) + "\n"

    def is_equal(self, node):
        test1 = self.year is node.year
        test2 = self.x is node.x
        test3 = self.y is node.y
        return test1 and test2 and test3


def read_input():
    # read input
    input_file = open("./input.txt", 'r')
    method = input_file.readline().rstrip()                     #Method of search being used

    space_size = input_file.readline().rstrip().split(" ")      #Space size of each year
    space_size_x = int(space_size[0])
    space_size_y = int(space_size[1])

    initial_point = input_file.readline().rstrip().split(" ")   #Initial point of the search
    init_node = Node(int(initial_point[0]), int(initial_point[1]), int(initial_point[2]))

    goal_point = input_file.readline().rstrip().split(" ")      #Goal point of the search
    goal_node = Node(int(goal_point[0]), int(goal_point[1]), int(goal_point[2]))

    numberOfJaunt = int(input_file.readline().rstrip())         #Number of jaunts in the problem

    jaunts = []                                                 #List of all the jaunts in node
    for i in range(numberOfJaunt):
        jaunt = input_file.readline().rstrip().split(" ")
        jaunt_node1 = Node(int(jaunt[0]), int(jaunt[1]), int(jaunt[2]),int(jaunt[3]), None )
        jaunt_node2 = Node(int(jaunt[3]), int(jaunt[1]), int(jaunt[2]),int(jaunt[0]), None )
        jaunts.append(jaunt_node1)
        jaunts.append(jaunt_node2)

    input_file.close()

    return method, space_size_x, space_size_y, init_node, goal_node, jaunts

def write_output(output_message):
    # outputting solution
    outputFile = open("./output.txt", "w+")
    for message in output_message:
        if(message == "FAIL"):
            outputFile.write(str(message))
        else:
            outputFile.write(str(message) + "\n")
    outputFile.close()

def expand(node):
    #expand all the possible move of the node
    #This is where all the move constraint should be handled
    #where jaunts, space size x and space size y are global variable



def bfs(initPoint, goalPoint, jaunts):
    #space size x and space size y are the bound of the space
    #THey are both global variable

    cost_of_move = 1
    frontier_nodes = []
    explored_nodes = []

    #initial
    frontier_nodes.append(init_node)
    found_goal = False
    cost = 0

    while (len(frontier_nodes) != 0) and (not found_goal):      #while the frontier node is not empty and goal not found, keep searching
        temp_node = frontier_nodes.pop(0)

        if temp_node.is_equal(goal_node):
            found_goal = True
        else:
            childrens = expand(temp_node)
            for child in childrens:
                frontier_nodes.append(child)
        explored_nodes.append(temp_node)

    moves_and_cost = []

    return_statements = []

    if not found_goal:
        return_statements.append("FAIL")
    else:
        return_statements.append(cost)
        return_statements.append(len(moves_and_cost))
        for i in range(moves_and_cost)
            return_statements.append()
    return "BFS"

def ucs():
    return "UCS"

def a_star():
    return "A*"


method, space_size_x, space_size_y, init_node, goal_node, jaunts = read_input()


if method == "BFS":
    bfs(init_node, goal_node, jaunts)
elif method == "UCS":
    ucs()
else:
    a_star()
