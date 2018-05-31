from django.conf import settings
from rest_framework import serializers, viewsets
from .models import Note


class NoteSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Note
        fields = ('title', 'content')

    def create(self, validated_data):
        # import pdb; pdb.set_trace()
        user = self.context['request'].user

        note = Note.objects.create(user=user, **validated_data)
        return note


class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    queryset = Note.objects.all()

    def get_queryset(self):
        user = self.request.user

        if settings.DEBUG:
            return Note.objects.all()
        elif user.is_anonymous:
            return Note.objects.none()
        else:
            return Note.objects.filter(user=user)
