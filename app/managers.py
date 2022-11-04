from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username,email,  password):
        user = self.create_user(username, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user