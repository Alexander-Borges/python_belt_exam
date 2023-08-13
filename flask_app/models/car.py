from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app.models import user
from flask_app.models import car
from datetime import datetime
import re

class Car:
    db = "cars"

    def __init__(self, car):
        self.id = car['id']
        self.price = car['price']
        self.model = car['model']
        self.make = car['make']
        self.year = car["year"]
        self.description = car['description']
        self.created_at = car['created_at']
        self.updated_at = car['updated_at']
        self.user = car['user_id']

    # GET CAR BY ID
    @classmethod
    def get_by_id(cls, car_id):

        # Get car data with user data who created it 
        query = """
                SELECT * FROM cars 
                JOIN users on cars.user_id = users.id
                WHERE cars.id = %(id)s;
                """
        data = {
            "id": car_id
        }
        car_dict = connectToMySQL(cls.db).query_db(query, data)[0]
        
        
        if not car_dict:
            return None  # car not found
        
        car_dict = car_dict  # Get the first result
        car_object = Car(car_dict)
        
        # Make a car object from data
        car_object = Car(car_dict)
        # Make a user object from data
        user_object = user.User({
            "id" : car_dict["users.id"],
            "first_name" : car_dict["first_name"],
            "last_name" :car_dict["last_name"],
            "email" : car_dict["email"],
            "password" : car_dict["password"],
            "created_at" : car_dict["users.created_at"],
            "updated_at": car_dict["users.updated_at"]
        })
        # Associate user with car
        car_object.user = user_object
        # Return car
        return car_object

    # GET ALL
    @classmethod
    def get_all(cls):

        # Get all cars, and the user info for the creators
        query = """
                SELECT * FROM cars
                JOIN users on cars.user_id = users.id;
                """
        results = connectToMySQL(cls.db).query_db(query)
        # Make a list to hold car objects to return
        print("Retrieved cars:", results)
        cars = []
        # Iterate thru the list of car dictionaries
        for car_dict in results:
            # convert data into a car object
            car_object = Car(car_dict)
            # convert joined user data into a user object
            user_object = user.User({
                "id" : car_dict["users.id"],
                "first_name" : car_dict["first_name"],
                "last_name" :car_dict["last_name"],
                "email" : car_dict["email"],
                "password" : car_dict["password"],
                "created_at" : car_dict["users.created_at"],
                "updated_at": car_dict["users.updated_at"]
            })
            # Associate user with car
            car_object.user = user_object
            # append to list
            cars.append(car_object)
        # Return the list of cars
        return cars


    # CREATE VALID CAR
    @classmethod
    def save(cls, car_data):
        # create a new dict to hold the modified data 
        new_car_data = {
            "price": car_data["price"],
            "model": car_data["model"],
            "make": car_data["make"],
            "year": car_data["year"],
            "description": car_data["description"],
            "user_id": car_data["user_id"],
            }
        # takes data dictionary from request.form 
        # validates data
        # Insert the car into the database
        print("Inserting the following data:")
        print(new_car_data)  # Add this line to print the data before insertion
    
        
        query = """
                INSERT INTO cars (price, make, model, year, description, user_id)
                VALUES (%(price)s, %(make)s, %(model)s, %(year)s, %(description)s, %(user_id)s);
                """
        connectToMySQL(cls.db).query_db(query, new_car_data)
        # return id? or False if the validation fails

    # DELETE CAR BY ID 
    @classmethod
    def delete_by_id(cls, car_id):
        query = """
                DELETE FROM cars
                WHERE id = %(id)s; 
                """
        data = {
            "id": car_id
        }
        connectToMySQL(cls.db).query_db(query, data)
        # Delete car using the id
        return

    # UPDATE CAR
    @classmethod
    def update(cls, car_data):
        query = """
                UPDATE cars
                SET price = %(price)s, make = %(make)s, model = %(model)s, year = %(year)s, description = %(description)s 
                WHERE id = %(id)s;
                """
        connectToMySQL(cls.db).query_db(query, car_data)
        
        return
        
        # takes data dictionary from request.form 
        # Updates car using the id in the format
        
        # Returns the new car as an object or False if the validation fails



    @staticmethod
    def is_valid(car_dict):

        # Set valid variable to TRUE
        valid = True
        # No fields blank
        if len(car_dict["price"]) == 0:
            valid = False
            flash("Price is required")
            
        if len(car_dict["model"]) == 0:
            valid = False 
            flash("Model Required")
        elif len(car_dict['model']) < 1:
            valid = False
            flash("Model must be at least 1 character.")

        if len(car_dict["make"]) == 0:
            valid = False
            flash("Make required.")
        elif len(car_dict['make']) < 1:
            valid = False
            flash("Make must be at least 1 character")

        if len(car_dict["year"]) == 0:
            valid = False 
            flash("Year Required")

        if len(car_dict["description"]) == 0:
            valid = False
            flash("Description Required")


        return valid