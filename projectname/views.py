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
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

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

    serializer_class = DartsPlayerSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        player = DartsPlayer.objects.get(id=self.request.user.id)
        related_players = DartsPlayer.objects.filter(id__in=player.related_players.all())
        player_serializer = DartsPlayerSerializer(player)
        related_players_serializer = DartsPlayerSerializer(related_players, many=True)
        data = {
            'player': player_serializer.data,
            'related_players': related_players_serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)


class ScoreEditView(APIView):
    def patch(self, request):
        data = request.data
        for obj in data:
            id = obj['id']
            player = DartsPlayer.objects.get(id=id)
            serializer = DartsPlayerSerializer(player, data=obj, partial=True)
            if serializer.is_valid():
                serializer.save()
        return Response(status=200)

class UserTokenView(TokenObtainPairView):
    serializer = UserTokenSerializer


class ListUsers(APIView):

    authentication_classes = [JWTAuthentication]
    
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):

        scores = [user.id for user in DartsPlayer.objects.all()]


        return Response(scores)









class DartsPlayerAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data

        # Check the new player's credentials
        try:
            new_player = authenticate(username=data['username'], password=data['password'])
            if not new_player:
                raise AuthenticationFailed('Invalid credentials')
        except KeyError:
            raise AuthenticationFailed('Must provide both username and password')

        # Find the main user's DartsPlayer instance
        try:
            main_player = DartsPlayer.objects.get(id=request.user.id)
        except DartsPlayer.DoesNotExist:
            raise AuthenticationFailed('Main user has no associated DartsPlayer instance')

        # Add the new player to the related_players field of the main user's DartsPlayer instance
        main_player.related_players.add(new_player.id)

        return Response({'detail': 'Player added to related players list'}, status=status.HTTP_200_OK)
