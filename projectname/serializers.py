from rest_framework import serializers
from .models import DartsPlayer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class DartsPlayerSerializer(serializers.ModelSerializer):
    class Meta:
            model = DartsPlayer
            fields = ['id', 'username', 'password', 'score', 'darts_thrown', 'T20_count', 'games_played', 'games_won', 'related_players']

    def create(self, validated_data):
            user = DartsPlayer.objects.create(**validated_data)
            user.set_password(validated_data['password'])
            user.save()
            return user

    def partial_update(self, instance, validated_data):
        instance.score += validated_data.get('score', instance.score)
        instance.save()
        return instance
        
        
class UserTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return (token)

class ScoreField(serializers.Field):
    def to_representation(self, obj):
        return obj

    def to_internal_value(self, data):
        try:
            return int(data)
        except ValueError:
            raise serializers.ValidationError('Score must be an integer')


class ScoreEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = DartsPlayer
        fields = ['score', 'darts_thrown', 'games_played', 'games_won']
    
    def update(self, instance, validated_data):
        games_won = validated_data.pop('games_won', None)
        score = validated_data.pop('score', None)
        darts_thrown = validated_data.pop('darts_thrown', None)
        if score & darts_thrown is not None:
            instance.score += score
            instance.darts_thrown += darts_thrown
            instance.games_played += 1
            if games_won is not None:
                instance.games_won += 1
        return super().update(instance, validated_data)


