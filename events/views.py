from django.shortcuts import render
from rest_framework import generics, status, viewsets
from rest_framework.exceptions import PermissionDenied, ValidationError

from .models import Attendees, Event, Reviews
from .permissions import IsConfirmedOrReadOnly, IsOrganizerOrReadOnly
from .serializers import (EventSerializer, Reviewserializer,
                          confirmAttendanceSerializer)


# Create your views here.
class EventListCreateAPIView(viewsets.ModelViewSet):
    queryset=Event.objects.all()
    serializer_class=EventSerializer
    permission_classes=[IsOrganizerOrReadOnly]

    def perform_create(self,serializer):
        organizer=self.request.user
        if organizer.profile.is_creator:
            serializer.save(organizer=organizer)
        else:
            raise PermissionDenied("You are not authorized to create Events. Update your profile!")


    def perform_destroy(self, instance):
        Event_instance=self.get_object()
        user=self.request.user
        organizer=Event_instance.organizer

        if user !=organizer:
            raise ValidationError("Sorry you are not authorized to delete this Event!")
        Event_instance.delete()



class confirmAttendanceAPIView(viewsets.ModelViewSet):
    queryset=Attendees.objects.all()
    serializer_class=confirmAttendanceSerializer
    permission_classes=[IsConfirmedOrReadOnly]

    def perform_create(self,serializer):
        print(self.request.data['event'])
        attendance_queryset=Attendees.objects.filter(event=self.request.data['event'],
        user=self.request.user)

        if attendance_queryset.exists() :
            raise ValidationError('you already booked this event.')
        serializer.save(user=self.request.user)


class ReviewserializerAPIView(generics.ListCreateAPIView):
    queryset=Reviews.objects.all()
    serializer_class=Reviewserializer

    def perform_create(self, serializer):
        Event_pk=self.kwargs.get("Event_pk")
        Event_instance=generics.get_object_or_404(Event,pk=Event_pk)
        reviewer=self.request.user

        review_queryset=Reviews.objects.filter(Event=Event_instance,reviewer=reviewer)

        if review_queryset.exists():
            raise ValidationError("oops you already made a review!,Try editing your previous review")
        serializer.save(Event=Event_instance,reviewer=reviewer)


class ReviewserializerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Reviews.objects.all()
    serializer_class=Reviewserializer
    permisssion_class=[IsConfirmedOrReadOnly]
