## Future features

In its current state, the application does what it was supposed to from the start: allow an user browse recipes and create new ones using ingredients in the database that can be sorted and assigned informative properties by the user. Still, there are many ways in which the application might be improved. 

#### Tags
The next important feature for this application would be the ability to assign tags, e.g. 'vegetarian', to a recipe and then allow users to search by tags. Currently ingredients have categories, which work as a sort of a tag, allowing a user to search for 'vegetable' and then get recipes using ingredients of this category provided that such a category value has been entered. 

Originally the idea behind ingredient categories was to also provide a way to assign tags: for example a 'vegetarian' tag could be assigned to a recipe with no animal products. However, this would require that ingredient category is mandatory, which is not very user-friendly since category is a property defined by the user. The category property could be left as is to provide sorting and search options for users or just be removed and replaced by a recipe tag feature.

#### Unit conversions
Adding automatic unit conversions for the most common cases would make calculating serving kcal values easier. Currently the application expects that the user uses an ingredient's default unit (as listed in the db table Ingredient) in a recipe in order for this ingredient to be included in calculating a kcal value per serving. Adding conversions for cases such as tbsp=15ml, kg=1000g, cup=250ml would make this feature much more flexible. 

#### Ingredient name parsing
When adding new ingredients to the database after recipe creation, the application currently checks for existing ingredients based on name. The names are compared in lowercase with any extra whitespace removed, but e.g. singular and plural forms of a nouns are two different names, which results in unnecessary database entries simply because a user wants to write '1 onion' instead of '1 onions'. This is especially true for Finnish language entries where different cases of a noun produce even more extra entries simply due to language conventions. Not the easiest problem to start solving, but an interesting one.