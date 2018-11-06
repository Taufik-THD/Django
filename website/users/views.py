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

from rest_framework import generics, permissions
import jwt

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
    email = user.values('email')[0]['email']
    if email:
        data = user.values('password')[0]
        hashed = bcrypt.hashpw(str(request.POST['password']), str(data['password']))

        if hashed == data['password']:
            token = jwt.encode({'email': email}, 'secret_token', algorithm='HS256')

            # decoded = jwt.decode(token, data['password'], algorithms=['HS256'])
            # print(decoded)

            return HttpResponse('Sign In success, your token: '+ token)
        else:
            return HttpResponse('Wrong password...')

    else:
        return HttpResponse('Email is not defined...')
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im1lbGFAcm92aWFuaS5jb21zIn0.dYVNedGaM618Yj7Zmig-KDRPAwWAft6j96kLKwxmnzI
@csrf_exempt
def update(request, data):
    headers = request.META.get('HTTP_TOKEN')
    
    try:
        decode = jwt.decode(str(headers), 'secret_token', algorithms=['HS256'])
        
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
        
    except:
        print 'gagal'
        
        return HttpResponse('Please input a valid token..')
    

@csrf_exempt
def delete(request, data):
    Users.objects.filter(id=data).delete()
    print(data)
    return HttpResponse('delete success...')
