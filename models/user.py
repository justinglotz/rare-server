class User():

    def __init__(self, id=None, first_name=None, last_name=None, email=None, bio=None, username=None, password=None, profile_image_url=None, created_on=None, active=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.bio = bio
        self.username = username
        self.password = password
        self.profile_image_url = profile_image_url
        self.created_on = created_on
        self.active = active

    def all_users(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "username": self.username
        }

    def single_user(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "profile_image_url": self.profile_image_url,
            "username": self.username,
            "created_on": self.created_on,
            "bio": self.bio
        }
