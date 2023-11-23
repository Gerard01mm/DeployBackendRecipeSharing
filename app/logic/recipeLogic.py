import json
from app.models import Recipe
from app.models import CustomUser


# Recipe logic
def recipe_logic(title, ingredients, instructions, prep_time, username_id, servings, recipe_type, allergens, request):
    new_recipe = Recipe(title=title,
                        ingredients=ingredients,
                        instructions=instructions,
                        username_id=username_id,
                        preparation_time=prep_time,
                        servings=servings,
                        kcal=calculateCalories(ingredients),
                        recipe_type=recipe_type,
                        allergens=allergens,
                        rating_amount=0,
                        rating_average=0,
                        rating_list={})
    new_recipe.save()
    user = CustomUser.objects.get(username=new_recipe.username_id)
    user.list_own_recipes[new_recipe.id] = new_recipe.toJson()
    user.save()
    return {'message': 'Recipe created.'}


def add_rating_logic(request):
    body = json.loads(request.body.decode('utf-8'))
    user_id = body.get("user_id")
    recipe_id = body.get("recipe_id")
    rating = body.get("rating")

    recipe = Recipe.objects.get(id=recipe_id)

    if recipe is None:
        return {'error': 'Recipe not found.'}
    if user_id in recipe.rating_list:
        previous_rating = recipe.rating_list.pop(user_id)
        recipe.rating_list[user_id] = rating
        recipe.rating_average = (((
                                          recipe.rating_average * recipe.rating_amount) - previous_rating) + rating) \
                                / recipe.rating_amount
        print(recipe.rating_average)
        recipe.save()
        return {'message': 'Rating updated.',
                'rating_average': recipe.rating_average,
                'rating_amount': recipe.rating_amount}
    else:
        recipe.rating_list[user_id] = rating
        recipe.rating_amount += 1
        recipe.rating_average = (recipe.rating_average + rating) / recipe.rating_amount
        recipe.save()
        return {'message': 'Rating added.',
                'rating_average': recipe.rating_average,
                'rating_amount': recipe.rating_amount}


def get_all_recipes():
    recipes = Recipe.objects.all()  # Esto obtiene todos los objetos Recipe, ajusta tu consulta según sea necesario
    recipe_list = [recipe.toJson() for recipe in recipes]
    return {'recipes': recipe_list}


def get_recipes_main():
    recipes_rating = Recipe.objects.order_by("-rating_average")
    recipes_rating_list = [recipe.toJson() for recipe in recipes_rating]
    recipes_recent = Recipe.objects.order_by("-creation_date")
    recipes_recent_list = [recipe.toJson() for recipe in recipes_recent]
    return {'recipes_rating': recipes_rating_list, 'recipes_recent': recipes_recent_list}


def get_list_recipes_by_query(query):
    if not query is None:
        # try:
        recipes = Recipe.objects.all()
        # separate the string query by the string "%A3"

        if "%A3" in query:

            filters_order = query.split("%A3")
            order = filters_order[0]
            if order.split("=")[0] != "order_by":
                return {'error': 'Query not valid.'}

            ordering = order.split("=")[1].split("+")[0]

            if ordering in ["rate", "recent"]:
                if ordering == "recent":
                    ordering = "creation_date"
                elif ordering == "rate":
                    ordering = "rating_average"
                # return {'error': ordering}

                if order.split("=")[1].split("+")[1] == "desc":
                    recipes = Recipe.objects.all().order_by("-" + ordering)
                elif order.split("=")[1].split("+")[1] == "asc":
                    recipes = Recipe.objects.all().order_by(ordering)
                else:
                    return {'error': 'Query not valid.'}
            else:
                return {'error': 'Query not valid.'}

            # separate the string query by the string "%A2"
            if "%A2" in filters_order[1]:
                list_filters = filters_order[1].split("%A2")
                # iterate the list of filters and create a dictionary with the filters, setting the index as the
                # value before the character "=" and the value after the character "=" as a list of values separated
                # by the character "+"
                filters = {}

                for filter in list_filters:
                    if "+" in filter:
                        filters[filter.split("=")[0]] = filter.split("=")[1].split("+")
                    else:
                        filters[filter.split("=")[0]] = filter.split("=")[1]

                for filter in filters:
                    if filter not in ["ingredients", "allergens", "recipe_type", "servings", "kcal", "preparation_time",
                                      "title"]:
                        return {'error': 'Query not valid.'}
                    if filter not in ["ingredients", "allergens", "recipe_type", "servings", "kcal", "preparation_time",
                                      "title"]:
                        return {'error': 'Query not valid.'}
                    if filter == "ingredients":
                        if isinstance(filters[filter], list):
                            for f in filters[filter]:
                                f.replace("%20", " ")
                                recipes = recipes.filter(ingredients__contains=f)
                        else:
                            f = filters[filter].replace("%20", " ")
                            recipes = recipes.filter(ingredients__contains=filters[filter])
                    elif filter == "allergens":
                        if isinstance(filters[filter], list):
                            for f in filters[filter]:
                                f.replace("%20", " ")
                                recipes = recipes.exclude(allergens__contains=f)
                        else:
                            f = filters[filter].replace("%20", " ")
                            recipes = recipes.exclude(allergens__contains=f)
                    elif filter == "recipe_type":
                        if isinstance(filters[filter], list):
                            final = None
                            for f in filters[filter]:
                                f.replace("%20", " ")
                                if final is None:
                                    final = recipes.filter(recipe_type__contains=f)
                                else:
                                    final = final | recipes.filter(recipe_type__contains=f)
                            recipes = final
                        else:
                            f = filters[filter].replace("%20", " ")
                            recipes = recipes.filter(recipe_type__contains=f)
                    elif filter == "servings":
                        if isinstance(filters[filter], list):
                            final = None
                            for f in filters[filter]:
                                f.replace("%20", " ")
                                if final is None:
                                    final = recipes.filter(servings__contains=f)
                                else:
                                    final = final | recipes.filter(servings__contains=f)
                            recipes = final
                        else:
                            f = filters[filter].replace("%20", " ")
                            recipes = recipes.filter(servings__contains=f)
                    elif filter == "kcal":
                        if isinstance(filters[filter], list):
                            final = None
                            for f in filters[filter]:
                                f.replace("%20", " ")
                                if final is None:
                                    final = recipes.filter(kcal__contains=f)
                                else:
                                    final = final | recipes.filter(kcal__contains=f)
                            recipes = final
                        else:
                            f = filters[filter].replace("%20", " ")
                            recipes = recipes.filter(kcal__contains=f)
                    elif filter == "preparation_time":
                        if isinstance(filters[filter], list):
                            final = None
                            for f in filters[filter]:
                                f.replace("%20", " ")
                                if final is None:
                                    final = recipes.filter(preparation_time__contains=f)
                                else:
                                    final = final | recipes.filter(preparation_time__contains=f)
                            recipes = final
                        else:
                            f = filters[filter].replace("%20", " ")
                            recipes = recipes.filter(preparation_time__contains=f)
                    elif filter == "title":
                        if isinstance(filters[filter], list):
                            for f in filters[filter]:
                                f.replace("%20", " ")
                                recipes = recipes.filter(title__contains=f)
                        else:
                            f = filters[filter].replace("%20", " ")
                            recipes = recipes.filter(title__contains=f)
            else:
                filters = {}

                if "+" in filters_order[1]:
                    filters[filters_order[1].split("=")[0]] = filters_order[1].split("=")[1].split("+")
                else:
                    filters[filters_order[1].split("=")[0]] = filters_order[1].split("=")[1]

                filter = filters_order[1].split("=")[0]

                if filter not in ["ingredients", "allergens", "recipe_type", "servings", "kcal", "preparation_time",
                                  "title"]:
                    return {'error': 'Query not valid.'}
                if filter not in ["ingredients", "allergens", "recipe_type", "servings", "kcal", "preparation_time",
                                  "title"]:
                    return {'error': 'Query not valid.'}
                if filter == "ingredients":
                    if isinstance(filters[filter], list):
                        for f in filters[filter]:
                            f.replace("%20", " ")
                            recipes = recipes.filter(ingredients__contains=f)
                    else:
                        f = filters[filter].replace("%20", " ")
                        recipes = recipes.filter(ingredients__contains=filters[filter])
                elif filter == "allergens":
                    if isinstance(filters[filter], list):
                        for f in filters[filter]:
                            f.replace("%20", " ")
                            recipes = recipes.exclude(allergens__contains=f)
                    else:
                        f = filters[filter].replace("%20", " ")
                        recipes = recipes.exclude(allergens__contains=f)
                elif filter == "recipe_type":
                    if isinstance(filters[filter], list):
                        final = None
                        for f in filters[filter]:
                            f.replace("%20", " ")
                            if final is None:
                                final = recipes.filter(recipe_type__contains=f)
                            else:
                                final = final | recipes.filter(recipe_type__contains=f)
                        recipes = final
                    else:
                        f = filters[filter].replace("%20", " ")
                        recipes = recipes.filter(recipe_type__contains=f)
                elif filter == "servings":
                    if isinstance(filters[filter], list):
                        final = None
                        for f in filters[filter]:
                            f.replace("%20", " ")
                            if final is None:
                                final = recipes.filter(servings__contains=f)
                            else:
                                final = final | recipes.filter(servings__contains=f)
                        recipes = final
                    else:
                        f = filters[filter].replace("%20", " ")
                        recipes = recipes.filter(servings__contains=f)
                elif filter == "kcal":
                    if isinstance(filters[filter], list):
                        final = None
                        for f in filters[filter]:
                            f.replace("%20", " ")
                            if final is None:
                                final = recipes.filter(kcal__contains=f)
                            else:
                                final = final | recipes.filter(kcal__contains=f)
                        recipes = final
                    else:
                        f = filters[filter].replace("%20", " ")
                        recipes = recipes.filter(kcal__contains=f)
                elif filter == "preparation_time":
                    if isinstance(filters[filter], list):
                        final = None
                        for f in filters[filter]:
                            f.replace("%20", " ")
                            if final is None:
                                final = recipes.filter(preparation_time__contains=f)
                            else:
                                final = final | recipes.filter(preparation_time__contains=f)
                        recipes = final
                    else:
                        f = filters[filter].replace("%20", " ")
                        recipes = recipes.filter(preparation_time__contains=f)
                elif filter == "title":
                    if isinstance(filters[filter], list):
                        for f in filters[filter]:
                            f.replace("%20", " ")
                            recipes = recipes.filter(title__contains=f)
                    else:
                        f = filters[filter].replace("%20", " ")
                        recipes = recipes.filter(title__contains=f)
        else:
            if "order_by" in query:
                order = query
                ordering = order.split("=")[1].split("+")[0]

                if ordering in ["rate", "recent"]:

                    if ordering == "recent":
                        ordering = "creation_date"
                    elif ordering == "rate":
                        ordering = "rating_average"

                    if order.split("=")[1].split("+")[1] == "desc":
                        recipes.order_by("-" + ordering)
                    elif order.split("=")[1].split("+")[1] == "asc":
                        recipes.order_by(ordering)
                    else:
                        return {'error': 'Query not valid.'}
                else:
                    return {'error': 'Query not valid.'}

            elif "ingredients" in query or "allergens" in query or "recipe_type" in query or "servings" in query or "kcal" in query or "preparation_time" in query or "title" in query:

                if not "%A2" in query:
                    filters = {}

                    if "+" in query:
                        filters[query.split("=")[0]] = query.split("=")[1].split("+")
                    else:
                        filters[query.split("=")[0]] = query.split("=")[1]

                    filter = query.split("=")[0]

                    if filter not in ["ingredients", "allergens", "recipe_type", "servings", "kcal", "preparation_time",
                                      "title"]:
                        return {'error': 'Query not valid.'}
                    if filter == "ingredients":
                        if isinstance(filters[filter], list):
                            for f in filters[filter]:
                                f.replace("%20", " ")
                                recipes = recipes.filter(ingredients__contains=f)
                        else:
                            f = filters[filter].replace("%20", " ")
                            recipes = recipes.filter(ingredients__contains=filters[filter])
                    elif filter == "allergens":
                        if isinstance(filters[filter], list):
                            for f in filters[filter]:
                                f.replace("%20", " ")
                                recipes = recipes.exclude(allergens__contains=f)
                        else:
                            f = filters[filter].replace("%20", " ")
                            recipes = recipes.exclude(allergens__contains=f)
                    elif filter == "recipe_type":
                        if isinstance(filters[filter], list):
                            final = None
                            for f in filters[filter]:
                                f.replace("%20", " ")
                                if final is None:
                                    final = recipes.filter(recipe_type__contains=f)
                                else:
                                    final = final | recipes.filter(recipe_type__contains=f)
                            recipes = final
                        else:
                            f = filters[filter].replace("%20", " ")
                            recipes = recipes.filter(recipe_type__contains=f)
                    elif filter == "servings":
                        if isinstance(filters[filter], list):
                            final = None
                            for f in filters[filter]:
                                f.replace("%20", " ")
                                if final is None:
                                    final = recipes.filter(servings__contains=f)
                                else:
                                    final = final | recipes.filter(servings__contains=f)
                            recipes = final
                        else:
                            f = filters[filter].replace("%20", " ")
                            recipes = recipes.filter(servings__contains=f)
                    elif filter == "kcal":
                        if isinstance(filters[filter], list):
                            final = None
                            for f in filters[filter]:
                                f.replace("%20", " ")
                                if final is None:
                                    final = recipes.filter(kcal__contains=f)
                                else:
                                    final = final | recipes.filter(kcal__contains=f)
                            recipes = final
                        else:
                            f = filters[filter].replace("%20", " ")
                            recipes = recipes.filter(kcal__contains=f)
                    elif filter == "preparation_time":
                        if isinstance(filters[filter], list):
                            final = None
                            for f in filters[filter]:
                                f.replace("%20", " ")
                                if final is None:
                                    final = recipes.filter(preparation_time__contains=f)
                                else:
                                    final = final | recipes.filter(preparation_time__contains=f)
                            recipes = final
                        else:
                            f = filters[filter].replace("%20", " ")
                            recipes = recipes.filter(preparation_time__contains=f)
                    elif filter == "title":
                        if isinstance(filters[filter], list):
                            for f in filters[filter]:
                                f.replace("%20", " ")
                                recipes = recipes.filter(title__contains=f)
                        else:
                            f = filters[filter].replace("%20", " ")
                            recipes = recipes.filter(title__contains=f)
                    return {'recipes': [recipe.toJson() for recipe in recipes]}

                else:

                    list_filters = query.split("%A2")
                    # iterate the list of filters and create a dictionary with the filters, setting the index as the
                    # value before the character "=" and the value after the character "=" as a list of values
                    # separated by the character "+"
                    filters = {}

                    for filter in list_filters:
                        if "+" in filter:
                            filters[filter.split("=")[0]] = filter.split("=")[1].split("+")
                        else:
                            filters[filter.split("=")[0]] = filter.split("=")[1]

                    for filter in filters:
                        if filter not in ["ingredients", "allergens", "recipe_type", "servings", "kcal",
                                          "preparation_time", "title"]:
                            return {'error': 'Query not valid.'}
                        if filter == "ingredients":
                            if isinstance(filters[filter], list):
                                for f in filters[filter]:
                                    f.replace("%20", " ")
                                    recipes = recipes.filter(ingredients__contains=f)
                            else:
                                f = filters[filter].replace("%20", " ")
                                recipes = recipes.filter(ingredients__contains=filters[filter])
                        elif filter == "allergens":
                            if isinstance(filters[filter], list):
                                for f in filters[filter]:
                                    f.replace("%20", " ")
                                    recipes = recipes.exclude(allergens__contains=f)
                            else:
                                f = filters[filter].replace("%20", " ")
                                recipes = recipes.exclude(allergens__contains=f)
                        elif filter == "recipe_type":
                            if isinstance(filters[filter], list):
                                final = None
                                for f in filters[filter]:
                                    f.replace("%20", " ")
                                    if final is None:
                                        final = recipes.filter(recipe_type__contains=f)
                                    else:
                                        final = final | recipes.filter(recipe_type__contains=f)
                                recipes = final
                            else:
                                f = filters[filter].replace("%20", " ")
                                recipes = recipes.filter(recipe_type__contains=f)
                        elif filter == "servings":
                            if isinstance(filters[filter], list):
                                final = None
                                for f in filters[filter]:
                                    f.replace("%20", " ")
                                    if final is None:
                                        final = recipes.filter(servings__contains=f)
                                    else:
                                        final = final | recipes.filter(servings__contains=f)
                                recipes = final
                            else:
                                f = filters[filter].replace("%20", " ")
                                recipes = recipes.filter(servings__contains=f)
                        elif filter == "kcal":
                            if isinstance(filters[filter], list):
                                final = None
                                for f in filters[filter]:
                                    f.replace("%20", " ")
                                    if final is None:
                                        final = recipes.filter(kcal__contains=f)
                                    else:
                                        final = final | recipes.filter(kcal__contains=f)
                                recipes = final
                            else:
                                f = filters[filter].replace("%20", " ")
                                recipes = recipes.filter(kcal__contains=f)
                        elif filter == "preparation_time":
                            if isinstance(filters[filter], list):
                                final = None
                                for f in filters[filter]:
                                    f.replace("%20", " ")
                                    if final is None:
                                        final = recipes.filter(preparation_time__contains=f)
                                    else:
                                        final = final | recipes.filter(preparation_time__contains=f)
                                recipes = final
                            else:
                                f = filters[filter].replace("%20", " ")
                                recipes = recipes.filter(preparation_time__contains=f)
                        elif filter == "title":
                            if isinstance(filters[filter], list):
                                for f in filters[filter]:
                                    f.replace("%20", " ")
                                    recipes = recipes.filter(title__contains=f)
                            else:
                                f = filters[filter].replace("%20", " ")
                                recipes = recipes.filter(title__contains=f)
        filtered_recipes = []
        for recipe in recipes:
            filtered_recipes.append(recipe.toJson())
        return {'recipes': filtered_recipes}
    #    except:
    #       return {'error': 'Query not valid.'}


def get_rating_by_id(recipe_id):
    try:
        recipe = Recipe.objects.get(id=recipe_id)  # Supongo que el campo para el ID de la receta se llama 'id'
        return {'rating_amount': recipe.rating_amount,
                'rating_average': recipe.rating_average}  # Supongo que tienes un método toJson() en tu modelo Recipe
        # para convertirlo en un diccionario.
    except Recipe.DoesNotExist:
        return {'error': 'Recipe not found'}


def calculateCalories(ingredients):
    total_calories = 0
    for i in ingredients:
        if CALORIES[i]:
            total_calories += CALORIES[i]
    return total_calories


def get_recipe_by_id(recipe_id):
    try:
        recipe = Recipe.objects.get(id=recipe_id)  # Supongo que el campo para el ID de la receta se llama 'id'
        return {'recipe': recipe.toJson()}
    except Recipe.DoesNotExist:
        return {'error': 'Recipe not found'}


def add_comment_logic(request):
    body = json.loads(request.body.decode('utf-8'))
    user_id = body.get("user_id")
    recipe_id = body.get("recipe_id")
    comment = body.get("comment")

    recipe = Recipe.objects.get(id=recipe_id)
    # Convertir las claves a cadenas
    str_recipe_id = str(user_id)

    if recipe is None:
        return {'error': 'Recipe not found.'}
    if user_id in recipe.comments_list:
        recipe.comments_list[user_id] = comment
        recipe.save()
        return {'message': 'Comment updated.',
                'comments_list': recipe.comments_list,
                'comments_amount': recipe.comments_amount}
    else:
        recipe.comments_list[user_id] = comment
        recipe.comments_amount += 1
        recipe.save()
        return {'message': 'Comment updated.',
                'comments_list': recipe.comments_list,
                'comments_amount': recipe.comments_amount}


CALORIES = {
    "Apple": 52,
    "Banana": 89,
    "Blackberry": 43,
    "Blueberries": 32,
    "Cantaloupe": 34,
    "Cherry": 50,
    "Coconut": 354,
    "Custard Apple": 101,
    "Date": 282,
    "Dried Date": 282,
    "Dried Figs": 249,
    "Figs": 74,
    "Grape": 69,
    "Grapefruit": 32,
    "Gooseberry": 44,
    "Kiwi": 61,
    "Lemon": 29,
    "Loquats": 47,
    "Mango": 60,
    "Nectarine": 44,
    "Orange": 43,
    "Orange Juice": 43,
    "Papaya": 43,
    "Pear": 57,
    "Pineapple": 50,
    "Canned Pineapple": 53,
    "Persimmon": 81,
    "Pomegranate": 83,
    "Plum": 46,
    "Prune": 240,
    "Raisin": 299,
    "Raspberry": 52,
    "Strawberries": 32,
    "Tangerine": 53,
    "Watermelon": 30,
    "Artichokes": 47,
    "Arugula": 25,
    "Asparagus": 20,
    "Beetroot": 43,
    "Bell Pepper": 31,
    "Black Olives": 115,
    "Boiled Potatoes": 87,
    "Brussels Sprouts": 43,
    "Cabbage": 25,
    "Canned Asparagus": 20,
    "Canned Crushed Tomatoes": 32,
    "Carrot": 41,
    "Cauliflower": 25,
    "Celery": 16,
    "Cucumber": 15,
    "Eggplant": 25,
    "Endive": 17,
    "Escarole": 17,
    "Fennel": 31,
    "Frozen Spinach": 43,
    "Garlic": 149,
    "Green Beans": 31,
    "Green Onion": 31,
    "Lettuce": 5,
    "Leeks": 31,
    "Mushrooms and other fungi": 38,
    "Onion": 40,
    "Parsley": 36,
    "Pumpkin": 26,
    "Radishes": 16,
    "Soybean Sprouts": 80,
    "Spinach": 43,
    "Tomato Juice": 17,
    "Tomatoes": 18,
    "Truffle": 29,
    "Turnips": 28,
    "Watercress": 11,
    "Zucchini": 17,
    "Almonds": 576,
    "Hazelnuts": 629,
    "Chestnuts": 131,
    "Peanuts": 567,
    "Walnuts": 654,
    "Pine Nuts": 673,
    "Pistachios": 560,
    "Creme Caramel": 139,
    "Vanilla Flan": 151,
    "Dairy Ice Cream": 207,
    "Sweetened Condensed Milk": 321,
    "Unsweetened Condensed Milk": 134,
    "Goat's Milk": 69,
    "Sheep's Milk": 108,
    "Skimmed Milk": 35,
    "Skimmed Milk Powder": 353,
    "Whole Milk Powder": 496,
    "Whole Milk": 61,
    "Semi-Skimmed Milk": 47,
    "Mousse": 186,
    "Cream": 296,
    "Fat-Free Cottage Cheese": 73,
    "Brie Cheese": 334,
    "Camembert Cheese": 299,
    "Cheddar Cheese": 403,
    "Cream Cheese": 342,
    "Edam Cheese": 357,
    "Emmental Cheese": 379,
    "Spreadable Processed Cheese": 319,
    "Gruyere Cheese": 413,
    "Manchego Cheese": 373,
    "Mozzarella Cheese": 280,
    "Parmesan Cheese": 431,
    "Ricotta Cheese": 174,
    "Roquefort Cheese": 369,
    "Cottage Cheese": 98,
    "Fat-Free Yogurt": 48,
    "Fat-Free Fruit Yogurt": 54,
    "Yogurt Enriched with Cream": 101,
    "Natural Yogurt": 61,
    "Natural Yogurt with Fruit": 74,
    "Bacon (Pancetta)": 417,
    "Boiled Sausage": 212,
    "Burger": 250,
    "Chorizo": 455,
    "Chicken": 148,
    "Chicken Breast": 165,
    "Chicken Leg": 185,
    "Chicken Liver": 197,
    "Cured Ham": 337,
    "Cured Loin": 199,
    "Deer": 158,
    "Duck": 364,
    "Foie Gras": 464,
    "Frankfurter Sausage": 299,
    "Ham": 165,
    "Kid Goat": 128,
    "Lamb Liver": 130,
    "Lamb Ribs": 104,
    "Leg of Lamb": 105,
    "Mortadella": 311,
    "Partridge": 151,
    "Pheasant": 119,
    "Pig's Feet": 205,
    "Pork Chop": 143,
    "Pork Cracklings": 544,
    "Pork Liver": 143,
    "Pork Loin": 143,
    "Quail and Partridge": 123,
    "Rabbit and Hare": 173,
    "Roast Beef": 250,
    "Salami": 336,
    "Salchichón Sausage": 366,
    "Suckling Lamb": 171,
    "Turkey Breast": 135,
    "Turkey Leg": 135,
    "Veal": 105,
    "Veal Brains": 148,
    "Veal Chop": 105,
    "Veal Kidney": 105,
    "Veal Liver": 119,
    "Veal Sirloin": 119,
    "Veal Tongue": 150,
    "Wild Boar": 144,
    "York Ham": 114,
    "Anchovies": 210,
    "Anguillas": 150,
    "Clams": 142,
    "Canned Tuna in Vegetable Oil": 192,
    "Canned Tuna in Water": 116,
    "Fresh Tuna": 144,
    "Fresh Cod": 74,
    "Dried Cod": 210,
    "Sea Bream": 115,
    "Mackerel": 305,
    "Squid": 82,
    "Crab": 90,
    "Caviar": 264,
    "Conger Eel": 76,
    "Dorado": 104,
    "Hake": 88,
    "John Dory": 96,
    "Shrimp": 97,
    "Lobster": 96,
    "Prawn": 71,
    "Sole": 84,
    "Sea Bass": 97,
    "Pike": 105,
    "Mussels": 86,
    "Four-Spot Megrim": 80,
    "Grouper": 105,
    "Oysters": 68,
    "Silverside": 97,
    "Swordfish": 158,
    "Octopus": 82,
    "Turbot": 110,
    "Salmon": 206,
    "Smoked Salmon": 104,
    "Red Mullet": 105,
    "Canned Sardines in Vegetable Oil": 208,
    "Sardines": 135,
    "Trout": 119,
    "Caramel": 325,
    "Cocoa Powder with Instant Sugar": 393,
    "Candies": 394,
    "Milk Chocolate": 545,
    "Dark Chocolate": 552,
    "Chocolate Hazelnut Spread": 546,
    "Quince Jelly": 295,
    "Water Ice Cream": 112,
    "Jam with Sugar": 282,
    "Jam without Sugar": 152,
    "Sugar": 387,
    "Barley": 352,
    "Breakfast Cereals with Honey": 376,
    "Cereals with Chocolate": 375,
    "Corn Flakes": 372,
    "Cornmeal": 350,
    "White Rice": 365,
    "Whole Rice": 360,
    "Oats": 389,
    "Polenta": 70,
    "Rye": 333,
    "Semen Semolina": 332,
    "Integral Wheat Bread": 248,
    "Refined Wheat Flour": 363,
    "Whole Wheat Flour": 340,
    "Rye Bread": 260,
    "White Wheat Bread": 247,
    "Whole Wheat Bread": 247,
    "White Wheat Sliced Bread": 247,
    "Whole Wheat Sliced Bread": 247,
    "Egg Pasta": 360,
    "Wheat Pasta": 356,
    "Honey": 304,
    "Cassava": 160,
    "Chickpeas": 164,
    "Kidney Beans": 127,
    "Lentils": 116,
    "Egg White": 52,
    "Egg Yolk": 322,
    "Hard-Boiled Egg": 155,
    "Whole Egg": 143,
    "Apple Cake": 332,
    "Apple Pie": 237,
    "Butter Danish-Style Cookies": 466,
    "Bizcocho (Sponge Cake)": 355,
    "Cheesecake": 321,
    "Chocolate Croissant": 440,
    "Croissant": 406,
    "Croissant, Donut": 419,
    "Chocolate Cookies": 495,
    "Magdalenas": 371,
    "Puff Pastry Dough (Baked)": 558,
    "Savory Crackers": 492,
    "Anise": 337,
    "Bitter Vermouth": 157,
    "Brandy": 231,
    "Cacao Powder for Chocolate": 284,
    "Champagne (Demi-Sec)": 90,
    "Champagne (Sweet)": 80,
    "Champagne (Dry)": 66,
    "Almond Milk": 13,
    "Coffee": 2,
    "Cola Drinks": 41,
    "Daiquiri": 125,
    "Gin & Tonic": 98,
    "Gin": 263,
    "Lactose-Free Cocoa Milkshake": 82,
    "Cane Liquor": 268,
    "Pina Colada": 142,
    "Pisco": 250,
    "Sweet Cider": 61,
    "Dry Cider": 46,
    "Pineapple Liqueur": 224,
    "Port Wine": 169,
    "Rum": 231,
    "Scotch Whisky": 250,
    "Sparkling Water": 0,
    "Sweet Sherry": 124,
    "Table Wine": 69,
    "Tea": 1,
    "Vodka": 231,
    "Water": 0,
    "Whiskey": 250,
    "Butter": 717,
    "Lard": 902,
    "Olive Oil": 884,
    "Sunflower Oil": 884,
    "Vegetable Margarine": 700,
    "Bechamel": 124,
    "Canned Tomato Sauce": 20,
    "Concentrated Broths": 16,
    "Ketchup": 102,
    "Light Mayonnaise": 262,
    "Mayonnaise": 302,
    "Mustard": 66,
    "Soy Sauce": 60,
    "Sofrito": 101,
    "Vinegars": 19
}
