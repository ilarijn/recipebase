https://recipebase.herokuapp.com

#### recipebase
The aim is to create a database of ingredients and recipes. Users may create and store recipes using ingredients in the database and add missing ingredients to the database. Users may make recipes public to be viewed by anyone or keep them private. Recipes may be searched for using different parameters: by recipe name, recipe time, ingredient name, ingredient category or different combinations.
Tags for recipes might be added later for more search options.

[Preliminary database diagram](documentation/pre_diagram.png)

[User stories](documentation/user_stories.txt)


##### Current version
Authorized users can create, delete, view and edit recipes. A recipe has a name, instructions, creation timestamp and a list of associated ingredients. An ingredient is connected to a recipe via an association object that also stores the amount.

Ingredients existing in the database can be added to recipes via a jQuery autocomplete function. New ingredients are automatically added to the database at recipe creation, and they can also be added and viewed separately. At this time ingredient properties consist of a name, category, unit of measurement and a kcal per unit value.


##### Todo
- Link added ingredient to user: the idea is for a user to be able to maintain their own customizable collection of preferred ingredients, not provide a huge default selection
- Public/private toggle for recipes
- Appropriate login-required checks for actions
- Admin view for managing users etc.
- Do not lock empty fields as readonly when retrieving ingredients to enable updates

[Current database diagram](documentation/current_diagram.png)

