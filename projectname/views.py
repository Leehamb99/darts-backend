from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import  DartsPlayer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import DartsPlayerSerializer, UserTokenSerializer, ScoreEditSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, UpdateAPIView

user = DartsPlayer
class UserRegistrationView(APIView):
    def post(self, request):
        serializer = DartsPlayerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return DartsPlayer.objects.filter(id=self.request.user)


class UserViewSet(RetrieveAPIView):
    queryset = DartsPlayer.objects.all()
    serializer_class = DartsPlayerSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return(self.request.user)


class ScoreEditView(UpdateAPIView):
    serializer_class = ScoreEditSerializer
    
    def get_object(self):
        return self.request.user




class UserTokenView(TokenObtainPairView):
    serializer = UserTokenSerializer
    
        

    
    


class ListUsers(APIView):

    authentication_classes = [JWTAuthentication]
    
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):

        """
        Return a list of all users.
        """
        scores = [user.id for user in DartsPlayer.objects.all()]


        return Response(scores)






