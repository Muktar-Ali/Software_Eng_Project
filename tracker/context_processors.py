# Makes remaining calls available everywhere
from django.contrib.auth.decorators import login_required

def api_limits(request):
    if request.user.is_authenticated:
        return {
            'remaining_calls': request.user.api_limit.calls_remaining,
            'total_calls': 500  # Your daily limit
        }
    return {}