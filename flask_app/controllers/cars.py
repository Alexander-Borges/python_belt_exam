from flask import Flask, render_template, session, redirect, request
from flask_app import app
from flask_app.models.user import User 
from flask_app.models.car import Car 
from flask import flash 
from flask_bcrypt import Bcrypt
from datetime import datetime
bcrypt = Bcrypt(app)


########## GET ROUTES #############

@app.route("/cars/dashboard")
def cars_dashboard():
    if "user_id" not in session:
        flash("You must be logged in to access the dashboard.")
        return redirect("/")

    # TO DO:
    # Get all the cars and send to the template
    #user = User.get_by_id(session["user_id"])
    user = User.get_by_id({"id": session["user_id"]})  # Retrieve the user object
    cars = Car.get_all()  # Make sure you have a get_all() method in your Car model
    return render_template("dashboard.html", user=user, cars=cars)

#Render Page Details Page for One Car
@app.route("/cars/<int:car_id>")
def car_detail(car_id):
    print("In details: ", car_id) 
    user = User.get_by_id({"id": session["user_id"]})
    # Need to get that car from the database
    car = Car.get_by_id(car_id)
    #print(car.user)
    # Pass the car into the template
    return render_template("car_detail.html", car=car, user = user)

# Render Page with Create Form
@app.route("/cars/new")
def create_page():
    print("In create route.")
    user = User.get_by_id({"id": session["user_id"]})
    return render_template("create_car.html", user = user)

# Render Page with Edit Form
@app.route("/cars/edit/<int:car_id>", methods = ["GET", "POST"])
def edit_page(car_id):
    print("In edit page: ", car_id)
    if request.method == "POST":
        is_valid = Car.is_valid(request.form)
        #return redirect("/cars")

        #if the form data is good THEN save and go to the dashboard
        if is_valid:
            Car.update(request.form)
            return redirect("/cars/dashboard")
    car = Car.get_by_id(car_id)
    # Need to get that car from the database
    # Pass the car into the template
    return render_template("edit_car.html", car = car)


# GET Action Routes:
# Delete Route (GET request)
@app.route("/cars/delete/<int:car_id>")
def delete_car(car_id):
    print("In delete page: ", car_id)
    # Call delete method
    Car.delete_by_id(car_id)
    return redirect("/cars/dashboard")

######## POST Routes ########


# CREATE (Process Form)
@app.route("/cars", methods=["POST"])
def create_car():
    print("In the create process POST route: ", request.form)
    # Before we save
    # If the form data is good THEN save and go to the dashboard
    is_valid = Car.is_valid(request.form)
    
    print(is_valid)
    car_data = {
        "price": request.form["price"],
        "model": request.form["model"],
        "make": request.form["make"],
        "year": request.form["year"],
        "description": request.form["description"],
        "user_id": request.form["user_id"]
    }

    print("Car Data:", car_data)

    #try:

    #   flash("Car created successfully!", "success")
    #except Exception as e:
    #    flash("Error creating car: " + str(e), "danger")
    if is_valid:
        Car.save(request.form)
        return redirect("/cars/dashboard")
    #else: -- redirect to the new page to show errors to the user
    return redirect("cars/new")

# Update (Process Form)
"""@app.route("/cars/update", methods=["POST"])
def update_cars():
    print("In update POST route: ", request.form)
    is_valid = Car.is_valid(request.form)
    #return redirect("/cars")

    #if the form data is good THEN save and go to the dashboard
    if is_valid:
        Car.update(request.form)
        return redirect("/cars/dashboard")
    return redirect(f"cars/edit/{request.form['id']}")"""