from django.utils import timezone
from .models import VotingPeriod
import calendar
from datetime import timedelta
from apps.dashboard.models import log_activity

def create_monthly_vote():
    now = timezone.now()
    # Create for current month if not exists
    period, created = VotingPeriod.objects.get_or_create(
        month=now.month,
        year=now.year
    )
    if created:
        print(f"Created voting period for {now.month}/{now.year}")
        log_activity(None, 'SYSTEM', f"Creación automática de votación {now.month}/{now.year}")
        # Here we could seed candidates if needed or notify admin
    else:
        print(f"Voting period for {now.month}/{now.year} already exists")

def close_monthly_vote():
    now = timezone.now()
    # Check if it is actually the last day of the month
    last_day = calendar.monthrange(now.year, now.month)[1]
    if now.day != last_day:
        return

    try:
        period = VotingPeriod.objects.get(month=now.month, year=now.year)
        if period.status == 'OPEN':
            period.status = 'CLOSED'
            period.save()
            print(f"Closed voting period for {now.month}/{now.year}")
            log_activity(None, 'SYSTEM', f"Cierre automático de votación {now.month}/{now.year}")
    except VotingPeriod.DoesNotExist:
        print(f"No voting period found for {now.month}/{now.year}")

def reveal_winner():
    now = timezone.now()
    # This runs on day 1 of the NEW month, so we want to reveal the PREVIOUS month
    # Actually, request says: "El día 1 del mes siguiente a las 19:00: Se muestra automáticamente el ganador"
    # So if today is May 1st, we reveal April.
    
    prev_month_date = now - timedelta(days=1)
    month = prev_month_date.month
    year = prev_month_date.year
    
    try:
        period = VotingPeriod.objects.get(month=month, year=year)
        if period.status == 'CLOSED':
            period.status = 'REVEALED'
            period.save()
            print(f"Revealed winner for {month}/{year}")
            log_activity(None, 'SYSTEM', f"Revelación automática de ganador {month}/{year}")
    except VotingPeriod.DoesNotExist:
        print(f"No voting period found for {month}/{year}")
