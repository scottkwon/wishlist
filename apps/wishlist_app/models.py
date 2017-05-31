from __future__ import unicode_literals
import re
from django.db import models
from django.contrib import messages

# Create your models here.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
    def check_registration_form(self, request):
        no_error = True
        if not EMAIL_REGEX.match(request.POST['email']):
            messages.error(request, 'Not a valid email!')
            no_error = False
        if len(request.POST['name']) < 2:
            messages.error(request, 'Name must be atleast 2 characters')
            no_error = False
        if len(request.POST['password']) < 8:
            messages.error(request,'Password must be atleast 8 characters')
            no_error = False
        check_user = self.filter(email=request.POST['email'])
        if check_user:
            messages.error(request, 'Email already exists')
            no_error = False
        return no_error

    def verify_login(self, request):
        no_error = True
        if not EMAIL_REGEX.match(request.POST['email']):
            no_error=False
        target = User.objects.filter(email = request.POST['email'])
        if target:
            if request.POST['password'] == target[0].password:
                pass
                # request.session['first_name'] = target[0].first_name
                # request.session['user_id'] = target[0].id
            else:
                no_error = False
                messages.error(request, 'Username and Password do not match')
        else:
            no_error=False
            messages.error(request, 'Email not found')
        return no_error



class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Item(models.Model):
    name= models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Wishlist(models.Model):
    user = models.OneToOneField(User)
    item = models.ManyToManyField(Item)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
