"""
Create your views here.
"""
import json
import os
import sys
from ingredients import (
    get_ingredients,
    get_calories,
    on_menu
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status  # pylint: disable=unused-import


class BusinessLogic(APIView):
    """
    This is an example of adding/modifying slots using business logic, using
    """
    def post(self, request, _format=None):  # pylint: disable=unused-argument, no-self-use
        """
        Sample post request function.
        """
        # this builds up a list of already ordered items, so we can compare again it
        # to stop against duplicate items
        items_ordered = []
        if '_FOOD_MENU_' in request.data['slots']:
            for food_item in request.data['slots']['_FOOD_MENU_']['values']:
                if food_item['resolved'] == 1:
                    items_ordered.append(food_item['value'])
                if food_item['resolved'] == -1 and food_item['food_menu_dest'] != 'NULL':
                    food_item['tokens'] = food_item['food_menu_dest']

        if '_MISSING_ITEMS_' in request.data['slots']:
            request.data['slots'].pop('_MISSING_ITEMS_', None)

        missing_items = []

        # ingredients_list logic
        if (request.data['state'] == 'ingredients_list'):

            calorie_count = 0
            ingredients_list = []

            if '_FOOD_MENU_' in request.data['slots']:
                for food_item in request.data['slots']['_FOOD_MENU_']['values']:
                    if not (food_item['resolved'] == -1 and food_item['tokens'] in items_ordered):
                        food_item['resolved'] = 1
                        food_item['value'] = food_item['tokens']

                        # magical API call
                        food_item['ingredients'] = get_ingredients(food_item['tokens'])

                        if food_item['ingredients'] == ['Sorry, that item is not on the menu']:
                             missing_items.append(food_item['value'])

                    if food_item['resolved'] == 1:
                        # magical API call
                        calories = get_calories(food_item['tokens'])
                        if calories:
                            calorie_count = calorie_count + calories 

            # this creates a `_CALORIE_TOTAL_` slot for our response
            request.data['slots']['_CALORIE_TOTAL_'] = {
                'type': "int",
                'values': [
                    {
                        "value": calorie_count,
                        "tokens": calorie_count,
                        "resolved": 1,
                    }
                ]
             }
        # food_order logic
        if (request.data['state'] == 'food_order'):

            if '_FOOD_MENU_' in request.data['slots']:
                for food_item in request.data['slots']['_FOOD_MENU_']['values']:
                    if 'resolved' in food_item and food_item['resolved'] == -1:
                        if food_item['tokens'] not in items_ordered:
                            food_item['resolved'] = 1
                            food_item['value'] = food_item['tokens']

                            # magical API call
                            if not on_menu(food_item['value']):
                                missing_items.append(food_item['value'])

        # this deals with the tokens we extracted that are not on the menu, and
        # creates a `_MISSING_ITEMS_` slot for our response
        if missing_items:
            for item in missing_items:
                for food_item in request.data['slots']['_FOOD_MENU_']['values']:
                    if ('value' in food_item and food_item['value'] == item):
                        request.data['slots']['_FOOD_MENU_']['values'].remove(food_item)
                        break

            request.data['slots']['_MISSING_ITEMS_'] = {
                'type': "list",
                'values': [
                    {
                        "value": missing_items,
                        "tokens": missing_items,
                        "resolved": 1,
                    }
                ]
             }

        # return the business logic payload
        return Response(request.data)
