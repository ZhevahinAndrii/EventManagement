from datetime import timedelta

from django.conf import settings
from django.utils.timezone import now
from django.db import models


def one_day_later():
    return now() + timedelta(days=1)


class Event(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    date = models.DateTimeField(default=one_day_later, blank=True)
    location = models.TextField(blank=False)
    organizer = models.ForeignKey(to=settings.AUTH_USER_MODEL, 
                                  on_delete=models.CASCADE, 
                                  related_name='organized_events', 
                                  related_query_name='organized_event')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    max_participants = models.PositiveIntegerField(null=True, blank=True)
    participants = models.ManyToManyField(to=settings.AUTH_USER_MODEL,
                                          related_name='participated_events',
                                          related_query_name='participated_event')
    
    def has_free_slots(self):
        return self.max_participants is None or self.participants.count() < self.max_participants

    def save(self,*args,**kwargs):
        if self.max_participants < (count:=self.participants.count()):
            self.max_participants = count
        return super().save(*args,**kwargs)
            

    def __str__(self):
        return f"{self.title} ({self.date.strftime('%d-%m-%Y %H:%M')})"

    class Meta:
        indexes = (
            models.Index(fields=('title',),name='event_title_index'),
            models.Index(fields=('location',), name='event_location_index')
        )



