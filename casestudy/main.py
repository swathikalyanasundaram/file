import pyodbc
from module import MainMenu

if __name__ == "__main__":
    # Database connection details
    server_name = "MSI\\SQLEXPRESS"
    database_name = "ordermanagement"
    conn_str = (
        f"Driver={{SQL Server}};"
        f"Server={server_name};"
        f"Database={database_name};"
        f"Trusted_Connection=yes;"
    )

    # Connect to the database
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Call the main menu
    MainMenu.main_menu(cursor, conn)

    # Close the database connection
    conn.close()
