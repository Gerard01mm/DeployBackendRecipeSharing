from app.models import CustomUser


# Función para verificar la contraseña
def check_password_custom(raw_password, stored_password):
    return raw_password == stored_password


# Ejemplo de cómo usar la función
def login_logic(username, email, password):
    if username:
        if username == "Logout":
            return {'error': 'Logged out.'}

        users = CustomUser.objects.filter(username=username)
    elif email:
        users = CustomUser.objects.filter(email=email)

    if users.exists() and check_password_custom(password, users[0].password):
        # If the password is correct,
        # log the user in and return a success message
        return {'message': 'Logged in.'}
    else:
        # If the user is not found or the password is incorrect,
        # return an error message
        return {'error': 'Invalid username, email, or password.'}
