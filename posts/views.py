from django.shortcuts import render
from .serializer import postserializer,voteserializer
from .models import post,vote
from rest_framework import generics,permissions,mixins,status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

class postlist(generics.ListCreateAPIView):
    queryset = post.objects.all()
    serializer_class = postserializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(poster=self.request.user)

class postretrive(generics.RetrieveDestroyAPIView):
    queryset = post.objects.all()
    serializer_class = postserializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        poster=post.objects.filter(pk=kwargs['pk'],poster=self.request.user)

        if poster.exists():
            return self.destroy(request,*args,**kwargs)
        else:
            raise ValidationError('this is not ur post to delete')


class votecreate(generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = voteserializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user=self.request.user
        posts= post.objects.get(pk=self.kwargs['pk'])
        return vote.objects.filter(voter=user,post=posts)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError('U have voted once!')

        serializer.save(voter=self.request.user,post=post.objects.get(pk=self.kwargs['pk']))

    def delete(self,request,*args,**kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError('U have never voted!')


