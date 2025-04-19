from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from tracker.models import ConsumedFood
from users.models import Log

@receiver([post_save, post_delete], sender=ConsumedFood)
def update_log_calories(sender, instance, **kwargs):
    """Update the log whenever food entries change"""
    log = Log.objects.filter(
        user=instance.user,
        created__date=instance.date_consumed
    ).first()
    if log:
        log.update_calories()