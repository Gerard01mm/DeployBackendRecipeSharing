# Import the 're' module for regular expressions
import re
# Import necessary functions and models from Django's authentication module
from app.models import CustomUser


from app.models import CustomUser

def register_user(username, email, password, request):
    # Check if the provided username already exists in the database
    if CustomUser.objects.filter(username=username).exists():
        return {'error': 'Username already exists.'}

    # Check if the provided email already exists in the database
    if CustomUser.objects.filter(email=email).exists():
        return {'error': 'Email already exists.'}

    # Check the validity of the provided username, email, and password
    if username_check(username):
        if email_check(email):
            if password_check(password):
                # Create a new CustomUser object with the provided data
                new_user = CustomUser(
                    username=username,
                    email=email,
                    password=password
                )
                new_user.save()
                # Return a success message indicating
                # that registration was successful
                return {'message': 'Registration successful.'}
            else:
                return {'error': 'Password not valid'}
        else:
            return {'error': 'Email not valid'}
    else:
        return {'error': 'Username not valid'}


# Function to check the validity of a username
def username_check(username):
    # Check if the length of the username is between 8 and 16 characters
    if 8 <= len(username) <= 16:
        return True
    else:
        return False


# Function to check the validity of an email
def email_check(email):
    # Regular expression pattern for validating email addresses
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    # Check if the string matches the email pattern
    if re.match(pattern, email):
        return True
    else:
        return False


# Function to check the validity of a password
def password_check(password):
    # Check for a minimum length of 8 characters
    if len(password) < 8:
        return False

    # Check if there is at least one special character in the password
    if not re.search(r'[-_!@#$%^&*(),.?":{}|<>]', password):
        return False

    # Check if there is at least one uppercase letter in the password
    if not re.search(r'[A-Z]', password):
        return False

    # Check if there is at least one digit in the password
    if not re.search(r'[0-9]', password):
        return False

    # Check if there is at least one lowercase letter in the password
    if not re.search(r'[a-z]', password):
        return False

    # If it passes all the above checks, the password is valid
    return True
