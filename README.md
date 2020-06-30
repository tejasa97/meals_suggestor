# Meals Suggestor
##### (As part of L*****a***n challenge)

Meals Suggestor is an app you can use to plan out your meals for the week to reach your fitness goals.

  - Get multiple meal combo suggestions that comply with your planned calorie intake for the day
  - Save your chose meal combo to your weekly planner
  - View your weekly planner 
## Tech

Meals Suggestor uses a number of open source projects that comprise it's core components

* [Python]
* [Flask]
* [SQLAlchemy]
* [PostgreSQL]
* [Redis]

## Installation

Meals Suggestor can be built and run locally with docker and docker-compose

1. Clone this repository  
2. Refer links [docker-install]  and [docker-compose-install] to install the latest versions of docker and docker-compose *(check system compatibility)*
3. **(Optional)** Sign up for [Spoonacular] and obtain an API KEY, and replace the existing key in the `.env` file (a working demo key is already in repository)
3. Run the deployment with docker-compose
    ```sh
    $ docker-compose up --build
    ```
    ##### Note:
    The deployment uses Nginx for reverse proxying the API calls and runs on port 8080, so if you have any webserver already running on port 8080, you will have to stop it.
    ```sh
    $ sudo service stop apache2
    ```

## Usage

Meals Suggestor provides for 3 APIs, the instructions on using them are indicated below

### REST APIs <br>
1. Get meal suggestions with max total calories for the day provided <br>

    **Request:**
     ```sh
     $ curl 'http://localhost/api/meals/suggestion?calories=2000&day=Sunday' | json_pp
     ```
    **Response:**
     ```sh
    {
       "total_calories" : 1892,
       "meals" : [
          {
             "name" : "Freaky Hand Sandwiches",
             "calories" : 639,
             "meal_id" : 426892
          },
          {
             "calories" : 603,
             "meal_id" : 372675,
             "name" : "Torta della Nonna (Grandma's Cake)"
          },
          {
             "meal_id" : 9897,
             "calories" : 650,
             "name" : "Crouching Cabbage, Hidden Mushrooms"
          }
       ]
     }
     ```
     
     Every time the above API is called, a new meals combo is provided.
     The `meal_id` corresponding to the meal is utilised to confirm a particular meals combo, or individual meals from different combinations. 
     
     The following API indicates how a meal combination (or meals from different combinations) can be confirmed to the day meal planner.
     
2.  Confirm a meals suggestion (or individual meals) for a day <br>

    **Request:**
    ```sh
    $ curl --header "Content-Type: application/json" --request POST --data '{"day":"Sunday","calories":2000, "meal_ids":[426892, 372675, 9897]}' http://localhost/api/meals/confirm_suggestion | json_pp    
    ```
    **Response:**
    ```sh
    {
       "total_calories" : 1892,
       "meals" : [
          {
             "calories" : 639,
             "meal_id" : 426892,
             "name" : "Freaky Hand Sandwiches"
          },
          {
             "name" : "Torta della Nonna (Grandma's Cake)",
             "meal_id" : 372675,
             "calories" : 603
          },
          {
             "name" : "Crouching Cabbage, Hidden Mushrooms",
             "meal_id" : 9897,
             "calories" : 650
          }
       ]
    }
    ```
    ##### Note: 
    1. The daily plans can be added in any order (eg: Friday, Wednesday, Monday, etc)
    2. The plan for a day can be updated by issuing the API for the same day with the new desired ```meal_ids```.
    
    To view the added meals combination in the weekly meal planner, you can use the following API.
3. Get current weekly meal planner <br>

    **Request:**
    ```sh
    $ curl http://localhost/api/meals/weekly_plan | json_pp
    ```
    **Response:**
    ```sh
    {
       "total_calories_week" : 1892,
       "plan" : [
          {
             "day" : "Sunday",
             "day_calories" : 1892,
             "meals" : [
                {
                   "calories" : 639,
                   "meal_id" : 426892,
                   "name" : "Freaky Hand Sandwiches"
                },
                {
                   "meal_id" : 372675,
                   "name" : "Torta della Nonna (Grandma's Cake)",
                   "calories" : 603
                },
                {
                   "calories" : 650,
                   "meal_id" : 9897,
                   "name" : "Crouching Cabbage, Hidden Mushrooms"
                }
             ]
          }
       ]
    }
    ```
    Below is an example weekly plan obtained after having confirmed meal suggestions for all days of the week <br>
    **Response:**
    ```sh
    {
        "plan": [
            {
                "day": "Sunday",
                "meals": [
                    {
                        "meal_id": 508950,
                        "name": "Chocolate Pear Tartlets",
                        "calories": 430
                    },
                    {
                        "meal_id": 887560,
                        "name": "Chocolate Chip Strawberry Shortcakes",
                        "calories": 453
                    },
                    {
                        "meal_id": 526894,
                        "name": "Grilled Lime Chicken Leg Quarters",
                        "calories": 465
                    }
                ],
                "day_calories": 1348
            },
            {
                "day": "Monday",
                "meals": [
                    {
                        "meal_id": 406312,
                        "name": "Cherry Nut Ice Cream",
                        "calories": 613
                    },
                    {
                        "meal_id": 112134,
                        "name": "Baked Cauliflower Cheese Soup",
                        "calories": 622
                    },
                    {
                        "meal_id": 113845,
                        "name": "Autumn Parfait",
                        "calories": 621
                    }
                ],
                "day_calories": 1856
            },
            {
                "day": "Tuesday",
                "meals": [
                    {
                        "meal_id": 426892,
                        "name": "Freaky Hand Sandwiches",
                        "calories": 639
                    },
                    {
                        "meal_id": 372675,
                        "name": "Torta della Nonna (Grandma's Cake)",
                        "calories": 603
                    },
                    {
                        "meal_id": 9897,
                        "name": "Crouching Cabbage, Hidden Mushrooms",
                        "calories": 650
                    }
                ],
                "day_calories": 1892
            },
            {
                "day": "Wednesday",
                "meals": [
                    {
                        "meal_id": 206324,
                        "name": "Nilla Wafer-Banana Cake",
                        "calories": 932
                    },
                    {
                        "meal_id": 1142563,
                        "name": "Chocolate Pudding Pie",
                        "calories": 915
                    },
                    {
                        "meal_id": 590873,
                        "name": "Biscoff Marshmallow Pie",
                        "calories": 913
                    }
                ],
                "day_calories": 2760
            },
            {
                "day": "Thursday",
                "meals": [
                    {
                        "meal_id": 706965,
                        "name": "Chicken and Rice Noodle Stir-Fry with Ginger and Basil",
                        "calories": 338
                    },
                    {
                        "meal_id": 462117,
                        "name": "Asian Roll Lettuce Wrap",
                        "calories": 372
                    },
                    {
                        "meal_id": 160015,
                        "name": "Pan-Seared Halibut with Wine-Braised Leeks",
                        "calories": 346
                    }
                ],
                "day_calories": 1056
            },
            {
                "day": "Friday",
                "meals": [
                    {
                        "meal_id": 593243,
                        "name": "Chicken & Rice with Béchamel",
                        "calories": 933
                    },
                    {
                        "meal_id": 564354,
                        "name": "Apple Walnut Spinach Salad",
                        "calories": 929
                    },
                    {
                        "meal_id": 602612,
                        "name": "Spinach Mushroom and Bacon Cheese Fondue",
                        "calories": 881
                    }
                ],
                "day_calories": 2743
            },
            {
                "day": "Saturday",
                "meals": [
                    {
                        "meal_id": 1041378,
                        "name": "Candy Corn Cupcakes with Real Candy Corn Frosting #HalloweenTreatsWeek",
                        "calories": 544
                    },
                    {
                        "meal_id": 52768,
                        "name": "Double-Crust Cherry Tart",
                        "calories": 572
                    },
                    {
                        "meal_id": 247746,
                        "name": "Bacon Wrapped Stuffed Medjool Dates",
                        "calories": 549
                    }
                ],
                "day_calories": 1665
            }
        ],
        "total_calories_week": 13320
    }    
    ```

    ##### Note: 
      To add the meal plans afresh or delete all existing data(Postgres/Redis), you will need to stop and kill the running containers and then remove the Postgres and Redis v    volumes that were created.
    ```sh
    $ docker rm -f $(docker ps -a -q)
    $ docker volume remove postgres_db redis_dump
    ```

   [Python]: <https://www.python.org/>
   [Redis]: <https://redis.io/>
   [PostgreSQL]: <https://www.postgresql.org/>
   [Flask]: <https://flask.palletsprojects.com/en/1.1.x/>
   [SQLAlchemy]: <https://www.sqlalchemy.org/>
   [docker-install]: <https://docs.docker.com/get-docker/>
   [docker-compose-install]: <https://docs.docker.com/compose/install/>
   [Spoonacular]: <https://spoonacular.com/food-api/console#Dashboard>
