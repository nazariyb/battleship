from battleship_main import *


def read_file(filename):
    """
    read file with field and return it as a list
    :return: list
    """
    field = []
    with open(filename, encoding='utf-8') as f:
        f.readline()
        for line in f:
            field.append(line[3:].split())
    return field


# generate empty field
def just_field(): return [['-' for j in range(10)] for i in range(10)]


def point_in_ship(ships, coor):
    """
    check whether current point belong to any ship's space
    :return:
    """
    for ship in ships:
        if coor in ship.coordinates or coor in ship.neighbor:
            return True
    return False


def is_valid(field, ships):
    """
    check whether field is generated correctly
    :return: bool
    """
    requirement = {i: 5 - i for i in range(4, 0, -1)}
    found_ships = {i: 0 for i in range(4, 0, -1)}
    used = set()
    for row in range(len(field)):
        for column in range(len(field[row])):
            if row < 10 and column < 10:
                ship = has_ship(field, (row, column))
                if ship:
                    ship = find_ship(ships, (row, column))
                    if ship.bow not in used:
                        try:
                            found_ships[ship.length] += 1
                            used.add(ship.bow)
                        except KeyError:
                            return False
            else:
                return False
    return requirement == found_ships


def create_ship(length, *args):
    """
    create ship with randomly chosen start point and orientation
    :return: ship as object
    """
    coord = (randint(0, 10 - length), randint(0, 10 - length))
    check = True
    while check:
        check = False
        if args:
            for arg in args:
                check = point_in_ship(arg, coord) if check == False else True
                while point_in_ship(arg, coord):
                    coord = (randint(0, 10 - length), randint(0, 10 - length))
        else:
            break
    return Ship(length=length, horizontal=randint(0, 1), bow=coord)


def set_coordinates(ship, length, *args):
    """
    set coordinates of ships on the field
    """
    check = True
    tries = 0
    while check:
        new_pos = []
        if ship.horizontal:
            for i in range(1, length):
                new_pos.append((ship.bow[0], ship.bow[1] + i))
        else:
            for i in range(1, length):
                new_pos.append((ship.bow[0] + i, ship.bow[1]))
        for pos in new_pos:
            if args:
                for arg in args:
                    check = point_in_ship(arg, pos)
                    if check: break
                else:
                    continue
                break
            else:
                check = False
        if check:
            tries += 1
            if tries == 1 and length != 1:
                if ship.horizontal:
                    ship.horizontal = False
                else:
                    ship.horizontal = True
            if tries >= 2:
                if len(args) == 4:
                    ship = create_ship(length, args[0], args[1],
                                       args[2], args[3])
                elif len(args) == 3:
                    ship = create_ship(length, args[0], args[1], args[2])
                elif len(args) == 2:
                    ship = create_ship(length, args[0], args[1])
                elif len(args) == 1:
                    ship = create_ship(length, args[0])

                tries = 0
    ship.coordinates += new_pos


def generate_field(field):
    """
    create ships and set them on the field
    :param field: list
    :return: both ships as objects and field
    """
    ship4 = [create_ship(4)]
    set_coordinates(ship4[0], 4)
    ship4[0].find_neighbor()
    ship3 = []
    for i in range(2):
        ship3.append(create_ship(3, ship4, ship3))
        set_coordinates(ship3[-1], 3, ship4, ship3[:-1])
        ship3[-1].find_neighbor()
    ship2 = []
    for i in range(3):
        ship2.append(create_ship(2, ship4, ship3, ship2))
        set_coordinates(ship2[-1], 2, ship4, ship3, ship2[:-1])
        ship2[-1].find_neighbor()
    ship1 = []
    for i in range(4):
        ship1.append(create_ship(1, ship4, ship3, ship2, ship1))
        ship1[-1].find_neighbor()

    for i in range(1, 5):
        for ship in eval('ship' + str(i)):
            for coor in ship.coordinates:
                field[coor[0]][coor[1]] = '■'
    ships = []
    for ship in ship4:
        ships.append(ship)
    for ship in ship3:
        ships.append(ship)
    for ship in ship2:
        ships.append(ship)
    for ship in ship1:
        ships.append(ship)
    return field, ships


def write_to_file(field):
    with open('field', 'w') as f:
        f.write(field)
