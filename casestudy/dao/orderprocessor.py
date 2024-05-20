import pyodbc
from exception import UserNotFoundException, OrderNotFoundException
from IOrderManagementRepository import IOrderManagementRepository


class OrderProcessor(IOrderManagementRepository):
    def __init__(self, connection_string):
        self.conn = pyodbc.connect(connection_string)

    def createOrder(self, user_data, products_data):
        try:
            cursor = self.conn.cursor()

            # Check if user exists in the database
            cursor.execute("SELECT * FROM [User] WHERE userId=?", (user_data['userId'],))
            if cursor.fetchone() is None:
                # If user doesn't exist, raise UserNotFoundException
                raise UserNotFoundException("User not found in the database")

            # Create the order and store it in the database
            # Example code - You need to replace this with your actual database interaction logic
            cursor.execute("INSERT INTO Orders (userId, productId) VALUES (?, ?)", (user_data['userId'], products_data[0]['productId']))

            self.conn.commit()
            print("Order created successfully.")

        except Exception as e:
            self.conn.rollback()
            print("Error creating order:", str(e))

    def cancelOrder(self, user_id, order_id):
        try:
            cursor = self.conn.cursor()

            # Check if the order with the given user_id and order_id exists in the database
            cursor.execute("SELECT * FROM Orders WHERE userId=? AND orderId=?", (user_id, order_id))
            if cursor.fetchone() is None:
                # If order doesn't exist, raise OrderNotFoundException
                raise OrderNotFoundException("Order not found in the database")

            # Cancel the order in the database
            # Example code - You need to replace this with your actual database interaction logic
            cursor.execute("DELETE FROM Orders WHERE userId=? AND orderId=?", (user_id, order_id))

            self.conn.commit()
            print("Order cancelled successfully.")

        except Exception as e:
            self.conn.rollback()
            print("Error cancelling order:", str(e))

    def createProduct(self, user_data, product_data):
        try:
            cursor = self.conn.cursor()

            # Check if the user is an admin (role == "Admin")
            if user_data['role'] != "Admin":
                print("Only admin users can create products.")
                return

            # Create the product and store it in the database
            # Example code - You need to replace this with your actual database interaction logic
            cursor.execute("INSERT INTO Product (productId, productName, description, price, quantityInStock, type, brand, warrantyPeriod) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                           (product_data['productId'], product_data['productName'], product_data['description'], product_data['price'], product_data['quantityInStock'], product_data['type'], product_data['brand'], product_data['warrantyPeriod']))

            self.conn.commit()
            print("Product created successfully.")

        except Exception as e:
            self.conn.rollback()
            print("Error creating product:", str(e))

    def createUser(self, user_data):
        try:
            cursor = self.conn.cursor()

            # Create the user and store it in the database
            # Example code - You need to replace this with your actual database interaction logic
            cursor.execute("INSERT INTO [User] (userId, username, password, role) VALUES (?, ?, ?, ?)",
                           (user_data['userId'], user_data['username'], user_data['password'], user_data['role']))

            self.conn.commit()
            print("User created successfully.")

        except Exception as e:
            self.conn.rollback()
            print("Error creating user:", str(e))

    def getAllProducts(self):
        try:
            cursor = self.conn.cursor()

            # Retrieve all products from the database
            # Example code - You need to replace this with your actual database interaction logic
            cursor.execute("SELECT * FROM Product")
            products = cursor.fetchall()

            print("All products retrieved successfully.")
            return products

        except Exception as e:
            print("Error getting all products:", str(e))
            return []

    def getOrderByUser(self, user_data):
        try:
            cursor = self.conn.cursor()

            # Retrieve orders for the given user from the database
            # Example code - You need to replace this with your actual database interaction logic
            cursor.execute("SELECT * FROM Orders WHERE userId=?", (user_data['userId'],))
            orders = cursor.fetchall()

            print("Orders retrieved successfully.")
            return orders

        except Exception as e:
            print("Error getting orders by user:", str(e))
            return []

