from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from rest_framework import serializers


from .models import Event


User = get_user_model()


class EventSerializer(serializers.ModelSerializer):
    organizer = serializers.StringRelatedField()
    participants = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Event
        fields = (
            'id', 'title', 'description', 'date', 'location', 'organizer', 'max_participants', 'participants','created_at', 'updated_at','is_active'
        )
        extra_kwargs = {field:{'required': False} for field in ['description','date','created_at','updated_at','max_participants']}
        extra_kwargs.update({field:{'read_only':True} for field in ['id', 'organizer', 'created_at','updated_at', 'participants','is_active']})
    
    def validate_max_participants(self, value):
        if value is not None and value <=0:
            raise serializers.ValidationError('Maximum count of participants must be > 0 or None')
        return value
    
    def create(self,validated_data):
        user = self.context.get('request').user
        validated_data['organizer'] = user
        return super().create(validated_data)


class EventRegistrationSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=False)

    def validate_user_id(self, value):
        try:
            return User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError({'user': 'User not found'})

    def validate(self,data):
        user = self.context.get('request').user
        event: Event = self.context.get('event')
        target_user = data.get('user_id', user)

        if target_user != user and not user.is_superuser:
            raise serializers.ValidationError({'user': 'You can only register yourself unless you are an admin'})
        if event.participants.filter(id=target_user.id).count() > 0:
            raise serializers.ValidationError({'participants': "This user is already a participant of event"})
        if not event.has_free_slots():
            raise serializers.ValidationError({'max_participants': 'No available slots'})
        
        return {'user': target_user}
    
    def save(self):
        user = self.validated_data['user']
        event: Event = self.context['event']
        
        event.participants.add(user)
        return event


class EventUnregistrationSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=False)

    def validate_user_id(self, value):
        try:
            return User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError({'user': 'User not found'})
        
    def validate(self,data):
        user = self.context.get('request').user
        event: Event = self.context.get('event')
        target_user = data.get('user_id', user)

        if target_user != user and not user.is_superuser:
            raise serializers.ValidationError({'user': 'You can only unregister yourself unless you are an admin'})
        
        if event.participants.filter(id=target_user.id).count() == 0:
            raise serializers.ValidationError({'participants': "This user is not a participant of event"})
        return {'user': target_user}
    
    def save(self):
        user = self.validated_data.get('user')
        event: Event = self.context.get('event')
        
        event.participants.remove(user)
        return event



