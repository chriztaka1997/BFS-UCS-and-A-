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
    item_index = 0
    iteration = 0
    for node in nodes:
        if node.is_equal(target_node):
            found_node = True
            item_index += iteration
        iteration+=1
    return found_node, item_index

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
        node.jaunt = jaunts[check_jaunt[1]].jaunt
        possible_move.append((node.jaunt.year, node.jaunt.x, node.jaunt.y))


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
    total_cost = 0
    cost_list = []
    if method == "BFS":

        temp_node = node
        while not (temp_node.parent is None):
            total_cost += 1
            cost_list.append((temp_node, 1))
            temp_node = temp_node.parent

        cost_list.append((temp_node,0))
        cost_list.reverse()

    else:
        print("This is for ucs and A*")

    return total_cost,cost_list

def check_no_solution(init_node, goal_node, jaunts):
    init_year = init_node.year
    goal_year = goal_node.year
    combine_year = [i.year for i in jaunts ]
    combine_year.append(init_year)

    if goal_year in combine_year:
        return False
    else:
        return True



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

    while (len(frontier_nodes) != 0) and (not found_goal) and (not no_solution):      #while the frontier node is not empty and goal not found, keep searchingr
        print(len(frontier_nodes))
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
        total_cost, cost_list = evaluate_cost(goal_node)
        return_statements.append(total_cost)
        return_statements.append(len(cost_list))
        for cost in cost_list:
            current_node = cost[0]
            return_statements.append(str(current_node.year)+" "+ str(current_node.x)+ " "+ \
                                     str(current_node.y)+" " +str(cost[1]) )

    write_output(return_statements)




def ucs():
    return "UCS"

def a_star():
    return "A*"

# Main Function
method, space_size_x, space_size_y, init_node, goal_node, jaunts = read_input()

if method == "BFS":
    bfs(init_node, goal_node, jaunts)
elif method == "UCS":
    ucs()
else:
    a_star()

# TEST

# method = read_input()
# print (method[1])

# test jaunt list
# for jaunt in jaunts:
#     print(jaunt)

# temp_node = Node(2020, 12, 16)
# print(temp_node in jaunts)              # This will return the wrong answer

#Check the check_node function using temp_node      #This will result in a correct answer
# for jaunt in jaunts:
#     if temp_node.is_equal(jaunt):
#         print(True)

# explored_node = []
# childrens = expand_bfs(temp_node,explored_node)
# print(explored_node[0])

#test if the jaunt is the one in the list
# test_node = Node(2020,12,16, 100)
# j = 0
# for i in jaunts:
#     print("This is j = ",j)
#     print(i.is_equal(test_node))
#     j+=1


#test copy def in node
# method, space_size_x, space_size_y, init_node, goal_node, jaunts = read_input()
# node = init_node.copy()
# node.x += 1
# print(init_node.x)
# print(node.x)

#testing if a tuple could also be reverse
# node1 = Node(1,2,3)
# node2 = Node(2,3,4)
# node3 = Node(3,4,5)
# node4 = Node(4,5,6)
#
# list_nodes = [(node1,1 ), (node2, 2), (node3, 3), (node4, 4)]
# list_nodes.reverse()
# print(list_nodes[0][1])
# print(len(list_nodes))

#Check if a tuple of string can be checked
# tuple1 = [(2020,12,11), (2021, 13, 10)]
# tuple2 = [(2020,12,11), (2021, 13, 10), (2020, 3, 1)]
# print(len(tuple2))
# tuple1.append((2020,12,11))
# print(tuple1)
# print(list(set(tuple1)))
# print(set(tuple2) )

# list1 = [i for i in range (10)]
# list1.append(10)
# print(list1)