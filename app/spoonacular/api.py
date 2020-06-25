from app.spoonacular.config import BASE_URL, API_KEY
from app.config import MAX_RESULTS
import requests

class Spoonacular(object):

    def __init__(self):
    
        self.API_KEY = API_KEY
    
    def get_recipies_by_nutrients(self, calories):
    
        url = f'{BASE_URL}/recipes/findByNutrients'

        query_params = {
            'number'      : MAX_RESULTS,
            'apiKey'      : self.API_KEY,
            'maxCalories' : calories,
            'minCalories' : max(0, calories - max(10, int(calories*0.1))) # 10% lesser than `maxCalories`, and at least less by `10`
        }

        try:
            req = requests.get(url, params=query_params, timeout=5)
        except requests.exceptions.ConnectionError:
            raise Exception("Cannot access the server")

        if req.status_code != 200:
            if req.status_code == 401:
                raise Exception("Invalid API key provided!")

            else:
                raise Exception("Failed to obtain the data")

        return req.json()
