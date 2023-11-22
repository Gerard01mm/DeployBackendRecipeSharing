from django.test import TestCase
import json

from app.models import Recipe
from app.logic import recipeLogic


class RatingTestCase(TestCase):
    def test_add_rating_logic(self):
        # Crea una receta de ejemplo en la base de datos
        recipe = Recipe.objects.create(
            title='Recipe 1',
            ingredients="['Ingredient 1', 'Ingredient 2']",
            instructions="Instructions 1"
        )

        # Crea una solicitud simulada con datos de calificación
        request_data = {
            "user_id": "user123",
            "recipe_id": recipe.id,
            "rating": 4.0
        }
        response = self.client.post('/postratings/',
                                    json.dumps(request_data),
                                    content_type='application/json'
                                    )

        # Llama a la función add_rating_logic con la solicitud simulada
        # # Envía la solicitud, no la respuesta
        response_logic = recipeLogic.add_rating_logic(response.wsgi_request)

        # Verifica que la respuesta de la lógica sea la esperada
        # # Ajusta el código de estado según tu implementación
        self.assertEqual(response_logic['message'], 'Rating added.')
