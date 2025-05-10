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
        """Selects all users for the frontend to view a list of users

        Returns:
            dictionary: attributes needed for view all users in front end
        """
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "username": self.username
        }

    def single_user(self):
        """Selects a single user for the frontend to use in the user details page

        Returns:
            dictionary: attributes needed for viewing the details of a single user in the frontend
        """
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "profile_image_url": self.profile_image_url,
            "username": self.username,
            "created_on": self.created_on,
            "bio": self.bio
        }
