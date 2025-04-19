from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .fatsecret_api import FatSecretAPI
from .models import ConsumedFood, FoodHistory
from .forms import FoodSearchForm, AddConsumedFoodForm
from datetime import date, timedelta, datetime
from users.models import Log
from django.db.models import Sum, F

api = FatSecretAPI()

@login_required
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
    # Initialize form early
    form = AddConsumedFoodForm(request.POST or None)
    
    # Get food_id from either URL parameter or GET parameter
    food_id = food_id or request.GET.get('food_id')
    
    if not food_id:
        messages.error(request, "No food selected")
        return redirect('tracker:search_food')

    # Get detailed food information
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
            'date_consumed': timezone.now().date()
        }
        form = AddConsumedFoodForm(initial=initial_data)
    
    elif request.method == 'POST' and form.is_valid():
        food_id = form.cleaned_data['food_id']
        date_consumed = form.cleaned_data['date_consumed']
        
        # Get calories for this food
        calories = api.get_calories(food_id)
        
        try:
            # Update existing entry
            existing_entry = ConsumedFood.objects.get(
                user=request.user,
                fatsecret_food_id=food_id,
                date_consumed=date_consumed
            )
            existing_entry.servings += form.cleaned_data['servings']
            existing_entry.calories_per_serving = calories
            existing_entry.save()
            
            # Update log
            log, _ = Log.objects.get_or_create(
                user=request.user,
                created__date=date_consumed,
                defaults={'user': request.user}
            )
            log.dailyCalorieCount = ConsumedFood.objects.filter(
                user=request.user,
                date_consumed=date_consumed
            ).aggregate(
                total=Sum(F('servings') * F('calories_per_serving'))
            )['total'] or 0.0
            log.save()
            
            messages.success(request, "Servings updated for existing entry!")
            return redirect('tracker:search_food')
            
        except ConsumedFood.DoesNotExist:
            # Create new entry with calories
            consumed_food = ConsumedFood(
                user=request.user,
                fatsecret_food_id=food_id,
                servings=form.cleaned_data['servings'],
                date_consumed=date_consumed,
                calories_per_serving=calories
            )
            consumed_food.save()
            
            # Update log
            log, _ = Log.objects.get_or_create(
                user=request.user,
                created__date=date.today(),
                defaults={
                    'user': request.user,
                    'created': timezone.now()  # Set actual datetime
                }
            )
            log.dailyCalorieCount = ConsumedFood.objects.filter(
                user=request.user,
                date_consumed=date_consumed
            ).aggregate(
                total=Sum(F('servings') * F('calories_per_serving'))
            )['total'] or 0.0
            log.save()
            
            messages.success(request, "Food added to your log!")
            return redirect('tracker:add_consumed_food_with_param', food_id=food_id)
    
    # Render the template with the form and food data
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
def calorie_log(request, days=7):
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=days-1)
    
    # Get/create today's log
    today_log, created = Log.objects.get_or_create(
        user=request.user,
        created__date=end_date,
        defaults={'user': request.user}
    )
    ideal_intake = today_log.dailyOptimalCount  # This uses the TDEE calculation
    
    # Get daily calorie totals
    log_entries = []
    for single_date in (end_date - timedelta(n) for n in range(days)):
        # Calculate total calories for the date
        total_calories = api.tally_calories(request.user.id, single_date) or 0.0
        
        # Get log for the date if exists
        date_log = Log.objects.filter(
            user=request.user,
            created__date=single_date
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