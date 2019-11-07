https://recipebase.herokuapp.com

#### recipebase
The aim is to create a database of ingredients and recipes. Users may create and store recipes using ingredients in the database and add missing ingredients to the database. Users may make recipes public to be viewed by anyone or keep them private. Recipes may be searched for using different parameters: by recipe name, recipe time, ingredient name, ingredient category or different combinations.
Tags for both ingredients and recipes will maybe be added later for more search options.

[Preliminary database diagram](documentation/pre_diagram.png)

[User stories](documentation/user_stories.txt)


##### Current version
Currently a user can create, delete and view recipes. A recipe has a name, instructions, creation timestamp and a list of associated ingredients. An ingredient is connected to a recipe by an association object that also stores the amount of the ingredient.
Names and instructions of existing recipes can be edited. Ingredients can be added and viewed.

[Current database diagram](documentation/current_diagram.png)



##### Things to fix:
recipes/views.py:
- Find better way to add and clear ingredient selections when creating and editing and editing. Now two dicts outside method scope are used, which is problematic when using separate methods for both creating new recipes and editing existing ones.
- Clean copy/paste code and combine methods where possible, especially for creating and editing recipes.