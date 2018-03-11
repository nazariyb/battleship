from os import system

from battleship_auxiliary_functions import *


def read_coord(game):
    """
    ask players to input coordinates and check whether they are in
    correct format and return them if yes
    :return:
    """
    while True:
        shot = input(
            'player ' + game.current_player + ', enter coordinates ('
                                              'like this: A1 or '
                                              'b2): ')
        try:
            if int(shot[1:]) > 10 or int(shot[1:]) < 1:
                continue
            if ord(shot[0].lower()) < 97 or ord(shot[0].lower()) > 106:
                continue
        except (ValueError, IndexError):
            continue
        if shot not in game.shoots:
            game.shoots.add(shot)
            break

    return shot[0], int(shot[1:])


def create_fields(name1, name2):
    """
    create fields and game with these fields
    :param name1, name2: players' names
    :return:
    """
    # actually following 2 'while' loops will do one iteration once per ten
    # times in other case - ot will never starts 'cause it has been tested
    # 'generate_field' function and it return correct field in 90.46% cases
    field1 = generate_field(just_field())
    while not is_valid(field1[0], field1[1]):
        field1 = generate_field(just_field())
    field1 = Field(field1[0], field1[1])

    field2 = generate_field(just_field())
    while not is_valid(field2[0], field2[1]):
        field2 = generate_field(just_field())
    field2 = Field(field2[0], field2[1])

    field01 = Field(just_field(), field1.ships)
    field02 = Field(just_field(), field2.ships)

    game = Game(players=[name1, name2], fields={'field' + name1: field1,
                                                'field' + name2: field2,
                                                'field' + name1 + '_hidden':
                                                    field01,
                                                'field' + name2 + '_hidden':
                                                    field02})
    return game


def play():
    """
    organize and manage game
    """
    name1 = input('1st player\'s name: ')
    name2 = input('2st player\'s name: ')

    game = create_fields(name1, name2)

    show_field = True if input('players, if you want your fields to be '
                               'shown (you will see field each other) enter '
                               '\'yes\' else just press Enter: '
                               '') == 'yes' else False
    system('cls')
    while True:
        if show_field:
            print('■ - your ships\n░ - miss/just sea\n√ - nice shot!')
            print('player ' + game.current_player + ', your field:')
            game.fields['field' + game.current_player].display()
        else:
            print('░ - miss/just sea\n√ - nice shot!')
        print('player ' + game.current_player + ', your opponent\'s field:')
        game.fields['field' + game.opposite_player + '_hidden'].display()
        shot = read_coord(game)
        game.shoot_at(game.fields['field' + game.opposite_player], shot)
        if not game.fields['field' + game.opposite_player].ships:
            print(game.current_player + ', Congratulations!\nYOU WON!')
            break
        system('cls')


if __name__ == '__main__':
    play()
