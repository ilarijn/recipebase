## Use cases and related queries


- User searches for recipes in the database by name, ingredient or ingredient category with search term `:term`. User gets search results sorted by number of matches in a single recipe where applicable.

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

- User lists recipes they have created themselves.

```sql
SELECT * FROM Recipe WHERE Recipe.account_id = [Account.id of current user];
```

- User browses ingredients and only ingredients created by current user are displayed.

```sql
SELECT * FROM Ingredient WHERE Ingredient.account_id = [Account.id of current user];
```

