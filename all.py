import math
# import time

class Node:
    def __init__(self,year,x,y, jaunt = None, parent = None):
        self.year = int(year)
        self.x = int(x)
        self.y = int(y)
        self.jaunt = jaunt          #has to be node
        self.parent = parent        #has to be node

    def __str__(self):                                  #for debugging
        if (self.jaunt is None):
            return "Year: " + str(self.year) + "\n" + \
                   "X: " + str(self.x) + "\n" + \
                   "Y: " + str(self.y) + "\n"

        else:
            return "Year: "+ str(self.year) + "\n"+ \
                "X: " + str(self.x) + "\n" + \
                "Y: " + str(self.y) + "\n" + \
                "Jaunt to: \n" +  str(self.jaunt.year) + "\n"

    def is_equal(self, node):
        test1 = self.year == node.year
        test2 = self.x == node.x
        test3 = self.y == node.y
        return test1 and test2 and test3

    def copy (self):
        temp_node = Node(self.year,self.x,self.y,self.jaunt,self.parent)
        return temp_node


def read_input():
    # read input
    input_file = open("./input.txt", 'r')
    method = input_file.readline().rstrip()                     #Method of search being used

    space_size = input_file.readline().rstrip().split(" ")      #Space size of each year
    space_size_x = int(space_size[0])
    space_size_y = int(space_size[1])

    initial_point = input_file.readline().rstrip().split(" ")   #Initial point of the search
    init_node = Node(initial_point[0], initial_point[1], initial_point[2])

    goal_point = input_file.readline().rstrip().split(" ")      #Goal point of the search
    goal_node = Node(goal_point[0], goal_point[1], goal_point[2])

    numberOfJaunt = int(input_file.readline().rstrip())         #Number of jaunts in the problem

    jaunts = []                                                 #List of all the jaunts in node
    for i in range(numberOfJaunt):
        jaunt = input_file.readline().rstrip().split(" ")
        jaunt_node1 = Node(jaunt[0], jaunt[1], jaunt[2], None)
        jaunt_node2 = Node(jaunt[3], jaunt[1], jaunt[2],jaunt_node1)
        jaunt_node1.jaunt = jaunt_node2
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

def check_node(target_node, nodes):
    '''
    This function will check if the node is in the list of nodes or not
    Using the overwritten is_equal function
    :param node:
    - target_node: is the node that is being searched
    - nodes: is the list of explored nodes
    :return: a boolean of true and false
    '''
    found_node = False
    item_index = []
    iteration = 0
    for node in nodes:
        if node.is_equal(target_node):
            found_node = True
            item_index.append(iteration)
        iteration+=1
    return found_node, item_index

def check_no_solution(init_node, goal_node, jaunts):
    init_year = init_node.year
    goal_year = goal_node.year
    combine_year = [i.year for i in jaunts ]
    combine_year.append(init_year)

    if goal_year in combine_year:
        if (0 <= goal_node.x < space_size_x) and (0<=goal_node.y< space_size_y)\
                and (0 <= init_node.x < space_size_x) and (0 <= init_node.y < space_size_y):
            return True
        else:
            return False
    else:
        return False


def evaluate_cost(node):
    '''
    This function is to evaluate cost by subtracting the distance between the current node and its parent (year,x,y)
    depending on the method of search.
    The adding their absolute value, it will differentiate the actions were taken
    :param node: the goal node
    :return:
    - total_cost: the total cost of the moves taken to reach the goal
    - cost_list: The list of tuple of the move taken from start to goal with the cost
    '''
    cost_list = []

    temp_node = node
    if method == "BFS":

        while not (temp_node.parent is None):
            cost_list.append((temp_node, 1))
            temp_node = temp_node.parent

    else:
        while not (temp_node.parent is None):
            if temp_node.x != temp_node.parent.x or temp_node.y != temp_node.parent.y:
                x_diff = abs(temp_node.x - temp_node.parent.x)
                y_diff = abs(temp_node.y - temp_node.parent.y)

                if x_diff+y_diff == 2:
                    cost_list.append((temp_node, 14))
                else:
                    cost_list.append((temp_node, 10))
            else:
                cost_list.append((temp_node, abs(temp_node.parent.year - temp_node.year)))
            temp_node = temp_node.parent

    cost_list.append((temp_node, 0))
    cost_list.reverse()

    return cost_list

'''
This part is specific to BFS 
'''

def expand_bfs(node):
    '''
    expand all the possible move of the node
    This is where all the move constraint should be handled
    where jaunts, space size x and space size y are global variable
    Return a list of nodes that could be the possible next move and the cost
    '''
    move_cost = 1
    #moves starts from jaunt, N, NE, E, SE, S, SW, W, NW
    possible_move = []
    #check jaunt
    check_jaunt = check_node(node, jaunts)
    if check_jaunt[0] :
        list_of_jaunt = check_jaunt[1]
        for i in list_of_jaunt:
            possible_move.append((jaunts[i].jaunt.year, node.x, node.y))


    #Check other possible move
    #North
    if node.y +1 < space_size_y:
        temp_node = node.copy()
        temp_node.y += 1
        possible_move.append((temp_node.year,temp_node.x, temp_node.y))


    #North East
    if node.x + 1 < space_size_x and node.y + 1 < space_size_y:
        temp_node = node.copy()
        temp_node.y += 1
        temp_node.x += 1
        possible_move.append((temp_node.year, temp_node.x, temp_node.y))

    #East
    if node.x + 1 < space_size_x :
        temp_node = node.copy()
        temp_node.x += 1
        possible_move.append((temp_node.year, temp_node.x, temp_node.y))

    #South East
    if node.x + 1 < space_size_x and node.y - 1 >= 0:
        temp_node = node.copy()
        temp_node.y -= 1
        temp_node.x += 1
        possible_move.append((temp_node.year, temp_node.x, temp_node.y))

    #South
    if node.y - 1 >= 0:
        temp_node = node.copy()
        temp_node.y -= 1
        possible_move.append((temp_node.year, temp_node.x, temp_node.y))

    #South West
    if node.x - 1 >= 0 and node.y - 1 >= 0:
        temp_node = node.copy()
        temp_node.y -= 1
        temp_node.x -= 1
        possible_move.append((temp_node.year, temp_node.x, temp_node.y))

    #West
    if node.x - 1 >= 0  :
        temp_node = node.copy()
        temp_node.x -= 1
        possible_move.append((temp_node.year, temp_node.x, temp_node.y))

    #North West
    if node.x - 1 >= 0and node.y + 1 < space_size_y:
        temp_node = node.copy()
        temp_node.y += 1
        temp_node.x -= 1
        possible_move.append((temp_node.year, temp_node.x, temp_node.y))

    return list(dict.fromkeys(possible_move))





def bfs(init_node, goal_node, jaunts):
    #space size x and space size y are the bound of the space
    #THey are both global variable

    frontier_nodes = []
    explored_nodes = []

    #initial
    frontier_nodes.append(init_node)
    explored_nodes.append((init_node.year, init_node.x, init_node.y))

    found_goal = False

    no_solution = check_no_solution(init_node, goal_node, jaunts)

    while (len(frontier_nodes) != 0) and (not found_goal) and (no_solution):      #while the frontier node is not empty and goal not found, keep searchingr
        temp_node= frontier_nodes.pop(0)

        if temp_node.is_equal(goal_node):
            found_goal = True
            goal_node.parent = temp_node.parent
        else:
            childrens = expand_bfs(temp_node)
            for child in childrens:
                #Check if the node is in the explored list
                if not (child in explored_nodes):
                    child_node = Node(child[0], child[1], child[2])
                    if not(check_node(child_node, frontier_nodes)[0]):
                        if temp_node.year != child[0]:
                            child_node.jaunt = temp_node
                        child_node.parent = temp_node
                        explored_nodes.append((child_node.year, child_node.x, child_node.y))
                        frontier_nodes.append(child_node)

    return_statements = []

    if not found_goal:
        return_statements.append("FAIL")
    else:
        cost_list = evaluate_cost(goal_node)
        total_cost = len(cost_list)-1
        return_statements.append(total_cost)
        return_statements.append(len(cost_list))
        for cost in cost_list:
            current_node = cost[0]
            return_statements.append(str(current_node.year)+" "+ str(current_node.x)+ " "+ \
                                     str(current_node.y)+" " +str(cost[1]) )

    write_output(return_statements)


'''
This part is function that is specific for Uniform Cost Seacrch
'''

def expand_else(target_node):
    '''
    expand all the possible move of the node
    This is where all the move constraint should be handled
    where jaunts, space size x and space size y are global variable

    :param node: is a tuple consist of the total cost to that point and Node class
    :return: a list of possible moves, each with the total cost until that node
    '''

    move_cost_cheap = 10
    move_cost_expen = 14
    node = target_node[1]
    # moves starts from jaunt, N,E,S,W, NE, SE, SW, NW
    possible_move = []
    # check jaunt
    check_jaunt = check_node(node, jaunts)
    if check_jaunt[0]:
        list_of_jaunt = check_jaunt[1]
        for i in list_of_jaunt:
            possible_move.append((abs(jaunts[i].jaunt.year - node.year)+target_node[0],
                                  (jaunts[i].jaunt.year, node.x, node.y)))

    # Check other possible move
    # North
    if node.y + 1 < space_size_y:
        temp_node = node.copy()
        temp_node.y += 1
        possible_move.append((move_cost_cheap + target_node[0],
                              (temp_node.year, temp_node.x, temp_node.y)))
    # East
    if node.x + 1 < space_size_x:
        temp_node = node.copy()
        temp_node.x += 1
        possible_move.append((move_cost_cheap + target_node[0],
                              (temp_node.year, temp_node.x, temp_node.y)))

    # South
    if node.y - 1 >= 0:
        temp_node = node.copy()
        temp_node.y -= 1
        possible_move.append((move_cost_cheap + target_node[0],
                              (temp_node.year, temp_node.x, temp_node.y)))

    # West
    if node.x - 1 >= 0:
        temp_node = node.copy()
        temp_node.x -= 1
        possible_move.append((move_cost_cheap + target_node[0],
                              (temp_node.year, temp_node.x, temp_node.y)))

    # North East
    if node.x + 1 < space_size_x and node.y + 1 < space_size_y:
        temp_node = node.copy()
        temp_node.y += 1
        temp_node.x += 1
        possible_move.append((move_cost_expen + target_node[0],
                              (temp_node.year, temp_node.x, temp_node.y)))



    # South East
    if node.x + 1 < space_size_x and node.y - 1 >= 0:
        temp_node = node.copy()
        temp_node.y -= 1
        temp_node.x += 1
        possible_move.append((move_cost_expen + target_node[0],
                              (temp_node.year, temp_node.x, temp_node.y)))



    # South West
    if node.x - 1 >= 0 and node.y - 1 >= 0:
        temp_node = node.copy()
        temp_node.y -= 1
        temp_node.x -= 1
        possible_move.append((move_cost_expen + target_node[0],
                              (temp_node.year, temp_node.x, temp_node.y)))



    # North West
    if node.x - 1 >= 0 and node.y + 1 < space_size_y:
        temp_node = node.copy()
        temp_node.y += 1
        temp_node.x -= 1
        possible_move.append((move_cost_expen + target_node[0],
                              (temp_node.year, temp_node.x, temp_node.y)))

    return list(dict.fromkeys(possible_move))

def check_node_ucs(cost,target_node, nodes):
    """
    check the node only if it is in the frontier node

    :param target_node: the node that is being look for
    :param nodes: a list of tuple that consist total cost and the node
    :return: a true or false if the node is in the list
    """
    found_node = False
    for i in range(len(nodes)):
        node = nodes[i]
        if node[1].is_equal(target_node):
            found_node = True
            if node[0]> cost:
                nodes[i] = (cost, node[1])
    return found_node


def ucs(init_node, goal_node, jaunts):
    # space size x and space size y are the bound of the space
    # THey are both global variable

    frontier_nodes = []
    explored_nodes = []

    # initial
    frontier_nodes.append((0, init_node))
    explored_nodes.append((init_node.year, init_node.x, init_node.y))

    found_goal = False

    no_solution = check_no_solution(init_node, goal_node, jaunts)
    total_cost = 0

    while (len(frontier_nodes) != 0) and (not found_goal) and (no_solution):      #while the frontier node is not empty and goal not found, keep searchingr
        temp_node= frontier_nodes.pop(0)

        if temp_node[1].is_equal(goal_node):
            found_goal = True
            goal_node.parent = temp_node[1].parent
            total_cost += temp_node[0]

        else:
            childrens = expand_else(temp_node)
            for child in childrens:
                #Check if the node is in the explored list
                child_pos = child[1]
                if not (child_pos in explored_nodes):
                    child_node = Node(child_pos[0], child_pos[1], child_pos[2])
                    if not(check_node_ucs(child[0],child_node, frontier_nodes)):
                        if temp_node[1].year != child[0]:
                            child_node.jaunt = temp_node[1]
                        child_node.parent = temp_node[1]
                        explored_nodes.append((child_node.year, child_node.x, child_node.y))
                        frontier_nodes.append((child[0],child_node))
            frontier_nodes = sorted(frontier_nodes, key=lambda x: x[0])


    return_statements = []

    if not found_goal:
        return_statements.append("FAIL")
    else:
        cost_list = evaluate_cost(goal_node)
        return_statements.append(total_cost)
        return_statements.append(len(cost_list))
        for cost in cost_list:
            current_node = cost[0]
            return_statements.append(str(current_node.year) + " " + str(current_node.x) + " " + \
                                     str(current_node.y) + " " + str(cost[1]))

    write_output(return_statements)

'''
This is function necessary for a star algorithm
'''



def heuristic(current_node):
    '''
    This function will calculate the heuristic of the node

    :param current_node: a tuple that consist of (cost, node)
    :return: the heuristic of the node
    '''
    # print("Current node: ", current_node[1])

    g = current_node[0]
    h = math.sqrt((current_node[1].year - goal_node.year)**2+\
        (current_node[1].x - goal_node.x)**2 + abs(current_node[1].y - goal_node.y)**2)
    f = g + h
    # print("The hueristic: ",f)
    # print()
    return f

def check_node_a(cost,target_node, nodes):
    """
    check the node only if it is in the frontier node

    :param target_node: the node that is being look for
    :param nodes: a list of tuple that consist total cost and the node
    :return: a true or false if the node is in the list
    """
    found_node = False
    for i in range(len(nodes)):
        node = nodes[i]
        if node[2].is_equal(target_node):
            found_node = True
            if node[1]> cost:
                temp_node = (cost, node[2])
                heu = heuristic(temp_node)
                nodes[i] = (heu, cost, node[1])


    return found_node

def a_star(init_node, goal_node, jaunts):
    # space size x and space size y are the bound of the space
    # THey are both global variable

    frontier_nodes = []
    explored_nodes = []

    # initial
    frontier_nodes.append((0, 0, init_node))                                      #the tuple consist of (f, total cost to this node, current node)
    explored_nodes.append((init_node.year, init_node.x, init_node.y))

    found_goal = False

    no_solution = check_no_solution(init_node, goal_node, jaunts)
    total_cost = 0

    while (len(frontier_nodes) != 0) and (not found_goal) and (no_solution):      #while the frontier node is not empty and goal not found, keep searchingr
        print("Number of nodes in frontier node: ",len(frontier_nodes))
        temp_node= frontier_nodes.pop(0)

        if temp_node[2].is_equal(goal_node):
            found_goal = True
            goal_node.parent = temp_node[2].parent
            total_cost += temp_node[1]

        else:
            childrens = expand_else((temp_node[1],temp_node[2]))
            # print("Size of the children: ", len(childrens))
            for child in childrens:
                child_pos = child[1]
                if not (child_pos in explored_nodes):
                    child_node = Node(child_pos[0], child_pos[1], child_pos[2])
                    if not(check_node_a(child[0],child_node, frontier_nodes)):
                        if temp_node[2].year != child[0]:
                            child_node.jaunt = temp_node[2]
                        child_node.parent = temp_node[2]
                        explored_nodes.append((child_node.year, child_node.x, child_node.y))
                        frontier_nodes.append((heuristic((child[0], child_node)),child[0],child_node))
            frontier_nodes = sorted(frontier_nodes, key= lambda x : x[0] )

    return_statements = []

    if not found_goal:
        return_statements.append("FAIL")
    else:
        cost_list = evaluate_cost(goal_node)
        return_statements.append(total_cost)
        return_statements.append(len(cost_list))
        for cost in cost_list:
            current_node = cost[0]
            return_statements.append(str(current_node.year) + " " + str(current_node.x) + " " + \
                                     str(current_node.y) + " " + str(cost[1]))

    write_output(return_statements)

# Main Function
method, space_size_x, space_size_y, init_node, goal_node, jaunts = read_input()


# start_time = time.time()
if method == "BFS":
    bfs(init_node, goal_node, jaunts)
elif method == "UCS":
    ucs(init_node,goal_node,jaunts)
else:
    a_star(init_node,goal_node,jaunts)


# print("--- %s seconds ---" % (time.time() - start_time))
