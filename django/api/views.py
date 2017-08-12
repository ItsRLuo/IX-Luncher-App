# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.models import User, Group
from api.models import Food, Food, Menu
from rest_framework import viewsets, status
from rest_framework.response import Response

from api.serializers import UserSerializer, GroupSerializer, FoodSerializer, MenuSerializer, FoodRatingSerializer, FoodRatingCounterSerializer

from api.serializers import UserSerializer, GroupSerializer, FoodSerializer, MenuSerializer, RatingSerializer

from django.utils import timezone
from .models import Food as foodDB
import json
from StringIO import StringIO
from rest_framework.parsers import JSONParser
from django.core import serializers
import json


def get_client_ip(request):
   x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
   if x_forwarded_for:
       ip = x_forwarded_for.split(',')[0]
   else:
       ip = request.META.get('REMOTE_ADDR')
   return ip


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class MenuViewSet(viewsets.ModelViewSet):

    queryset =  Menu.objects.all()
    serializer_class = MenuSerializer
    #serializer = UserSerializer(queryset, many=True)
   
    # for menu in serializer.data:
    #         print "menu:" + menu
    #         if menu.date == request.data.date:
    #             print menu + "selected"

    def list(self, request):
      queryset = Menu.objects.all()
      serializer = MenuSerializer(queryset, many=True, context={'request':request})
       
      queryset1 = Food.objects.all()
      serializer1= FoodSerializer(queryset1, many=True, context={'request':request})
      temp=[]
      key_set = set(request.GET.keys())
      if len(serializer.data) > 0:

        temp_set = key_set.intersection(serializer.data[0].keys())

        for menu in serializer.data:
            flag = True
            for key in list(temp_set):
                if menu[key] != request.GET[key]:
                    flag = False

            if flag:
                temp.append(menu)
                menu['food'] = []
                for item in serializer1.data:
                  print item['menuID']
                  print menu['menuID']
                  if item['menuID'] == menu['menuID']:
                    print "Qwe"
                    menu['food'].append(item)
        	    #print temp[0]['menuID']
        	    #dtemp["food"] = temp
        return Response(temp)

      else:
        return Response(serializer.data)








class RateViewSet(viewsets.ModelViewSet):
  queryset = Food.objects.all()
  serializer_class = FoodRatingSerializer


  def create(self,request, pk=None):
   
    queryset = Food.objects.all()
    data = json.loads(json.dumps(request.data))
    
    ip = get_client_ip(request)



    if len(queryset) > 0:
      
        target_food_list = Food.objects.filter(id=int(data["id"]))
        if len(target_food_list) > 0:
          target_food = target_food_list[0]

          ips_rated = target_food.ip_list_rated.split()

          
          print "known:" + str(ips_rated)

          if not ip in ips_rated:
            
            target_food.rating_counter +=1
            target_food.rating = round(float(target_food.rating  + data['rating'] ),1)/target_food.rating_counter
            target_food.ip_list_rated = target_food.ip_list_rated + ' ' + str(ip)
            target_food.save()
            return Response({'status':'ok', 'message': 'user has already rated this food'})
          else:
            return Response({'status': 'ok'})

    return Response({'status': status.HTTP_400_BAD_REQUEST})



class highestRating():
  def __init__(self,name,rating):
    self.name = name
    self.rating = rating


class FoodViewSet(viewsets.ModelViewSet):
  queryset = Food.objects.all()
  serializer_class = FoodSerializer


  def list(self, request, *args, **kargs):
    queryset = Food.objects.all()
    serializer = FoodSerializer(queryset, many=True, context={'request':request})

    key_set = set(request.GET.keys())

    print request.GET

    if "tops" in request.GET:

      tops = request.GET["tops"]
      #print foodDB.objects.get(rating=2).rating
      #g = foodDB.objects.get(rating=2)
      #g.rating = 0
      #g.save()
      #print "Qwe"
      queryset = Food.objects.all()
      #serializer = FoodSerializer(queryset, many=True, context={'request':request})
      topTen = []
      all = [(item['name'],item['rating']) for item in serializer.data]
      all.sort(key=lambda x: x[1], reverse=True)
      if len(all) >= tops:
        all = all[0:tops -1]

      for item in all:
        topTen.append(highestRating(item[0], item[1]))


      topTenSer = RatingSerializer(topTen, many=True)
      #print c.data
      return Response(topTenSer.data)
    
    if len(serializer.data) > 0:
      temp_set = key_set.intersection(serializer.data[0].keys())


      temp = []
      for food in serializer.data:
        flag=True
        for key in list(temp_set):
          if str(food[key]) != str(request.GET[key]):
              flag = False

        if flag:
          temp.append(food)

      return Response(temp)

    return Response({'status': status.HTTP_400_BAD_REQUEST })


      
    # queryset = Food.objects.all()
    # serializer = FoodSerializer(queryset, many=True, context={'request':request})
    

    # return super(FoodViewSet, self).list(request, args, kargs)
