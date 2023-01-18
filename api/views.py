from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RegistrationSerializer

from .models import Registration
# Create your views here.

@api_view(['GET'])
def apiOverview(request):
	api_urls = {
		'List':'/reg-list/',
		'Detail View':'/reg-detail/<str:pk>/',
		'Create':'/reg-create/',
		'Update':'/reg-update/<str:pk>/',
		'Delete':'/reg-delete/<str:pk>/',
		}

	return Response(api_urls)

@api_view(['GET'])
def regList(request):
	registration = Registration.objects.all().order_by('-id')
	serializer = RegistrationSerializer(registration, many=True)
	return Response(serializer.data)

@api_view(['GET'])
def regDetail(request, pk):
	registration = Registration.objects.get(id=pk)
	serializer = RegistrationSerializer(registration, many=False)
	return Response(serializer.data)


@api_view(['POST'])
def regCreate(request):
	serializer = RegistrationSerializer(data=request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)

@api_view(['POST'])
def regUpdate(request, pk):
	registration = Registration.objects.get(id=pk)
	serializer = RegistrationSerializer(instance=registration, data=request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)


@api_view(['DELETE'])
def regDelete(request, pk):
	registration = Registration.objects.get(id=pk)
	registration.delete()

	return Response('Item succsesfully delete!')



