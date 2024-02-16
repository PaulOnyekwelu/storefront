import psycopg2
from psycopg2 import sql
import sys
import os
import time

database_config = {
    "host": os.environ.get("POSTGRES_HOST"),
    "user": os.environ.get("POSTGRES_USER"),
    "password": os.environ.get("POSTGRES_PASSWORD"),
    "database": os.environ.get("POSTGRES_DB"),
    "port": os.environ.get("POSTGRES_PORT"),
}


def table_exists(cursor, table_name):
    """
    Check if a table exists in the database.
    """
    cursor.execute(
        """
        SELECT EXISTS (
            SELECT 1 
            FROM information_schema.tables 
            WHERE table_name = %s
        )
        """,
        (table_name,),
    )

    return cursor.fetchone()[0]


def table_has_data(cursor, table_name):
    """
    Check if a table contains data.
    """

    query = sql.SQL("SELECT EXISTS (SELECT 1 FROM {} LIMIT 1)").format(
        sql.Identifier(table_name)
    )
    cursor.execute(query)
    return cursor.fetchone()[0]


def should_add_data(cursor, table_name):
    """
    validate conditions before adding data to database
    """

    if not table_exists(cursor, table_name):
        return False

    if table_has_data(cursor, table_name):
        return False

    return True


def run_sql_file(sql_file_path, table_name):
    """
    Executes SQL statements from a file and inserts data into a PostgreSQL database.

    Args:
        sql_file_path (str): Path to the SQL file containing INSERT statements.
        database_config (dict): Dictionary containing PostgreSQL connection details.

    Returns:
        None
    """

    # Establish connection using database_config
    while True:
        try:
            with psycopg2.connect(**database_config) as conn:
                with conn.cursor() as cursor:
                    # Read SQL statements from file
                    with open(sql_file_path, "r") as sql_file:
                        sql_statements = sql_file.readlines()

                    if should_add_data(cursor, table_name):

                        # Execute each statement, handling data and errors
                        for statement in sql_statements:
                            if statement.strip():  # Ignore empty lines
                                try:
                                    cursor.execute(statement)
                                except psycopg2.Error as e:
                                    # Handle potential exceptions and reporting
                                    print(f"Error executing statement: {e}")

                        # Commit changes to the database
                        conn.commit()
                        print("Data insertion completed successfully.")
                        break

        except psycopg2.OperationalError as error:
            sys.stderr.write(f"Waiting for database to connect...")
            time.sleep(5)


if __name__ == "__main__":

    # mocking the customer table
    sql_file_path = "mock/seed.sql"
    run_sql_file(sql_file_path, "store_customer")
