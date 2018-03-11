from random import randint


def letter_to_index(coord):
    """
    convert coordinates from format ('A', 1) to (0, 0)
    :param coord: tuple
    :return: tuple
    """
    return coord[1] - 1, ord(coord[0].lower()) - 97


def index_to_letter(coord):
    """
    convert coordinates from format (0, 0) to ('A', 1)
    :param coord: tuple
    :return: tuple
    """
    return (chr(coord[0] + 65), coord[1] + 1)


def has_ship(field, coord):
    """
    :return: bool whether a square has a ship
    """
    coord = letter_to_index(coord) if type(coord[0]) == str else coord
    return field[coord[0]][coord[1]] == '■'


def find_ship(ships, coord, delete=False):
    """
    return ship which is in current square
    or delete coord from ship's coordinates and return tuple of bool whether

    """
    coord = letter_to_index(coord) if type(coord[0]) == str else coord
    for ship in ships:
        for coor in ship.coordinates:
            if coor == coord:
                if delete:
                    ship.coordinates.remove(coord)
                return (bool(ship.coordinates), ship) if delete else ship
    # actually it is checked whether these coordinates belong to ship before
    # call this function(find_ship) so if there were no errors earlier this
    # func will never return False
    return False


class Ship:
    """
    represent ship with its coordinates, orientation and length
    """

    def __init__(self, bow=(), horizontal=True, length=0, neighbor=set()):
        self.bow = bow
        self.horizontal = horizontal
        self.length = length
        self.neighbor = neighbor
        self.coordinates = [bow]

    def find_neighbor(self):
        """
        find neighbor coordinates to ship's ones and return them in case it
        will be necessary
        :return: 
        """
        self.neighbor = set()
        for coord in self.coordinates:
            a1 = (coord[0] - 1, coord[1] - 1)
            a2 = (coord[0] - 1, coord[1])
            a3 = (coord[0] - 1, coord[1] + 1)
            a4 = (coord[0], coord[1] + 1)
            a5 = (coord[0] + 1, coord[1] + 1)
            a6 = (coord[0] + 1, coord[1])
            a7 = (coord[0] + 1, coord[1] - 1)
            a8 = (coord[0], coord[1] - 1)
            for i in range(1, 9):
                if eval('a' + str(i)) not in self.coordinates:
                    if eval('a' + str(i))[0] >= 0 and eval('a' + str(i))[1] \
                            >= 0:
                        self.neighbor.add(eval('a' + str(i)))
        return self.neighbor


class Field:
    """
    represent field with its coordinates and ships
    """

    def __init__(self, field, ships):
        self.field = field
        self.ships = ships[:]

    def field_to_str(self):
        """

        :return: str which can be printed
        """
        return '\n'.join([(str(number + 1) + '  ' + '  '.join(row)) for number, \
                                                                        row in
                          enumerate(self.field)])

    def display(self):
        """
        prints field with numeration
        """
        field = self.field_to_str()
        lett = [chr(i) for i in range(65, 75)]
        print('   ' + '  '.join(lett))
        print(field)


class Game:
    """
    combine all other game's objects
    """

    def __init__(self, fields, players):
        self.fields = fields
        self.__players = players[:]
        self.current_player = players[randint(0, 1)]
        self.opposite_player = players[0] if self.current_player == players[
            1] else players[1]
        self.shoots = set()

    def rewrite_coord(self, index, name, symbol, hidden=''):
        """
        helpful function for setting sings in coordinates where was shot in
        """
        self.fields['field' + name + hidden].field[
            index[0]][index[1]] = symbol

    def shoot_at(self, field, index):
        """
        organize thing which have to be done when player shoots
        :return: True or False whether shot was successful
        """
        index = letter_to_index(index) if type(index[0]) == str else index
        if has_ship(field.field, index):
            res = find_ship(field.ships, index, True)
            self.rewrite_coord(index, self.opposite_player, '√',
                               hidden='_hidden')
            self.rewrite_coord(index, self.opposite_player, '√')
            if not res[0]:
                for coord in res[1].neighbor:
                    try:
                        self.fields['field' + self.opposite_player +
                                    '_hidden'].field[coord[0]][coord[1]] = '░'
                        self.fields['field' + self.opposite_player
                                    ].field[coord[0]][coord[1]] = '░'
                    except IndexError:
                        pass
                for ship in field.ships:
                    if ship == res[1]:
                        field.ships.remove(ship)
                        return True
        else:
            self.rewrite_coord(index, self.opposite_player, '░',
                               hidden='_hidden')
            self.rewrite_coord(index, self.opposite_player, '░')
            self.current_player, self.opposite_player = \
                self.opposite_player, self.current_player
            return False
