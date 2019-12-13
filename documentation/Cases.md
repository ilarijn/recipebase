## Use cases and related queries



#### Recipes

User (with Account.id 1) creates a recipe (with Recipe.id 3).

- Insert new recipe into table Recipe.
```sql
INSERT INTO Recipe (date_created, name, instructions, servings, account_id, account_name) VALUES (CURRENT_TIMESTAMP, 'New recipe', 'Instructions', 2, 1, 'User Name');
```

- If recipe uses ingredients not already in the database, insert each new ingredient into table Ingredient.

```sql
INSERT INTO Ingredient (name, category, unit, kcal, account_id) VALUES ('New ingredient', NULL, 'g', NULL, 1)
```

- For each ingredient used in recipe, insert it into table RecipeIngredient.
```sql
INSERT INTO Recipe_Ingredient (recipe_id, ingredient_id, amount, unit) VALUES (3, 1, 100, g);
```


User edits a recipe.

- Update name, instructions and servings.

```sql
UPDATE Recipe SET name='Edited name', instructions='Edited instructions', servings=3 WHERE recipe.id = 3;
```

- Delete from table RecipeIngredient any ingredients removed from the recipe during the edit.

```sql
DELETE FROM Recipe_Ingredient WHERE recipe_ingredient.id = 2;
```

- Add any new ingredients to table Ingredient. Statement is identical to that used during recipe creation.


User deletes a recipe (with Recipe.id 2).

- First delete each related ingredient from table RecipeIngredient, then delete row from Recipe.

```sql
DELETE FROM Recipe_Ingredient WHERE recipe_ingredient.recipe_id = 2;
```

```sql
DELETE FROM Recipe WHERE recipe.id = ?
```

User searches for recipes in the database by name, ingredient or ingredient category with search term `:term`. User gets search results sorted by number of matches in a single recipe where applicable.

```sql
SELECT Recipe.id, Recipe.name, Recipe.account_id, Recipe.account_name FROM Recipe 
WHERE (LOWER(Recipe.name) LIKE LOWER(:term));
```

```sql
SELECT Recipe.id, Recipe.name, Recipe.account_id, Recipe.account_name, Ingredient.name as ingredient FROM Recipe
LEFT JOIN Recipe_Ingredient ON Recipe_Ingredient.recipe_id = Recipe.id 
LEFT JOIN Ingredient ON Ingredient.id = Recipe_Ingredient.ingredient_id LEFT JOIN 
(SELECT Recipe.name, Recipe.id as id, COUNT(Recipe.id) as count FROM Recipe
LEFT JOIN Recipe_Ingredient ON Recipe_Ingredient.recipe_id = Recipe.id
LEFT JOIN Ingredient ON Ingredient.id = Recipe_Ingredient.ingredient_id
WHERE (LOWER(Ingredient.name) LIKE LOWER(:term)) GROUP BY Recipe.id) as matches ON matches.id = Recipe.id
WHERE (LOWER(Ingredient.name) LIKE LOWER(:term)) ORDER BY matches.count DESC;
```

```sql
SELECT Recipe.id, Recipe.name, Recipe.account_id, Recipe.account_name, Ingredient.category as category FROM Recipe 
LEFT JOIN Recipe_Ingredient ON Recipe_Ingredient.recipe_id = Recipe.id 
LEFT JOIN Ingredient ON Ingredient.id = Recipe_Ingredient.ingredient_id LEFT JOIN 
(SELECT Recipe.name, Recipe.id as id, COUNT(Recipe.id) as count FROM Recipe 
LEFT JOIN Recipe_Ingredient ON Recipe_Ingredient.recipe_id = Recipe.id 
LEFT JOIN Ingredient ON Ingredient.id = Recipe_Ingredient.ingredient_id 
WHERE (LOWER(Ingredient.category) LIKE LOWER(:term)) GROUP BY Recipe.id ) as matches ON matches.id = Recipe.id 
WHERE (LOWER(Ingredient.category) LIKE LOWER(:term)) ORDER BY matches.count DESC;
```

User lists recipes they have created themselves.

```sql
SELECT * FROM Recipe WHERE Recipe.account_id = 1;
```


#### Ingredients

User manually adds an ingredient to the database.

```sql
INSERT INTO Ingredient (name, category, unit, kcal, account_id) VALUES ('Strawberry', 'fruit', 'g', 0.3, 1);
```

User edits an ingredient.
```sql
UPDATE Ingredient SET category='berry', unit='kg', kcal=300 WHERE ingredient.id = 4;
```

User deletes an ingredient.
```sql
DELETE FROM Ingredient WHERE ingredient.id = 4;
```

User browses ingredients and only ingredients created by current user are displayed.

```sql
SELECT * FROM Ingredient WHERE Ingredient.account_id = 1;
```

#### Authorization

User signs up for an account.
```sql
INSERT INTO Account (date_created, date_modified, name, username, password) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'new user', 'newuser', 'asdf1234');
```

User logs in.
```sql
SELECT account.id AS account_id, account.date_created AS account_date_created, account.date_modified AS account_date_modified, account.name AS account_name, account.username AS account_username, account.password AS account_password 
FROM Account WHERE account.username = 'newuser' AND account.password = 'asdf1234';
```

User 'newuser' is deleted from database.
```sql
DELETE FROM Account WHERE account.username = 'newuser';
```






