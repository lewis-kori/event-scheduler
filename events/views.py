from django.shortcuts import render
from rest_framework import generics, status, viewsets
from rest_framework.exceptions import PermissionDenied, ValidationError

from .models import event, reviews
from .permissions import IsOrganizerOrReadOnly
from .serializers import (confirmAttendanceSerializer, eventSerializer,
                          reviewSerializer)


# Create your views here.
class eventListCreateAPIView(viewsets.ModelViewSet):
    queryset=event.objects.all()
    serializer_class=eventSerializer
    permission_classes=[IsOrganizerOrReadOnly]

    def perform_create(self,serializer):
        organizer=self.request.user
        if organizer.profile.is_creator:
            serializer.save(organizer=organizer)
        else:
            raise PermissionDenied("You are not authorized to create events. Update your profile!")


    def perform_destroy(self, instance):
        event_instance=self.get_object()
        user=self.request.user
        organizer=event_instance.organizer

        if user !=organizer:
            raise ValidationError("Sorry you are not authorized to delete this event!")
        event_instance.delete()



class confirmAttendanceAPIView(viewsets.ModelViewSet):
    queryset=event.objects.all()
    serializer_class=confirmAttendanceSerializer

    def perform_create(self, serializer):
        event_pk=self.kwargs.get("pk")
        event_=generics.get_object_or_404(event,pk=event_pk)
        attendee=self.request.user
        attendee_queryset=reviews.objects.filter(event=event_,attendees=attendee)

        if attendee_queryset.exists():
            raise ValidationError("You already booked attendance for this event.")
        event_.objects.add(attendee)
        

class reviewSerializerAPIView(generics.ListCreateAPIView):
    queryset=reviews.objects.all()
    serializer_class=reviewSerializer

    
    def perform_create(self, serializer):
        event_pk=self.kwargs.get("event_pk")
        event_instance=generics.get_object_or_404(event,pk=event_pk)
        reviewer=self.request.user

        review_queryset=reviews.objects.filter(event=event_instance,reviewer=reviewer)

        if review_queryset.exists():
            raise ValidationError("oops you already made a review!,Try editing your previous review")
        serializer.save(event=event_instance,reviewer=reviewer)


class reviewSerializerDetailView(viewsets.ModelViewSet):
    queryset=reviews.objects.all()
    serializer_class=reviewSerializer
