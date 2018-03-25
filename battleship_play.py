import getpass
from os import system
from sys import exit

from auth.auth import authenticator, authorizor
from auth.exceptions import *
from battleship_auxiliary_functions import *


def create_superuser():
    """
    creating an admin with special permissions which can be realized later
    """
    print('Creating superuser...')
    while True:
        username = input('username: ')
        password = getpass.getpass('password: ')
        try:
            authenticator.add_user(username, password)
        except (UsernameAlreadyExists, PasswordTooWeak) as er:
            print(er)
            continue
        else:
            authorizor.add_permission('make_admin')
            authorizor.add_permission('del_user')
            authorizor.permit_user('make_admin', username)
            authorizor.permit_user('del_user', username)
            break


def create_user():
    """
    create usual user who will be able to play
    """
    print('Creating user...')
    while True:
        username = input('username: ')
        password = getpass.getpass('password: ')
        try:
            authenticator.add_user(username, password)
        except (UsernameAlreadyExists, PasswordTooWeak) as er:
            print(er)
            continue
        else:
            try:
                authorizor.add_permission('play')
            except PermissionError:
                pass
            authorizor.permit_user('play', username)
            break


def logging_in():
    """
    realize user's logging in
    """
    print('Logging in...')
    while True:
        username = input('username: ')
        password = getpass.getpass('password: ')
        try:
            authenticator.login(username, password)
        except (InvalidUsername, InvalidPassword) as er:
            print(er)
            login = input('maybe you don\'t have an account\n'
                          'Do you want to sign up now?\n'
                          '(enter yes if you want, leave field empty '
                          'otherwise)\n')
            if login == 'yes':
                create_user()
            continue
        else:
            break


def logging_out():
    """
    realize user's logging out
    """
    while True:
        username = input('enter your username: ')
        try:
            authenticator.logout(username)
        except InvalidUsername as iu:
            print(iu)
            continue
        else:
            break


def make_admin():
    """
    making superuser from user
    """
    check_user(None, 'make_admin')
    while True:
        try:
            username = input('enter username you want to make a superuser: ')
            authorizor.permit_user('make_admin', username)
            authorizor.permit_user('del_user', username)
            authorizor.forbid_user('play', username)
        except InvalidUsername as iu:
            print(iu, 'try again')
            continue
        else:
            break


def del_user():
    """
    deleting user from users list
    """
    check_user(None, 'del_user')
    while True:
        try:
            username = input('enter username you want to delete: ')
            authenticator.users.pop(username)
        except KeyError as ke:
            print(ke, 'invalid username or user doesn\'t exist')
            choice = input('try again? [y/n]: ')
            if choice == 'y':
                continue
            else:
                break
        else:
            break


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


def manage_users():
    """
    at the game starting call functions which create users and superuser
    """
    system('cls')
    create_superuser()
    system('cls')
    while True:
        add_user = input('add a new user? [y/n]: ')
        if add_user == 'y':
            create_user()
            continue
        elif add_user == 'n':
            break
        else:
            continue


def menu():
    """
    show actions which are allowed and call that which is chosen by user
    :return:
    """
    manage_users()
    system('cls')
    message = 'Choose an action:\n' \
              '(you need to be logged in to play)\n' \
              '1: sign up\n' \
              '2: log in\n' \
              '3: play\n' \
              '4: log out\n' \
              '5: exit\n' \
              '= for superusers\n' \
              '= 6: make superuser from user\n' \
              '= 7: delete user\n'
    while True:
        print(message)
        choice = input('your choice: ')
        choices = {'1': create_user, '2': logging_in, '3': play,
                   '4': logging_out, '5': exit, '6': make_admin, '7': del_user}
        action = choices.get(choice)
        action()


def check_user(num, *args):
    """
    check whether the user is logged in and whether he has permissions which
    gotten as args
    """
    system('cls')
    while True:
        if num:
            name = input(num + 'st player\'s name: ')
        else:
            name = input('enter your name: ')
        if authenticator.is_logged_in(name):
            break
        else:
            print('you need to logged in to do something\n'
                  '1: sign up and log in\n'
                  '2: log in')
            choice = input()
            if choice == '1':
                create_user()
                logging_in()
            elif choice == '2':
                logging_in()
            continue
    try:
        for arg in args:
            if authorizor.check_permission(arg, name):
                return name
            else:
                authorizor.permit_user(arg, name)
    except (PermissionError, NotPermittedError) as perm_er:
        print(perm_er, 'you have no rights here, good bye!')
        exit()


def play():
    """
    organize and manage game
    """

    name1 = check_user('1', 'play')
    name2 = check_user('2', 'play')

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
    menu()
