from rest_framework import serializers
from .models import post,vote

class postserializer(serializers.ModelSerializer):
    poster=serializers.ReadOnlyField(source='poster.username')
    poster_id = serializers.ReadOnlyField(source='poster.id')
    votes= serializers.SerializerMethodField()

    class Meta:
        model=post
        fields=['id','title','url','poster_id','poster','votes']

    def get_votes(self,Post):
        return vote.objects.filter(post=Post).count()






class voteserializer(serializers.ModelSerializer):
    class Meta:
        model=vote
        fields=['id']


