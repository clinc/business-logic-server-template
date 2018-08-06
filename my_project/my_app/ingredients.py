def get_ingredients(food_item):

    if food_item == 'hamburger':
        return [
            'ground beef patty',
            'brioche bun',
            'onions',
            'lettuce',
            'tomato',
            'pickles',
            'ketchup',
            'mustard'
        ]
    elif food_item == 'cheeseburger':
        return [
            'ground beef patty',
            'brioche bun',
            'onions',
            'lettuce',
            'tomato',
            'pickles',
            'ketchup',
            'mustard',
            'cheddar cheese'
        ]
    elif food_item == 'chicken sandwich':
        return [
            'breaded chicken breast',
            'brioche bun',
            'lettuce',
            'tomato',
            'mayo'
        ]
    elif food_item == 'fish sandwich':
        return [
            'battered cod filet',
            'tartar sauce',
            'lettuce',
            'lemon juice',
            'hot sauce'
        ]
    elif food_item == 'chicken tenders':
        return [
            'breaded chicken tenders'
        ]
    elif food_item == 'french fries':
        return [
            'idaho potatoes cooked in peanut oil',
            'sea salt'
        ]
    elif food_item == 'onion rings':
        return [
            'breaded onion slices'
        ]
    elif food_item == 'veggie burger':
        return [
            'black bean patty',
            'brioche bun',
            'lettuce',
            'tomato',
            'onion',
            'mayo',
            'feta cheese'
        ]
    elif food_item == 'milkshake':
        return [
            'vanilla ice cream',
            'milk',
            'whipped cream'
        ]
    elif food_item == 'quinoa salad':
        return [
            'mixed greens',
            'cherry tomatoes',
            'avocado',
            'quinoa',
            'onion',
            'vinaigrette',
            'walnuts'
        ]
    else:
        return ['Sorry, that item is not on the menu']

def get_calories(food_item):

    if food_item == 'hamburger':
        return 354 
    elif food_item == 'cheeseburger':
        return 455 
    elif food_item == 'chicken sandwich':
        return 515 
    elif food_item == 'fish sandwich':
        return 565 
    elif food_item == 'chicken tenders':
        return 230 
    elif food_item == 'french fries':
        return 365 
    elif food_item == 'onion rings':
        return 480 
    elif food_item == 'veggie burger':
        return 124 
    elif food_item == 'milkshake':
        return 350 
    elif food_item == 'quinoa salad':
        return 296 
    else:
        return 0

def on_menu(food_item):

    if food_item in [
        'hamburger',
        'cheeseburger',
        'chicken sandwich',
        'fish sandwich',
        'chicken tenders',
        'french fries',
        'onion rings',
        'veggie burger',
        'milkshake',
        'quinoa salad'
    ]:
        return True

    return False
