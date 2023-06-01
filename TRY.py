import mysql.connector

# Connect to the MySQL server
mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    passwd=""
)

# Create a cursor object
cursor = mydb.cursor()

#name of the database
database_name = "mydatabase1"

# Create the database if it doesn't exist
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")

# Use the database
cursor.execute(f"USE {database_name}")

# Select the newly created database
cursor.execute("USE mydatabase1")

# Create tables if they don't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        users_id INT PRIMARY KEY,
        first_name VARCHAR(255),
        last_name VARCHAR(255),
        email VARCHAR(255),
        password VARCHAR(10),
        city VARCHAR(20),
        zip_code VARCHAR(10)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS category (
        category_id INT PRIMARY KEY,
        category_name VARCHAR(255),
        description VARCHAR(255)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS business (
        business_id INT PRIMARY KEY,
        business_name VARCHAR(255),
        address VARCHAR(255),
        zip_code VARCHAR(10),
        phone VARCHAR(20),
        website VARCHAR(255),
        category_id INT,
        FOREIGN KEY (category_id) REFERENCES category(category_id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS review (
        review_id INT PRIMARY KEY,
        rating NUMERIC,
        review_text CHAR,
        business_id INT,
        users_id INT,
        FOREIGN KEY (business_id) REFERENCES business(business_id),
        FOREIGN KEY (users_id) REFERENCES users(users_id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS image (
        image_id INT PRIMARY KEY,
        url VARCHAR(255),
        business_id INT,
        FOREIGN KEY (business_id) REFERENCES business(business_id)
    )
""")


# Search for business details by business I
def search_business_details_by_id(business_id):
    sql = """
    SELECT b.business_id, b.business_name, b.address, b.zip_code, b.phone, b.website, b.category_id, c.category_name, r.rating, i.url
    FROM Business AS b
    JOIN Category AS c ON b.category_id = c.category_id
    LEFT JOIN Review AS r ON b.business_id = r.business_id
    LEFT JOIN Image AS i ON b.business_id = i.business_id
    WHERE b.business_id = %s
    """


    cursor.execute(sql, (business_id,))
    result = cursor.fetchone()

    if result:
        print("**************************************")
        print("Business ID:", result[0])
        print("Business Name:", result[1])
        print("Address:", result[2])
        print("Zip Code:", result[3])
        print("Phone:", result[4])
        print("Website:", result[5])
        print("Category:", result[7])
        print("Rating:", result[8])
        print("Image URL:", result[9])
        print("**************************************")

    else:
        print("**************************************")
        print("No business found with the specified ID.")


# Function to add a review for a business
def add_review(rating, review_text, business_id, users_id):
    # Check if the user is registered
    cursor.execute("SELECT * FROM users WHERE users_id = %s", (users_id,))
    users = cursor.fetchone()
    if users:
        # Generate a new review_id
        cursor.execute("SELECT MAX(review_id) FROM review")
        last_review_id = cursor.fetchone()[0]
        review_id = last_review_id + 1 if last_review_id else 1

        # Insert the review into the database
        query = "INSERT INTO review (review_id, rating, review_text, business_id, users_id) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (review_id, rating, review_text, business_id, users_id))
        mydb.commit()
        print("Review added successfully. Review ID:", review_id)

    else:
        print("Cannot add a review. Please register or log in to add a review.")



# Example usage
business_id = input("Enter the Business ID for Details : ")
search_business_details_by_id(business_id)


# Check if the user is registered to add a review
choice = input("Do you want to add a review? (y/n): ")
if choice.lower() == 'y':
    users_id = input("Enter your user ID: ")
    if not users_id:
        print("Cannot add a review. Please register to add a review.")
    else:
        rating = float(input("Enter the rating (1-5): "))
        review_text = input("Enter the review text: ")
        add_review(rating, review_text, business_id, users_id)
else:
    print("**************************************")
    print("Thank you for using the system")

# Close the database connection
mydb.close()

# Example usage
#business_id = input("Enter the Business ID for Details : ")
#search_business_details_by_id(business_id)
