from django import template
from ..models import Meetup, Attendee

register = template.Library()

@register.simple_tag
def meetup_timeleft(meetup):
    hours, minutes, seconds = meetup.timeleft()
    timeleft = ""
    if not meetup.active:
        return "expired"
    if hours > 0:
        timeleft += "{}".format(hours)
        if minutes > 0:
            timeleft += ":{} remaining".format(minutes)
    elif minutes > 0:
        timeleft += "{} minutes remaining".format(minutes)
    return timeleft
