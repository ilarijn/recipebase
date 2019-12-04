https://recipebase.herokuapp.com

Create a user at http://recipebase.herokuapp.com/auth/new or login as user1:user1 or user2:user2 to start testing.

***

#### recipebase
The aim is to create a database of ingredients and recipes. Users may create and store recipes using ingredients in the database and add missing ingredients to the database. Users may make recipes public to be viewed by anyone or keep them private. Recipes may be searched for using different parameters: by recipe name, recipe time, ingredient name, ingredient category or different combinations.
Tags for recipes might be added later for more search options.

[Preliminary database diagram](documentation/pre_diagram.png)

[User stories](documentation/user_stories.txt)


##### Current version
Authorized users can create, delete, view and edit recipes. Unauthorized users can view and search for recipes. Currently all recipes are visible to all. 

A recipe has a name, instructions, creation timestamp and a list of associated ingredients. An ingredient is connected to a recipe via an association object that also stores amount and unit of measurement used in recipe.

Ingredients in the database can be added to recipes via a jQuery autocomplete function. New ingredients are automatically added to the database at recipe creation, and they can also be added and viewed separately. Currently all ingredients are visible to all authorized users.

Kcal values for ingredients and time for recipes exist in the db but are not utilized yet.

[Current database diagram](documentation/current_diagram.png)

#### Todo
- Maybe not make ingredient names unique and make all ingredients user-specific 
- Recipe tags



