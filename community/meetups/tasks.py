from celery import shared_task


@shared_task
def set_inactive_after_time(community_id, id):
    from .models import Meetup
    meetup = Meetup.objects.get(community_id=community_id, id=id)
    meetup.active = False
    meetup.save()
