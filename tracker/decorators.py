from django.http import JsonResponse
from functools import wraps
from django.core.exceptions import ObjectDoesNotExist

def fatsecret_rate_limit(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=401)
        
        try:
            # Get/create the limit record
            limit = request.user.api_limit
            limit.reset_if_needed()
            
            if limit.calls_remaining <= 0:
                return JsonResponse(
                    {"error": "Daily API limit exceeded. Try again tomorrow."},
                    status=429
                )
            
            # Proceed with the view
            response = view_func(request, *args, **kwargs)
            
            # Only decrement if successful
            if response.status_code < 400:
                limit.calls_remaining -= 1
                limit.save()
            
            return response
            
        except ObjectDoesNotExist:
            return JsonResponse(
                {"error": "API limit configuration error"},
                status=500
            )
    
    return wrapped_view