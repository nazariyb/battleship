import hashlib

from auth.exceptions import *


class User:
    def __init__(self, username, password):
        """
        Create a new user object. The password will encrypted before storing.
        """
        self.username = username
        self.password = self._encrypt_pw(password)
        self.is_logged_in = False

    def _encrypt_pw(self, password):
        """
        Encrypt the password with the username and return the sha digest.
        """
        hash_string = (self.username + password)
        hash_string = hash_string.encode('utf-8')
        return hashlib.sha256(hash_string).hexdigest()

    def check_password(self, password):
        """
        Return True if the password is valid for this user, false otherwise.
        """
        encrypted = self._encrypt_pw(password)
        return encrypted == self.password


class Authenticator:
    def __init__(self):
        """
        Construct an authenticator to manage users logging in and out
        """
        self.users = {}

    def add_user(self, username, password):
        if username in self.users:
            raise UsernameAlreadyExists(username)
        if not self._strong_pw(password):
            print('password should to have at least 6 symbols '
                  'including lower and uppercase and numbers')
            raise PasswordTooWeak(username)
        self.users[username] = User(username, password)

    def _strong_pw(self, password):
        if len(password) < 6:
            return False
        up_letter = self._check_let(password, 64, 91)
        low_letter = self._check_let(password, 96, 123)
        num = self._check_let(password, 47, 58)
        return up_letter and low_letter and num

    @staticmethod
    def _check_let(password, start, end):
        for letter in password:
            if start < ord(letter) < end:
                return True
        return False

    def login(self, username, password):
        try:
            user = self.users[username]
        except KeyError:
            raise InvalidUsername(username)

        if not user.check_password(password):
            raise InvalidPassword(username, user)

        user.is_logged_in = True
        return True

    def logout(self, username):
        try:
            user = self.users[username]
        except KeyError:
            raise InvalidUsername(username)
        user.is_logged_in = False

    def is_logged_in(self, username):
        if username in self.users:
            return self.users[username].is_logged_in
        return False


authenticator = Authenticator()


class Authorizor:
    def __init__(self, authenticator):
        self.authenticator = authenticator
        self.permissions = {}

    def add_permission(self, perm_name):
        """
        Create a new permission that users can be added to
        """
        try:
            perm_set = self.permissions[perm_name]
        except KeyError:
            self.permissions[perm_name] = set()
        else:
            raise PermissionError('Permission Exists')

    def permit_user(self, perm_name, username):
        """
        Grant the given permission to the user
        """
        try:
            perm_set = self.permissions[perm_name]
        except KeyError:
            raise PermissionError('Permission does not exist')
        else:
            if username not in self.authenticator.users:
                raise InvalidUsername(username)
            perm_set.add(username)

    def forbid_user(self, perm_name, username):
        try:
            perm_set = self.permissions[perm_name]
        except KeyError:
            raise PermissionError('Permission does not exist')
        else:
            if username not in self.authenticator.users:
                raise InvalidUsername(username)
            perm_set.remove(username)

    def check_permission(self, perm_name, username):
        if not self.authenticator.is_logged_in(username):
            raise NotLoggedInError(username)
        try:
            perm_set = self.permissions[perm_name]
        except KeyError:
            raise PermissionError('Permission does not exist')
        else:
            if username not in perm_set:
                raise NotPermittedError(username)
            else:
                return True


authorizor = Authorizor(authenticator)
