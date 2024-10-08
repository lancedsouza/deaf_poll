from flask import Flask, request, redirect, render_template
import mysql.connector

app = Flask(__name__, template_folder='deaf_poll/templates')

# MySQL database connection details
db_host = "localhost"  # or your actual host
db_user = "poll_user"
db_password = "lancedes@123"  # replace with your actual password
db_name = "DEAF_POLL"

# Connect to MySQL
def get_db_connection():
    return mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )

# Route to render the form
@app.route('/')
def index():
    return render_template('poll_form.html')  # ensure this points to your HTML file

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    gender = request.form['gender']
    age = request.form['age']
    brand = request.form['brand']
    source = request.form['source']
    type_of_aid = request.form['type']
    price = request.form['price']
    phone_num = request.form['phone_num']
    email = request.form['email']

    # If "Other" brand is selected, capture the specified brand
    if brand == 'other':
        brand = request.form.get('other_brand', '')

    # Insert data into the database
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()

        cursor.execute("""
            INSERT INTO poll_responses (gender, age, brand, source, type_of_aid, price, phone_num, email)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (gender, age, brand, source, type_of_aid, price, phone_num, email))

        cnx.commit()
        cursor.close()
        cnx.close()
        return redirect('/')  # Redirect to a success page or back to the form
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "Error occurred while submitting the form"

if __name__ == '__main__':
    app.run(debug=True)
