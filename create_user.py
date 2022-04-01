from getpass import getpass
import sys

from webapp import create_app
from webapp.user.models import db, User

def choose_role():
    while True:
        role = input('Please type role: admin or user ')

        if role.lower() == 'admin':
            return role
        elif role.lower() == 'user':
            return role
        else:
            print('Please type: admin or user')

app = create_app()

with app.app_context():
    username = input('Enter username:')

    if User.query.filter(User.username == username).count():
        print('This username already exists')
        sys.exit(0)

    password1 = getpass('Enter password:')
    password2 = getpass('Confirm password:')

    if not password1 == password2:
        print('Passwords are not the same')
        sys.exit(0)

    role = choose_role()

    if role.lower() == 'admin':
        new_user = User(username=username, role='admin')
        new_user.set_password(password1)
    
    elif role.lower() == 'user':
        new_user = User(username=username, role='user')
        new_user.set_password(password1)

    db.session.add(new_user)
    db.session.commit()
    print('User with id {} added'.format(new_user.id))
