# User Management in python using Flask framework and MySQL Database
from flask import Flask, render_template, url_for, request, redirect, flash
from flask_mysqldb import MySQL

app = Flask(__name__)  # This takes the filename as a parameter

# MySQL Connection
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "Enter your password"
app.config["MYSQL_DB"] = "crud"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)

# Loading Home Page
@app.route("/")
def home():
    cursor = mysql.connection.cursor()
    # SELECT Query
    query = "SELECT * FROM users"
    cursor.execute(query)
    result = cursor.fetchall()
    return render_template("home.html", data = result)

# Loading Add Page
@app.route("/addPage", methods=["GET", "POST"])
# Add User Details
def add():
    if request.method == "POST":
    
        # Getting input from the user
        name = request.form["name"]
        age = request.form["age"]
        city = request.form["city"]
        
        cursor = mysql.connection.cursor()
        # INSERT Query
        query = "INSERT INTO users (NAME, AGE, CITY) VALUE (%s, %s, %s)"
        cursor.execute(query, (name, age, city))
        mysql.connection.commit()
        cursor.close()
        flash("Added Successfully") 
        return redirect(url_for("home"))
    return render_template("addPage.html")

# Loading Edit Page
@app.route("/editPage/<string:id>", methods=["GET", "POST"])
# Edit User Details
def edit(id):
    if request.method == "POST":
    
        # Getting input from user
        name = request.form["name"]
        age = request.form["age"]
        city = request.form["city"]
        
        cursor = mysql.connection.cursor()
        # UPDATE Query
        query = "UPDATE users SET  NAME = %s, AGE = %s, CITY = %s WHERE ID = %s"
        cursor.execute(query, (name, age, city, id))
        mysql.connection.commit()
        cursor.close()
        flash("Updated Successfully")
        return redirect(url_for("home"))

    cursor = mysql.connection.cursor()
    # SELECT Query
    query = "SELECT * FROM users WHERE ID = %s"
    cursor.execute(query, [id])
    result = cursor.fetchone()
    return render_template("editPage.html", data = result)

# Loading Delete Page
@app.route("/deletePage/<string:id>", methods=["GET", "POST"])
# Delete User Details
def delete(id):
    cursor = mysql.connection.cursor()
    # DELETE Query
    query = "DELETE FROM users WHERE ID = %s"
    cursor.execute(query, [id])
    mysql.connection.commit()
    cursor.close()
    flash("Deleted Successfully")
    return redirect(url_for("home"))
    
if (__name__ == "__main__"):
    app.secret_key = "thiskeyissecret"
    app.run(debug=True)