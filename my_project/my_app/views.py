"""
Create your views here.
"""
import json
from hotels import find_express_deal, check_available_credit
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status  # pylint: disable=unused-import


class BusinessLogic(APIView):
    """
    This is an example of adding/modifying slots using business logic, using
    the `hotel_booking` competency. There is also an example
    for arbitrary state transitions.

    Example competencies used:

        hotel_booking

            type: confirmational

            required slots:

                hotel_type,
                hotel_rating,
                price,
                location

            optional slots:

                transaction type

            example queries:

                - "I want to book a 4 star hotel in minneapolis"
                - "I'm looking to stay at a Hilton for less than $200 a night"
                - "I want an express deal"

       credit_card_offer

            type: informational

            notes: only accessible through business logic transitions

    """
    def post(self, request, _format=None):  # pylint: disable=unused-argument, no-self-use
        """
        Sample post request function.
        """
        # Assign hotel_booking variables
        if '_TRANSACTION_TYPE_' in request.data['slots']:
            transaction_type = request.data['slots']['_TRANSACTION_TYPE_']['candidates'][0]['tokens']
        else:
            transaction_type = None

        if '_LOCATION_' in request.data['slots']:
            location = request.data['slots']['_LOCATION_']['candidates'][0]['tokens']
        else:
            location = None

        if '_PRICE_' in request.data['slots']:
            price = request.data['slots']['_PRICE_']['candidates'][0]['tokens']
        else:
            price = None

        # this loop sets all of the _SLOTS_ to have a `"resovled": 1` so they will be kept
        # through each turn of the conversation.  Currently, each turn the slots are sent
        # with a `"resolved": -1`, so they need to be reset each time, however, they are
        # changing to be persistent based on their resolved status in an update coming soon
        for (slot, slot_data) in request.data['slots'].iteritems():
            if 'candidates' in request.data['slots'][slot]:
                for candidate in range(len(slot_data['candidates'])):
                    request.data['slots'][slot]['candidates'][candidate]['resolved'] = 1
                    if slot != '_DATE_':
                        request.data['slots'][slot]['candidates'][candidate]['value'] = \
                            request.data['slots'][slot]['candidates'][candidate]['tokens']
            else:
                request.data['slots'][slot]['resolved'] = 1

        #magical API call to check their credit
        available_credit = check_available_credit()

        # state transition example
        # if someone does not have enough credit available to pay for the hotel, 
        # redirect them to a credit_card_offer state, and return the payload
        if available_credit < price:
            request.data['state'] = 'credit_card_offer'
            return Response(request.data)

        if transaction_type == 'express deal':
            if location and price:
                # This is our magical API call to find express deals
                hotel = find_express_deal(location, price)
                if hotel:
                    # This is how to add new _SLOTS_ to the business logic json
                    hotel_rating = {
                        "candidates": [
                            {
                                "resolved": 1,
                                "value": hotel['hotel_rating']
                            }
                        ],
                        "required_matches": "EQ 1",
                        "type": "string"
                    }
                    request.data['slots']['_HOTEL_RATING_'] = hotel_rating
                    hotel_type = {
                        "candidates": [
                            {
                                "resolved": 1,
                                "value": hotel['hotel_type']
                            }
                        ],
                        "required_matches": "EQ 1",
                        "type": "string"
                    }
                    request.data['slots']['_HOTEL_TYPE_'] = hotel_type

        # return the modified business logic payload
        return Response(request.data)

