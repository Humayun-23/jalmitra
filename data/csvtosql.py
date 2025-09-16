import psycopg2
import csv

# --- DATABASE CONNECTION DETAILS ---
# Replace these with your actual PostgreSQL database credentials
DB_NAME = "rainwater"
DB_USER = "humayun"
DB_PASS = "testpassword"
DB_HOST = "localhost"
DB_PORT = "5432"

# --- FILE AND TABLE DETAILS ---
CSV_FILE_PATH = 'TNprepostgwl.csv'
TABLE_NAME = 'gwlevel'

# --- SQL CREATE TABLE STATEMENT (for reference) ---
# Before running this script, ensure your 'gwlevel' table exists in the database.
# You can use a statement like this to create it:
#
# CREATE TABLE gwlevel (
#     id SERIAL PRIMARY KEY,
#     dtname VARCHAR(255) NOT NULL,
#     premonsoongwl NUMERIC(10, 2),
#     postmonsoongwl NUMERIC(10, 2),
#     gwl_fluctuation_meters NUMERIC(10, 2)
# );

def insert_gwl_data_to_postgres():
    """
    Connects to the PostgreSQL database and inserts groundwater level data
    from a CSV file into the 'gwlevel' table.
    """
    conn = None
    cursor = None
    
    try:
        # Establish a connection to the database
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT
        )
        print("Database connection established successfully.")
        
        cursor = conn.cursor()
        
        # Open the CSV file for reading
        with open(CSV_FILE_PATH, 'r') as f:
            reader = csv.reader(f)
            
            # Skip the header row so we don't insert it into the DB
            next(reader) 
            
            print(f"Starting to insert data from '{CSV_FILE_PATH}' into table '{TABLE_NAME}'...")
            
            # Iterate over each row in the CSV file
            for row in reader:
                # Prepare the SQL INSERT statement for the gwlevel table.
                # Using %s placeholders is the standard, secure way to pass data,
                # preventing SQL injection vulnerabilities.
                sql = (
                    f"INSERT INTO {TABLE_NAME} (dtname, premonsoongwl, postmonsoongwl, gwl_fluctuation_meters) "
                    "VALUES (%s, %s, %s, %s)"
                )
                
                # The row contains: [District, premonsoongwl, postmonsoongwl, gwl_fluctuation_meters]
                # We pass the entire row to the execute method.
                # psycopg2 handles the conversion of types.
                cursor.execute(sql, (row[0], row[1], row[2], row[3]))

        # Commit the transaction to make all the inserts permanent
        conn.commit()
        print("Data inserted successfully!")

    except FileNotFoundError:
        print(f"Error: The file '{CSV_FILE_PATH}' was not found.")
    except psycopg2.Error as e:
        # If any database error occurs, rollback the transaction
        if conn:
            conn.rollback()
        print(f"Database error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        
    finally:
        # Ensure the cursor and connection are always closed
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            print("Database connection closed.")

if __name__ == '__main__':
    insert_gwl_data_to_postgres()