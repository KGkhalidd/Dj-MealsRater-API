# Dj-MealsRater-API
The project is about an interface for users to rate different meals. It includes three main components: Users, Meals, and Ratings.



1. Users: The User model is Django's built-in user model. It's used to manage users in your application. The UserSerializer is used to validate user data and transform it into a format that can be easily rendered into JSON, XML, or other content types. It includes fields for the user's id, username, and password. The password field is write-only and required, which means it will be used for write operations but won't be included in serialized representations of the object.



2. Meals: The Meal model represents meals that users can rate. The MealSerializer is used to validate meal data and transform it into a format that can be easily rendered into JSON, XML, or other content types. It includes fields for the meal's id, title, description, number of ratings, and average rating.



3. Ratings: The Rating model represents ratings that users have given to meals. The RatingSerializer is used to validate rating data and transform it into a format that can be easily rendered into JSON, XML, or other content types. It includes fields for the rating's id, the number of stars given, the user who gave the rating, and the meal that was rated.



In the MealViewSet, there's a custom action meal_rater that allows authenticated users to rate a meal. This action checks if the 'stars' field is in the request data, retrieves the meal and user, and then either updates an existing rating or creates a new one. If the rating is successfully updated or created, it returns a response with a message and the serialized data of the rating.



The project follows best practices for Django and Django REST Framework, including the use of serializers for data validation and transformation, viewsets for handling HTTP requests, and the Django ORM for database operations. It provides a robust API for managing users, meals, and ratings, and includes features for creating users and handling user authentication.
