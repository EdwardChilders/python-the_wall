from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt
from datetime import datetime, date

def index(request):
    return render(request, 'index.html')


def register(request):
    print(request.POST)
    # code for  registration
    errors = User.objects.register_validator(request.POST)
        # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')
    else:
        # if the errors object is empty, that means there were no errors!
        # retrieve the blog to be updated, make the changes, and save
        hash_browns = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        print(hash_browns)
        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hash_browns
        )
        print(user)
        # redirect to a success route
        request.session['uuid'] = user.id
        return redirect('/wall')



def login(request):
    print(request.POST)
    # code for  registration
    errors = User.objects.login_validator(request.POST)
        # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')
    else:
        # if the errors object is empty, that means there were no errors!
        # retrieve the blog to be updated, make the changes, and save
        user = User.objects.get(email=request.POST['email'])
        print(user)
        # redirect to a success route
        request.session['uuid'] = user.id
        return redirect('/wall')


def wall(request):
    if 'uuid' not in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['uuid']),
        'all_messages': Message.objects.all().order_by("-created_at"),
        'comments': Comment.objects.all().order_by("created_at")
    }
    return render(request, 'wall.html', context)


def logout(request):
    request.session.flush()
    return redirect('/')


def create_message(request):
    print(request.POST)
    logged_user = User.objects.get(id=request.session['uuid'])
    Message.objects.create(
        user_id=logged_user,
        message=request.POST['message']
    )
    return redirect('/wall')


def create_comment(request, message_id):
    print(request.POST)
    logged_user = User.objects.get(id=request.session['uuid'])
    user_message = Message.objects.get(id=message_id)
    Comment.objects.create(
        user_id=logged_user,
        message_id=user_message,
        comment=request.POST['comment']
    )
    return redirect('/wall')


def delete_message(request, message_id):
    user_message = Message.objects.get(id=message_id)

    user_message.delete()
    
    return redirect('/wall')


def delete_comment(request, comment_id):
    user_comment = Comment.objects.get(id=comment_id)
    user_comment.delete()
    
    return redirect('/wall')
