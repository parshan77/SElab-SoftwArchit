import datetime
import hashlib
import random
import string

import django
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response
from user.models import User, Ride
from Bike.models import Bike
from django.shortcuts import render
import requests

import math

from django.db.utils import OperationalError
format_list = [('', '(all)')]
geom_type_list = [('', '(all)')]
try:

    admin = User()
    admin.username = 'admin'
    admin.password = hashlib.md5('admin'.encode('utf-8')).digest()
    admin.isAdmin = True




    try:
        admin.save()
    except django.db.utils.IntegrityError:
        admin = User.objects.get(username='admin')

except OperationalError:
    pass

failed_atts = [0, 0, 0, 0]


class API(viewsets.ViewSet):
    def handle_request(self, request):
        print(request.data)
        try:
            service = request.data["service"]
        except KeyError:
            return HttpResponse('Bad Request', status=400)
        if service == 'register':
            if failed_atts[0] < 3:
                return self.register(request.data)
            else:
                return HttpResponse('Service Unavailable', status=503)

        if service == 'login':
            if failed_atts[1] < 3:
                return self.login(request.data)
            else:
                return HttpResponse('Service Unavailable', status=503)

        if service == 'start_ride':
            if failed_atts[2] < 3:
                return self.start_ride(request.data)
            else:
                return HttpResponse('Service Unavailable', status=503)

        if service == 'finish_ride':
            if failed_atts[3] < 3:
                return self.finish_ride(request.data)
            else:
                return HttpResponse('Service Unavailable', status=503)


        return HttpResponse('Bad Request', status=400)

    @staticmethod
    def register(data):
        url = 'http://127.0.0.1:8000/api/register'
        try:
            response = requests.post(url, data=data, timeout=0.500)
        except:
            failed_atts[0] += 1
            return HttpResponse('Service Unavailable', status=503)
        
        if response.status_code / 100 == 5:
            failed_atts[0] += 1
            return HttpResponse('Service Unavailable', status=503)
        return HttpResponse(response.text, status=response.status_code)

    @staticmethod
    def login(data):
        url = 'http://127.0.0.1:8000/api/login'
        try:
            response = requests.post(url, data=data, timeout=0.500)
        except:
            failed_atts[1] += 1
            return HttpResponse('Service Unavailable', status=503)
        
        print(response.status_code)
        if response.status_code / 100 == 5:
            failed_atts[1] += 1
            return HttpResponse('Service Unavailable', status=503)
        
        return HttpResponse(response.text, status=response.status_code)

    @staticmethod
    def start_ride(data):
        url = 'http://127.0.0.1:8000/api/start_ride'
        try:
            response = requests.post(url, data=data, timeout=0.500)
        except:
            failed_atts[1] += 1
            return HttpResponse('Service Unavailable', status=503)
        
        print(response.status_code)
        if response.status_code / 100 == 5:
            failed_atts[1] += 1
            return HttpResponse('Service Unavailable', status=503)
        
        return HttpResponse(response.text, status=response.status_code)

    @staticmethod
    def finish_ride(data):
        url = 'http://127.0.0.1:8000/api/finish_ride'
        try:
            response = requests.post(url, data=data, timeout=0.500)
        except:
            failed_atts[1] += 1
            return HttpResponse('Service Unavailable', status=503)
        
        print(response.status_code)
        if response.status_code / 100 == 5:
            failed_atts[1] += 1
            return HttpResponse('Service Unavailable', status=503)
        
        return HttpResponse(response.text, status=response.status_code)


class Register(viewsets.ViewSet):
    def handle_request(self, request):
        pass


class Login(viewsets.ViewSet):
    def handle_request(self, request):
        pass

class StartRide(viewsets.ViewSet):
    def handle_request(self, request):
        pass

class FinishRide(viewsets.ViewSet):

    def handle_request(self, request):
       pass
        
