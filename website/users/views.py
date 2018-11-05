# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from .models import Users
from .forms import UsersForm
from django.db import connection

import psycopg2
import urlparse
import bcrypt
import json

# Create your views here.

@csrf_exempt
def list_all_users(request):
    list_users = []

    for user in Users.objects.all():
        data = {
            'fullname': user['full_name'],
            'email': user['email']
        }
        list_users.append(data)

    return HttpResponse(list_users)

@csrf_exempt
def sign_up(request):
    password = request.POST['password']
    hashPwd = bcrypt.hashpw(str(password), bcrypt.gensalt())
    user = Users.objects.filter(email=request.POST['email'])

    if user.values('email'):
        return HttpResponse('email exists...')
    else:
        form = UsersForm(request.POST)
        if form.is_valid():
            password = form.save(commit=False)
            password.password = hashPwd
            password.save()
            return HttpResponse('sign up success...')

@csrf_exempt
def sign_in(request):
    user = Users.objects.filter(email=request.POST['email'])

    if user.values('email'):

        data = user.values('password')[0]
        hashed = bcrypt.hashpw(str(request.POST['password']), str(data['password']))

        if hashed == data['password']:
            return HttpResponse('Sign In success...')
        else:
            return HttpResponse('Wrong password...')

    else:
        return HttpResponse('Email is not defined...')

@csrf_exempt
def update(request, data):
    update = Users.objects.filter(id=data).update(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email']
           )

    project = Users.objects.get(id=data)
    form=UsersForm(request.POST,instance=project)
    if form.is_valid():
       form.save(commit=True)

    return HttpResponse('updated')

@csrf_exempt
def delete(request, data):
    Users.objects.filter(id=data).delete()
    print(data)
    return HttpResponse('delete success...')
