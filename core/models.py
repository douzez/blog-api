from django.template.defaultfilters import slugify  # new
from django.db import models
from django.conf import settings
# Extends the User model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    """ Class that provides the helper functions for creating the user or super user """

    def create_user(self, email, password=None, **extra_fields):
        """ Creates and saves a new user """
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """ Creates and saves a new superuser """
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ Custom User model that supports using email instead of username """

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Tag(models.Model):
    """ Tag to be used on Posts. ManyToMany with Posts """
    name = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             null=True,
                             on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Post(models.Model):
    """ Post object, this is the main object """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             null=True,
                             on_delete=models.SET_NULL)
    tags = models.ManyToManyField('Tag')
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=False)
    body = models.TextField()
    description = models.CharField(max_length=255)
    publish = models.BooleanField(default=False)
    # image = models.ImageField(upload_to='uploads/post',
    #                           blank=True,
    #                           null=True)
    # thumbnail = models.ImageField(upload_to='uploads/post',
    #                               blank=True,
    #                               null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/{self.slug}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
