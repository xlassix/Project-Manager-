from django.shortcuts import render
from rest_framework.views import APIView
from .models import ActionSerializer,ProjectSerializer,ProjectModel,ActionModel
from rest_framework.response import Response
from rest_framework import generics
from django.db.models import Q
class ProjectList(generics.ListCreateAPIView):
    queryset = ProjectModel.objects.all()
    serializer_class = ProjectSerializer
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    #authentication_classes = [authentication.TokenAuthentication]
    #permission_classes = [permissions.IsAdminUser]

    def post(self, request, format=None):
        data=ProjectSerializer(data=request.data)
        if data.is_valid():
            project=data.create(data.validated_data)
            return Response({"status":"Sucessful","data":project})
        else:
            return Response(data.errors)

class TestGetView(generics.ListAPIView):
    serializer_class = ActionSerializer

    paginate_by = 2

    def get_queryset(self):
        return ActionModel.objects.filter(Q(note__icontains=self.request.query_params.get('h',''))|Q(description__icontains=self.request.query_params.get('h',''))|Q(project_id__id__icontains=self.request.query_params.get('h','')))

# Create your views here.

class TestGetView2(APIView):
    def get(self,request):
        print(request.query_params)
        return Response({"status":"done"})

    def post(self, request,id):
        request.data["project_id"]=id
        data=ActionSerializer(data=request.data)
        if data.is_valid():
            project=data.create(data.validated_data,id)
            return Response({"status":"Sucessful","data":project})
        else:
            return Response(data.errors)



class TestView(APIView):
    def get(self,request,id):
        return Response({"status":"done"})

    def post(self, request,id):
        request.data["project_id"]=id
        data=ActionSerializer(data=request.data)
        if data.is_valid():
            project=data.create(data.validated_data,id)
            return Response({"status":"Sucessful","data":project})
        else:
            return Response(data.errors)

class ActionList(generics.ListCreateAPIView):
    queryset = ActionModel.objects.all()
    serializer_class = ActionSerializer
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    #authentication_classes = [authentication.TokenAuthentication]
    #permission_classes = [permissions.IsAdminUser]

    def post(self, request, format=None):
        return Response({"error":"this method is not allowed"})