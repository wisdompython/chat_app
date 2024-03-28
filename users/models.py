from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.password_validation import validate_password
# Create your models here.


class CustomManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have a valid email address ")

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, date_of_birth, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have a valid email address ")
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
        raise ValueError("Users must have a valid email address ")
class CustomUser(AbstractBaseUser, PermissionsMixin):
    firstname = models.CharField(max_length=50, null=True)
    lastname = models.CharField(max_length=50,null=True)
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField(null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["date_of_birth"]

    # def __str__(self):
    #     return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True                     

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
    
class UserProfile(models.Model):
    user = models.OneToOneField("CustomUser", on_delete=models.CASCADE)
    bio = models.TextField(null=True)
    profile_pic = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None, null=True, blank=True)

# i want to search for friend and send a request
class FriendRequest(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='friend_request_from', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name="friend_request_to", on_delete=models.CASCADE)
    pending = models.BooleanField(default=True)
    accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)    
class UserNotifications(models.Model):
    notification_name = models.CharField(max_length=500)
    sender = models.ForeignKey(CustomUser, related_name='sent_by', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name='sent_to', on_delete=models.CASCADE)
    friend_request = models.BooleanField(default=False)
    group_invite = models.BooleanField(default=False)
    
class UserFriends(models.Model):
    user = models.ForeignKey(CustomUser, related_name='friend_from', on_delete=models.CASCADE)
    friends = models.ForeignKey(CustomUser, related_name='friend_to', on_delete=models.CASCADE,unique=True )
    created_at = models.DateTimeField(auto_now_add=True)

