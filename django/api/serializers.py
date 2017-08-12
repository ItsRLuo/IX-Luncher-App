

from django.contrib.auth.models import User, Group
#from django.db.models.fields import DateField, MultipleChoiceField, IntegerField
from rest_framework import serializers
from api.models import Food, Menu


class RatingSerializer(serializers.Serializer):
	name = serializers.CharField(allow_null=False)
	# description = serializers.CharField(allow_null=True)
	# cal =  serializers.IntegerField(min_value=0)
	rating = serializers.IntegerField(min_value=0)

class FoodSerializer(serializers.ModelSerializer):

	# name = serializers.CharField(allow_null=False)
	# description = serializers.CharField(allow_null=True)
	# cal =  serializers.IntegerField(min_value=0)
	# rating = serializers.MultipleChoiceField(choices=[1,2,3,4,5])
	# types = serializers.MultipleChoiceField(choices=['Halal', 'Vegan', 'Vegetarian'])
	class Meta:
		model = Food
		fields = ('id','name', 'description','cal','types','rating','rating_counter','menuID','ip_list_rated')
        # fields = ('name', 'description', 'cal', 'rating', 'types')


class FoodRatingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Food
		fields =('id','rating')

class FoodRatingCounterSerializer(serializers.ModelSerializer):
	class Meta:
		model = Food
		fields =('id','rating', 'rating_counter')

class MenuSerializer(serializers.ModelSerializer):

	# date = serializers.DateField()
	# title =  serializers.CharField(allow_null=False, max_length=100)
	# caterer = serializers.CharField(allow_null=False, max_length=20)
	# location = serializers.MultipleChoiceField(choices=["KW", "Wingold", "Montreal"], allow_blank=False)
	# menuID = serializers.IntegerField(min_value=0)
	class Meta:
		model = Menu
		fields = ('date', 'title', 'caterer', 'location', 'menuID')
        # fields = ('date', 'title', 'caterer', 'location', 'menuID')



class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
