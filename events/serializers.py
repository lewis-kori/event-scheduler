from rest_framework import serializers
from .models import event,reviews

# serialize the events model
class eventSerializer(serializers.ModelSerializer):
    event= serializers.StringRelatedField(read_only=True,many=True)
    organizer = serializers.StringRelatedField(read_only=True)
    attendees = serializers.StringRelatedField(read_only=True,many=True)
    attendee_count=serializers.SerializerMethodField()
    class Meta:
        model=event
        fields='__all__'

    def get_attendee_count(self,object):
        return object.attendees.count()

class confirmAttendanceSerializer(serializers.ModelSerializer):
    organizer = serializers.StringRelatedField(read_only=True)
    attendees=serializers.StringRelatedField(many=True)
    class Meta:
        model=event
        fields=('id','attendees','organizer',)

class reviewSerializer(serializers.ModelSerializer):
    event=serializers.StringRelatedField(read_only=True)
    reviewer=serializers.StringRelatedField(read_only=True)
    class Meta:
        model=reviews
        fields='__all__'


