from flask_app.config.mysqlconnection import connectToMySQL
from pprint import pprint
from flask_app import flash
from flask_app.models import user

DATABASE = 'login_reg'

class Recipe:
    
    def __init__(self, data) -> None:
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under_30 = data['under_30']
        self.user_id = data['user_id']
        self.number_served = data['number_served']
        self.first_name = data['first_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod
    def save(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, date_made, under_30, user_id, number_served) VALUES (%(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under_30)s, %(user_id)s, %(number_served)s);"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    # ! READ ALL
    # Now we use class methods to query our database
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes LEFT JOIN users ON users.id = recipes.user_id;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(DATABASE).query_db(query)
        pprint(results)
        # Create an empty list to append our instances of friends
        recipes = []
        # Iterate over the db results and create instances of friends with cls.
        for recipe in results:
            recipes.append(cls(recipe))
        return recipes

    # ! READ ONE
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM recipes JOIN users ON users.id = recipes.user_id WHERE recipes.id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        pprint(result[0])
        recipe = Recipe(result[0])
        print(recipe)
        return recipe

    # ! READ ONE WITH MANY
    @classmethod
    def get_one_with_recipes(cls, data):
        query = "SELECT * FROM recipes JOIN users ON users.id = recipes.user_id WHERE users.id = %(id)s"

        results = connectToMySQL(DATABASE).query_db(query, data)
        pprint(results)
        user = user.User(results[0])
        print(user.recipes)

        for item in results:
            pprint(item)
            temp_recipe = {
                'id' : item['recipes.id'],
                'name' : item['name'],
                'description' : item['description'],
                'instructions' : item['instructions'],
                'date_made' : item['date_made'],
                'under_30' : item['under_30'],
                'user_id' : item['user_id'],
                'number_served' : item['number_served'],
                'first_name' : item['first_name'],
                'created_at' : item['ninjas.created_at'],
                'updated_at' : item['ninjas.updated_at']
            }
            user.recipes.append(Recipe(temp_recipe))
        print(user.recipes)
        return user

    # ! UPDATE
    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_made = %(date_made)s, under_30 = %(under_30)s, number_served = %(number_served)s WHERE recipes.id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    # ! DELETE
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    # ! Validation
    @staticmethod
    def validate_recipe(recipe:dict) -> bool:
        is_valid = True
        if len(recipe['name']) < 3:
            flash("Name must be three chars")
            is_valid = False
        if len(recipe['description']) < 3:
            flash("Name must be three chars")
            is_valid = False
        if len(recipe['instructions']) < 3:
            flash("Name must be three chars")
            is_valid = False
        if recipe['date_made'] == '':
            flash("Pick a date for when recipe was made.")
            is_valid = False
        if not 'under_30' in recipe:
            flash("Must select option for under 30 min.")
            is_valid = False
        if int(recipe['number_served']) <= 0:
            flash("Recipe has to serve at least one person.")
            is_valid = False
        return is_valid
            