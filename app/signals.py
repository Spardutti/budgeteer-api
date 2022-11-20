from django.db.models import signals
from django.dispatch import receiver
from .models import WeeklyCategory, CustomUser
from .task import create_weekly_expense, create_monthly_income

# Signals are set up in apps.py && __init.py__

@receiver(signals.post_save, sender=WeeklyCategory, dispatch_uid="create expense")
def create_weekly_expense_signal(sender, instance, created,**kwargs):
    if created:
        # create_weekly_expense.delay(instance.user.id, instance.id)
        create_weekly_expense(instance.user.id, instance.id)


@receiver(signals.post_save, sender=CustomUser, dispatch_uid="create monthly income")
def create_user_monthly_income(sender, instance, created, **kwargs):
    if created and not instance.is_staff:
        # create_monthly_income.delay(instance.id, instance.amount)
        create_monthly_income(instance.id, instance.amount)





   