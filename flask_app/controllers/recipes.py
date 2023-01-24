from flask_app import app, render_template, redirect, request, bcrypt, session, flash
from flask_app import app
from flask_app.models.recipe import Recipe
from flask_app.models.user import User

# TEST TO SEE IF DATA GOES TO SUCCESS ROUTE
@app.route('/recipes')
def success():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template ("recipes.html", recipes = Recipe.get_all())

@app.route('/recipes/new')
def new_recipe():
    return render_template ('new_recipe.html')

@app.route('/recipes/create', methods = ['POST'])
def create_recipe():
    print(request.form)
    
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')

    Recipe.save(request.form)
    return redirect ('/recipes')

# ! READ ONE
@app.route("/recipes/<int:id>")
def get_recipe(id):
    return render_template("show_recipe.html", recipe = Recipe.get_one({'id': id}))

# ! READ ONE WITH MANY
@app.route("/recipes/all_recipes/<int:id>")
def get_all_recipe(id):
    return render_template("all_recipes.html", user = Recipe.get_one_with_recipes({'id': id}))

# ! UPDATE
@app.route("/recipes/edit/<int:id>")
def recipe_edit(id):
    return render_template("edit_recipe.html", recipe = Recipe.get_one({'id': id}))

@app.route("/recipes/update", methods = ["POST"])
def recipe_update():
    print(request.form)
    
    if not Recipe.validate_recipe(request.form):
        return redirect(f"/recipes/edit/{request.form['id']}")

    Recipe.update(request.form)
    return redirect("/recipes")

# ! DELETE
@app.route("/recipes/delete/<int:id>")
def recipe_delete(id):
    Recipe.delete({'id': id})
    return redirect('/recipes')
