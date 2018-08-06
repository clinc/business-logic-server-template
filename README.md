# Business Logic Server Template

A template server for business logic intergation with the Clinc AI platform.

# Dependencies
- [docker](https://docs.docker.com/install/)
- [docker-compose](https://docs.docker.com/compose/)


# Start the server
```
docker-compose up
```

# Business logic interface

## Request

On every request, Clinc will check (1) if the you have business logic set up, and (2) whether the current competency is enabled with business logic. If both conditions are true, it will call your business logic with a request similar to the following:

```
POST /<BL-URL> HTTP/1.1
{
    "lat": 42.2730207,
    "qid": "6d090a7e-ba91-4b49-b9d5-441f179ccbbe",
    "lon": -83.7517747,
    "state": "transfer"
    "dialog": "lore36ho5l4pi9mh2avwgqmu5mv6rpxz/98FJ",
    "device": "web",
    "query": "I want to transfer $400 from John's checking account to my credit card account.
    "time_offset": 300,
    "slots": {
        "_ACCOUNT_FROM_": {
            "type": "string",
            "required_matches": "GT 0",
            "candidates": [
                {
                "tokens": "John's checking account",
                "resolved": -1
                }
            ]
        },
        "_ACCOUNT_TO_": {
            "type": "string",
            "required_matches": "GT 0",
            "candidates": [
                {
                "tokens": "credit card",
                "resolved": -1
                }
            ]
        },
        "_TRANSFER_AMOUNT_": {
            "type": "string",
            "required_matches": "GT 0",
            "candidates": [
                {
                "tokens": "$400",
                "resolved": -1
                }
            ]
        }
    }
}
```
### Explanation of business logic payload:

  * `lat` : Latitude of the query origin
  * `qid` : Query ID
  * `lon` : Longitutde of the query origin
  * `state` : The state that the classifier predicted for the current query
  * `dialog` : The dialog token
  * `device` : The device the query was made on
  * `query` : The query that was made
  * `time_offset` : The time zone offset from UTC
  * `slots` : The slots that were extracted for the query

The only mutable fields in the business logic payload are `slots` and `state`, which will be explained in more detail below

### Explanation of `slot` dictionary:

  * `required_matches` : The fulfillment criteria for matching a slot, and the supported operators include `EQ` (equal to), `GT` (greater than), `GE` (greater than or equal to), `LT` (less than), and `LE` (less than or equal to)
  * `candidates` : A list of matching candidates extracted form the user query
  * `type` : The type of the data in the slot.  It can be `string`, `date`, `number`, or `money`

### Explanation of `candidate` dictionary:

  * `tokens` : The original tokens that were extracted from the user query
  * `resolved` : Whether an extracted token has already been resolved.  There are three possible values for this:  `-1` for unresolved,  `0` for unsure, and `1` for already resolved.  These will be explained below in the next section

A response back to Clinc should look similar to the following example:

```
HTTP/1.1 200 OK
{
    "lat": 42.2730207,
    "qid": "6d090a7e-ba91-4b49-b9d5-441f179ccbbe",
    "lon": -83.7517747,
    "classifier_state": "transfer"
    "dialog": "lore36ho5l4pi9mh2avwgqmu5mv6rpxz/98FJ",
    "device": "web",
    "query": "I want to transfer $400 from John's checking account to my credit card account.
    "time_offset": 300,
    "state": "clean_hello_start"
    "slots": {
        "_ACCOUNT_FROM_": {
            "type": "string",
            "required_matches": "EQ 1",
            "candidates": [
                {
                    "tokens": "John's checking account",
                    "resolved": 1,
                    "value": "College Checking Account",
                    "account_id": "353675",
                    "balance": "5824.24",
                    "currency": "USD"
                }
            ]
        },
        "_ACCOUNT_TO_": {
            "type": "string",
            "required_matches": "EQ 1",
            "candidates": [
                {
                    "tokens": "credit card",
                    "resolved": 1,
                    "value": "Sapphire Credit Card Account",
                    "account_id": "7725485",
                    "balance": "332.21",
                    "currency": "USD"
                }
            ]
        },
            "_TRANSFER_AMOUNT_": {
            "type": "money",
            "required_matches": "EQ 1",
            "candidates": [
                {
                    "tokens": "$400",
                    "resolved": 1,
                    "value": "400.00",
                    "currency": "USD"
                }
            ]
        }
    }
}
```

### Explanation of new `candidate` keys:

  * `value` : This is the new value you would like to pass back to the AI
  * Every other key besides `tokens`, `resolved`, and `value` can be used to pass arbitrary parameters back to the AI.  In the example we just shown, currency was set by the business logic.

### Examples of `resolved` statuses in `slot` responses:

If the slot is valid and you want to keep it, set `"resolved": 1`, and return it to clinc:

```
"slots": {
    "_ACCOUNT_FROM_": {
        "type": "string",
        "required_matches": "EQ 1",
        "candidates": [
            {
                "tokens": "John's checking account",
                "resolved": 1,
                "value": "College Checking Account",
                "account_id": "353675",
                "balance": "5824.24",
                "currency": "USD"
            }
        ]
    }
}
```

If there are multiple possible values, and you would like the AI to try to determine which is the best match, you can send a `"resolved": 0`, along with an array of possible values for the `values` key:

```
"slots": {
    "_ACCOUNT_TO_": {
        "required_matches": "EQ 1",
        "candidates": [
            {
                "type": "string",
                "tokens": "credit card",
                "resolved": 0,
                "value": [
                    {
                        "value": "College Savings Account",
                        "account_id": "155243",
                        "balance": "4521.10",
                        "currency": "USD"
                    },
                    {
                        "value": "Sapphire Credit Card Account",
                        "account_id": "7725485",
                        "balance": "332.21",
                        "currency": "USD"
                    },
                    {
                        "value": "401K Account",
                        "account_id": "792311",
                        "balance": "12554.23",
                        "currency": "USD"
                    }
                ]
            }
        ]
    }
}
```

If an identified slot doesn't quite match, or is incorrect, a `"resolved": -1` will remove the extracted slot:

```
"slots": {
    "_ACCOUNT_TO_": {
        "type": "string",
        "required_matches": "EQ 1",
        "candidates": [
            {
                "tokens": "credit card",
                "resolved": -1,
                "reason": "You do not have a credit card with us."
            }
        ]
    }
}
```

Adding your own slots:

To add your own slots that can be used in the Jinja response templates, simply add a new key into the `slots` dictionary with a similar structure.  An example with the added slot `TRANSFER_FEE` can be found below:

```
HTTP/1.1 200 OK
{
    "query": "I want to transfer $400 from John's checking account to my credit card account.
    "lat": 42.2730207,
    "lon": -83.7517747,
    "time_offset": 300,
    "dialog": "2F38jGAsDds9ijcxzvkj/98FJ",
    "device": "LaunchPad",
    "state": "transfer_confirm",
    "slots": {
        "_ACCOUNT_FROM_": {
            "type": "string",
            "required_matches": "EQ 1",
            "candidates": [
                {
                    "tokens": "John's checking account",
                    "resolved": 1,
                    "value": "College Checking Account",
                    "account_id": "353675",
                    "balance": "5824.24",
                    "currency": "USD"
                }
            ]
        }
        "_ACCOUNT_TO_": {
            "type": "string",
            "required_matches": "EQ 1",
            "candidates": [
                {
                    "tokens": "credit card",
                    "resolved": 1,
                    "value": "Sapphire Credit Card Account",
                    "account_id": "7725485",
                    "balance": "332.21",
                    "currency": "USD"
                }
            ]
        },
        "_TRANSFER_AMOUNT_": {
            "type": "money",
            "required_matches": "EQ 1",
            "candidates": [
                {
                    "tokens": "$400",
                    "resolved": 1,
                    "value": "400.00",
                    "currency": "USD"
                }
            ]
        },
        "_TRANSFER_FEE_": {
            "type": "money",
            "required_matches": "EQ 1",
            "candidates": [
                {
                    "tokens": "$5.00",
                    "resolved": 1,
                    "value": "5.00",
                    "currency": "USD"
                }
            ]
        }
    }
}
```

Upon a successful response from a business logic server, the new set of variables will be directly passed into your response templates, allowing you to customize your responses with the new slots introduced in the business logic.

### Business Logic Transitions

Business logic transitions can be made by overwriting the `state` key in the business logic payload.  There must be an existing business logic transition between the state you were previously in, and the state you are trying to transition to.  These transitions can be added/removed from competencies with the `Edit` button on a competency's main Spotlight page.  A good way to check if your business logic transition exists between the states you expect it to is to look for it on the State Graph.

# Adding your own business logic

To add your own business logic to this server, simple modify/rewrite the `/my_project/my_app/views.py`

Both `/my_project/my_app/views.py` and `/my_project/my_app/views.py` are example views.  Only `views.py` is used by the business logic server, but both are there as starting point examples.  Similarly, `/my_project/my_app/hotels.py` is just there to make the `hotel_booking` example work, and can be removed.
