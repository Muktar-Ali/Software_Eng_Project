from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from users.models import *
from django.utils.timezone import localtime

@receiver(post_save, sender=CustomUser)
def update_today_log_daily_optimal_count(sender, instance, **kwargs):
    # Get today's date
    today = localtime(timezone.now()).date()

    # Find today's log for this user (if it exists)
    try:
        today_log = Log.objects.get(user=instance, log_date=today)
        today_log.save()  # This will trigger the save() method, which recalculates dailyOptimalCount for today's log
    except Log.DoesNotExist:
        # No log for today, so do nothing
        pass

@receiver(post_save, sender=CustomUser)
def create_user_api_limit(sender, instance, created, **kwargs):
    if created:
        UserApiLimit.objects.create(user=instance)