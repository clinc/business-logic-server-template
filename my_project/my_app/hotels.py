def find_express_deal (location, price):

    if location == 'minneapolis':
        return {
            "hotel_type": "Hilton",
            "hotel_rating": "4 stars"
        }
    if location == 'dallas':
        return {
            "hotel_type": "Holiday Inn",
            "hotel_rating": "3 stars"
        }

    return {
        "hotel_type": "Double Tree",
        "hotel_rating": "5 stars"
    }

def check_available_credit ():
    return 400
