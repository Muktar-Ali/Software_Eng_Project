from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from users.models import *


@receiver(post_save, sender=CustomUser)
def update_today_log_daily_optimal_count(sender, instance, **kwargs):
    # Get today's date
    today = timezone.now().date()

    # Find today's log for this user (if it exists)
    try:
        today_log = Log.objects.get(user=instance, created__date=today)
        today_log.save()  # This will trigger the save() method, which recalculates dailyOptimalCount for today's log
    except Log.DoesNotExist:
        # No log for today, so do nothing
        pass

@receiver(post_save, sender=CustomUser)
def create_first_log(sender, instance, created, **kwargs):
    if created:
        Log.objects.create(user=instance)

# New signal handler for TDEE updates
@receiver(pre_save, sender=CustomUser)
def update_tdee_on_user_change(sender, instance, **kwargs):
    if instance.pk:  # Only for existing users
        try:
            original = sender.objects.get(pk=instance.pk)
            if (original.weight != instance.weight or
                original.height != instance.height or
                original.age != instance.age or
                original.gender != instance.gender or
                original.activity_level != instance.activity_level):
                
                # Update all future logs (including today)
                today = timezone.now().date()
                future_logs = Log.objects.filter(
                    user=instance,
                    log_date__gte=today
                )
                for log in future_logs:
                    log.dailyOptimalCount = log.calculate_tdee()
                    log.save(update_fields=['dailyOptimalCount'])
        except sender.DoesNotExist:
            pass