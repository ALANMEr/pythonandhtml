from werkzeug.security import check_password_hash


class User():
     def __init__(self,Name,email,password)->None:
        self.Name=Name
        self.email=email
        self.password=password

@classmethod
def check_password_hash(self,hashed_passwoed,password):

    return check_password_hash(self,hashed_passwoed,password)


