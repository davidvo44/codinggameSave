import sys
import math
# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
map = []
troll_dict = dict()
treeList = []
shack0 = [0,0]
shack1 = [0,0]
width, height = [int(i) for i in input().split()]
for i in range(height):
    strs = input()
    map.append(strs)
    pos0 = strs.find('0')
    if pos0 != -1:
        shack0 = [pos0, i]
    pos1 = strs.find('1')
    if pos1 != -1:
        shack1 = [pos1, i]

class Troll (object):
    def __init__(self, _id, player, x, y, movement_speed, carry_capacity, harvest_power, chop_power, carry_plum, carry_lemon, carry_apple, carry_banana, carry_iron, carry_wood):
        self.speed = movement_speed
        self.bagCap = carry_capacity
        self.harvestPwr = harvest_power
        self.chopPwr = chop_power
        self.player = player
        self.position = [int(x),int(y)]
        self.id = _id
        self.lemon = carry_lemon
        self.plum = carry_plum
        self.apple = carry_apple
        self.banana = carry_banana
        self.iron = carry_iron
        self.wood = carry_wood
        self.invent = self.lemon + self.plum + self.apple + self.banana + self.iron + self.wood
        self.action = 'NONE' #action list NONE, goTree, goBase, chopTree, goPlant, plant, pick
        self.objectif = [0,0]
        self.stuck = False
        harvest = 0
        plant = 0
        for i in troll_dict:
            if troll_dict[i].player == 0:
                if troll_dict[i].job == 'HARVEST':
                    harvest += 1
                if troll_dict[i].job == 'PLANT':
                    plant += 1
        if harvest > 0 and plant == 0:
            self.job = 'PLANT' #list: 'HARVEST' 'PLANT'
            print(f"{self.job}", file=sys.stderr, flush=True)
        else:
            self.job = 'HARVEST'

    def updateInfo(self, _id, player, x, y, movement_speed, carry_capacity, harvest_power, chop_power, carry_plum, carry_lemon, carry_apple, carry_banana, carry_iron, carry_wood):
        self.speed = movement_speed
        self.bagCap = carry_capacity
        self.harvestPwr = harvest_power
        self.chopPwr = chop_power
        self.player = player
        self.position = [int(x),int(y)]
        self.id = _id
        self.lemon = carry_lemon
        self.plum = carry_plum
        self.apple = carry_apple
        self.banana = carry_banana
        self.iron = carry_iron
        self.wood = carry_wood
        self.invent = self.lemon + self.plum + self.apple + self.banana + self.iron + self.wood



class Tree (object):
    def __init__(self, type, x, y, size, health, fruit, cd):
        self.type = type
        self.position = [int(x), int(y)]
        text = map[self.position[1]]
        if type == 'PLUM':
            text = text[:self.position[0]] + 'p' + text[self.position[0] + 1:]
        if type == 'LEMON':
            text = text[:self.position[0]] + 'l' + text[self.position[0] + 1:]
        if type == 'APPLE':
            text = text[:self.position[0]] + 'a' + text[self.position[0] + 1:]
        if type == 'BANANA':
            text = text[:self.position[0]] + 'b' + text[self.position[0] + 1:]
        map[self.position[1]] = text
        self.size = int(size)
        self.health = int(health)
        self.fruits = int(fruit)
        self.cd = cd

class Score (object):
    def __init__(self, plum, lemon, apple, banana, iron, wood):
        self.plum = int(plum)
        self.lemon = int(lemon)
        self.apple = int(apple)
        self.banana = int(banana)
        self.iron = int(iron)
        self.wood = int(wood)

    def get(self, string):
        if string == 'plum':
            return self.plum
        if string == 'lemon':
            return self.lemon
        if string == 'apple':
            return self.apple
        if string == 'banana':
            return self.banana
        if string == 'iron':
            return self.iron
        if string == 'wood':
            return self.wood

score = [Score(0, 0, 0, 0, 0, 0),Score(0, 0, 0, 0, 0, 0)]


def plantNextTree():
    newPos = shack0.copy()
    coordList = [
        [newPos[0] + 1, newPos[1]],
        [newPos[0] - 1, newPos[1]],
        [newPos[0], newPos[1] + 1],
        [newPos[0], newPos[1] - 1],
        [newPos[0] + 1, newPos[1] + 1],
        [newPos[0] + 1, newPos[1] - 1],
        [newPos[0] -1, newPos[1] + 1],
        [newPos[0] -1, newPos[1] - 1],
        ]
    for pos in coordList:

        x = pos[0]
        y = pos[1]
        if x < width and x >= 0 and y < height and y >= 0 and map[y][x] == '.':
            return pos
    return [-1,-1]

def selectTypePlant():
    plum = 0
    lemon = 0
    apple = 0
    banana = 0
    newPos = shack0.copy()
    coordList = [
        [newPos[0] + 1, newPos[1]],
        [newPos[0] - 1, newPos[1]],
        [newPos[0], newPos[1] + 1],
        [newPos[0], newPos[1] - 1],
        [newPos[0] + 1, newPos[1] + 1],
        [newPos[0] + 1, newPos[1] - 1],
        [newPos[0] + 0, newPos[1] + 1],
        [newPos[0] + 0, newPos[1] - 1],
        ]

    for pos in coordList:
        x = pos[0]
        y = pos[1]
        if x < width or x >= 0 or y < height or y >= 0:
            continue
        if map[y][x] == 'p':
            plum += 1
        elif map[y][x] == 'l':
            lemon += 1
        elif map[y][x] == 'a':
            apple += 1
        elif map[y][x] == 'b':
            banana += 1

    fruits = {
        'plum': plum,
        'lemon': lemon,
        'apple': apple,
        'banana': banana
    }

    minimum = min(fruits.values())
    lowest_fruits = []
    for fruit, value in fruits.items():
        if value == minimum:
            lowest_fruits.append(fruit)
    fruits = {}
    for i in lowest_fruits:
        fruits[i] = score[0].get(i)
    lowest = min(fruits, key=fruits.get)
    print(f"{lowest}", file=sys.stderr, flush=True)
    return lowest
    

def plant(troll):
    objectif = plantNextTree()
    if objectif[0] == -1:
        troll.job = 'HARVEST'
        return
    troll.objectif = objectif
    type = selectTypePlant()
    if type == 'plum':
        troll.plum += 1
        if score[0].get(type) == 0:
            troll.action = 'search'
    if type == 'lemon':
        troll.lemon += 1
    if type == 'apple':
        troll.apple += 1
    if type == 'banana':
        troll.banana += 1
    troll.action = 'pick'



def treeAvailable(tree):
    for i in troll_dict:
        if troll_dict[i].player == 0:
            if troll_dict[i].objectif == tree.position:
                return False
    return True


def goBase(troll : Troll):
    troll.action = 'goBase'
    troll.objectif[0] = shack0[0]
    troll.objectif[1] = shack0[1]
    if abs(troll.objectif[0] - troll.position[0]) > abs(troll.position[1] - troll.objectif[1]):

        if troll.objectif[0] - troll.position[0] > 0:
            troll.objectif[0] = troll.objectif[0] - 1
        else :
            troll.objectif[0] = troll.objectif[0] + 1
    else:
        if troll.objectif[1] - troll.position[1] > 0:
            troll.objectif[1] = troll.objectif[1] - 1
        else :
            troll.objectif[1] = troll.objectif[1] + 1

def setNewobj(troll : Troll):
    if troll.job == 'PLANT':
        plant(troll)
    if troll.job == 'PLANT':
        return
    if troll.invent != 0:
       goBase(troll)
    else:
        dist = sys.maxsize
        newPos = [0,0]
        troll.action = 'goTree'
        for i in treeList:
            newDist = math.dist(troll.position, i.position)
            if i.fruits != 0 and dist > newDist and treeAvailable(i):
                dist = newDist
                newPos = i.position
        troll.objectif = newPos


def chopTreeft(troll : Troll):
    tree = 0
    for i in treeList:
        if troll.position == i.position:
            tree = i
            if troll.bagCap == troll.invent or i.fruits == 0:
                goBase(troll)
            break

def selectType(troll: Troll):
    if troll.plum != 0:
        return ' PLUM;'
    elif troll.lemon != 0:
        return ' LEMON;'
    elif troll.apple != 0:
        return ' APPLE;'
    elif troll.banana != 0:
        return ' BANANA;'
    return ''


def printMove(troll: Troll):
    action = 'None'
    printmsg = ''
    id = str(troll.id)
    if troll.action == 'goTree' or troll.action == 'goBase' or troll.action == 'goPlant':
        printmsg = ' MOVE' + ' ' + id + ' ' + str(troll.objectif[0]) + ' ' + str(troll.objectif[1]) + ';'
    if troll.action == 'chopTree':
        printmsg = ' HARVEST' + ' ' + id + ';'
    if troll.action == 'dropBase':
        printmsg = ' DROP' + ' ' + id + ';'
    if troll.action == 'dropBase':
        printmsg = ' DROP' + ' ' + id + ';'
    if troll.action == 'plant':
        printmsg = ' PLANT' + ' ' + id
        printmsg += selectType(troll)
    if troll.action == 'pick':
        printmsg = ' PICK ' + id
        printmsg += selectType(troll)

    return(printmsg)

def trainCondition(turn,score):
    trollNumber = 0 
    printmsg = ''
    for i in troll_dict:
        if troll_dict[i].player == 0:
            trollNumber += 1
    if turn < 50 and score.plum - trollNumber - trollNumber ** trollNumber >= 0 and score.lemon - trollNumber - trollNumber ** trollNumber >= 0 and score.apple - trollNumber - trollNumber ** trollNumber >= 0:
    
        print(f'troll after {turn} {score.plum} {score.lemon} {score.apple} {trollNumber}', file=sys.stderr, flush=True)
       
        # if turn < 10:
            # for i int 
            # mvt = (score.plum - trollNumber) // 2
            # carry = (score.lemon - trollNumber) // 3
            # pwr = score.apple - trollNumber
            # if pwr > carry:
                # pwr = carry
        # else:
        mvt = 1
        carry = 1
        pwr = 1
        print(f"{mvt}  {carry} {pwr}", file=sys.stderr, flush=True)
        printmsg = ' TRAIN ' + str(mvt) + ' ' + str(carry) + ' ' + str(pwr) + ' ' + '0'
    return printmsg




# game loop
turn = 0
while True:
    printmsg = ''
    treeList.clear()
    for i in range(2):
        plum, lemon, apple, banana, iron, wood = [int(j) for j in input().split()]
        score[i] = Score(plum, lemon, apple, banana, iron, wood)
    trees_count = int(input())
    print(f"{trees_count}", file=sys.stderr, flush=True)
    for i in range(trees_count):
        inputs = input().split()
        newTree = Tree(inputs[0], inputs[1], inputs[2], inputs[3], inputs[4], inputs[5], inputs[6])
        treeList.append(newTree)
    trolls_count = int(input())
    for i in range(trolls_count):
        _id, player, x, y, movement_speed, carry_capacity, harvest_power, chop_power, carry_plum, carry_lemon, carry_apple, carry_banana, carry_iron, carry_wood = [int(j) for j in input().split()]
        if _id in troll_dict:
            troll_dict[_id].updateInfo(_id, player, x, y, movement_speed, carry_capacity, harvest_power, chop_power, carry_plum, carry_lemon, carry_apple, carry_banana, carry_iron, carry_wood)
        else:
            troll_dict[_id] = Troll(_id, player, x, y, movement_speed, carry_capacity, harvest_power, chop_power, carry_plum, carry_lemon, carry_apple, carry_banana, carry_iron, carry_wood)

    for i in troll_dict:
        if troll_dict[i].player == 0:
            if troll_dict[i].action == 'pick':
                troll_dict[i].action = 'goPlant'
            if troll_dict[i].action == 'plant':
                goBase(troll_dict[i])
            if troll_dict[i].action == 'NONE' or troll_dict[i].action == 'dropBase':
                setNewobj(troll_dict[i])
            elif troll_dict[i].action == 'goTree':
                if troll_dict[i].position[0] == troll_dict[i].objectif[0] and troll_dict[i].position[1] == troll_dict[i].objectif[1]:
                    troll_dict[i].action = 'chopTree'
            elif troll_dict[i].action == 'goPlant':
                if troll_dict[i].position[0] == troll_dict[i].objectif[0] and troll_dict[i].position[1] == troll_dict[i].objectif[1]:
                    troll_dict[i].action = 'plant'
            elif troll_dict[i].action == 'chopTree':
                chopTreeft(troll_dict[i])
            elif troll_dict[i].action == 'goBase':
                if troll_dict[i].position[0] == troll_dict[i].objectif[0] and troll_dict[i].position[1] == troll_dict[i].objectif[1]:
                    troll_dict[i].action = 'dropBase'
            printmsg = printmsg + printMove(troll_dict[i])
    printmsg = printmsg + trainCondition(turn, score[0])
    print (printmsg)
    turn = turn + 1




    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)


    # valid actions:
    # MOVE <id> <x> <y>
    # HARVEST <id> - when you are on the same cell as a tree
    # DROP <id> - when you are next to your shack and carry items
