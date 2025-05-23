from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .fatsecret_api import FatSecretAPI
from .models import ConsumedFood
from .forms import FoodSearchForm, AddConsumedFoodForm
from datetime import date, timedelta, datetime
from users.models import Log
from django.db.models import Sum, F
from .decorators import fatsecret_rate_limit  # Import the decorator
from django.utils.timezone import localtime

api = FatSecretAPI()

@login_required
@fatsecret_rate_limit
def search_food(request):
    form = FoodSearchForm(request.GET or None)
    results = None
    
    if form.is_valid():
        query = form.cleaned_data['query']
        response = api.search_food(query)
        
        if response and 'foods' in response and 'food' in response['foods']:
            results = response['foods']['food']
            # Sometimes the API returns a single food as dict instead of list
            if isinstance(results, dict):
                results = [results]
            
            # Add nutrition data to each result
            for food in results:
                nutrition = api.get_nutritional_facts(food['food_id'])
                if nutrition:
                    food['nutrition'] = nutrition
    
    return render(request, 'tracker/search_food.html', {
        'form': form,
        'results': results
    })

@login_required
def add_consumed_food(request, food_id=None):
    form = AddConsumedFoodForm(request.POST or None)
    food_id = food_id or request.GET.get('food_id')

    if not food_id:
        messages.error(request, "No food selected")
        return redirect('tracker:search_food')

    food_data = api.get_food(food_id)
    if not food_data or 'food' not in food_data:
        messages.error(request, "Could not retrieve food details")
        return redirect('tracker:search_food')

    food = food_data['food']
    servings = food.get('servings', {}).get('serving', [])
    if isinstance(servings, dict):
        servings = [servings]
    serving = servings[0] if servings else {}

    if request.method == 'GET':
        initial_data = {
            'food_id': food_id,
            'date_consumed': localtime(timezone.now()).date()
        }
        form = AddConsumedFoodForm(initial=initial_data)

    elif request.method == 'POST' and form.is_valid():
        food_id = form.cleaned_data['food_id']
        date_consumed = form.cleaned_data['date_consumed']
        servings_input = form.cleaned_data['servings']
        calories = api.get_calories(food_id)

        

        # Get or create log for the day and update calorie count
        log, _ = Log.objects.get_or_create(
            user=request.user,
            log_date=date_consumed,
            defaults={'user': request.user}
        )
        # Always create a new ConsumedFood entry
        consumed_food = ConsumedFood.objects.create(
            log = log,
            fatsecret_food_id=food_id,
            servings=servings_input,
            date_consumed=date_consumed,
            calories_per_serving=calories
        )
        log.update_calories()

        messages.success(request, "Food added to your log!")
        return redirect('tracker:add_consumed_food_with_param', food_id=food_id)

    return render(request, 'tracker/add_consumed_food.html', {
        'form': form,
        'food_name': food.get('food_name', 'Unknown Food'),
        'serving_size': serving.get('serving_description', ''),
        'nutrition': {
            'calories': serving.get('calories', '?'),
            'protein': serving.get('protein', '?'),
            'fat': serving.get('fat', '?'),
            'carbs': serving.get('carbohydrate', '?'),
        }
    })


@login_required
#@fatsecret_rate_limit
def calorie_log(request, days=7):
    end_date = localtime(timezone.now()).date()
    start_date = end_date - timedelta(days=days-1)
    
    # Get/create today's log
    today_log, _ = Log.objects.get_or_create(
        user=request.user,
        log_date=end_date,
        defaults={'user': request.user}
    )
    ideal_intake = today_log.dailyOptimalCount  # This uses the TDEE calculation
    
    # Get daily calorie totals
    log_entries = []
    for single_date in (end_date - timedelta(n) for n in range(days)):
        # Calculate total calories for the date
        total_calories = api.tally_calories(request.user.log.id, single_date) or 0.0
        
        # Get log for the date if exists
        date_log = Log.objects.filter(
            user=request.user,
            log_date=single_date
        ).first()
        
        log_entries.append({
            'date': single_date,
            'actual': total_calories,
            'ideal': date_log.dailyOptimalCount if date_log else ideal_intake,
            'difference': total_calories - (date_log.dailyOptimalCount if date_log else ideal_intake)
        })
    
    return render(request, 'tracker/calorie_log.html', {
        'log_entries': sorted(log_entries, key=lambda x: x['date'], reverse=True),
        'days': days,
        'today_log': today_log  # Pass to template if needed
    })