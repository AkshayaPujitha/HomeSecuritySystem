from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes,authentication_classes,api_view
from rest_framework.permissions import IsAuthenticated

# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    return render(request,'dashboard.html')
