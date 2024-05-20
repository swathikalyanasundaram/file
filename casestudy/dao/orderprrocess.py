import pyodbc

class OrderProcessor:
    def __init__(self, cursor, conn):
        self.cursor = cursor
        self.conn = conn

    def create_order(self, user_id, product_ids):
        try:
            # Check if user exists
            self.cursor.execute("SELECT * FROM NewUser WHERE userId=?", (user_id,))
            Newuser = self.cursor.fetchone()
            if not Newuser:
                raise Exception("UserNotFound")

            # Check if products exist and are in stock
            for product_id in product_ids:
                self.cursor.execute("SELECT * FROM Product WHERE productId=? AND quantityInStock > 0", (product_id,))
                product = self.cursor.fetchone()
                if not product:
                    print(f"Product with ID {product_id} not found or out of stock.")
                    return

            # Create order
            for product_id in product_ids:
                self.cursor.execute("INSERT INTO Orders (userId, productId) VALUES (?, ?)", (user_id, product_id))
            self.conn.commit()
            print("Order created successfully.")
        except Exception as e:
            self.conn.rollback()
            if str(e) == "UserNotFound":
                raise e
            print("Error creating order:", str(e))

    def cancel_order(self, user_id, order_id):
        try:
            # Check if order exists and belongs to the user
            self.cursor.execute("SELECT * FROM Orders WHERE userId=? AND orderId=?", (user_id, order_id))
            order = self.cursor.fetchone()
            if not order:
                raise Exception("OrderNotFound")

            # Cancel order
            self.cursor.execute("DELETE FROM Orders WHERE userId=? AND orderId=?", (user_id, order_id))
            self.conn.commit()
            print("Order cancelled successfully.")
        except Exception as e:
            self.conn.rollback()
            if str(e) == "OrderNotFound":
                raise e
            print("Error cancelling order:", str(e))

    def create_product(self, product_data):
        try:
            # Check if the product ID already exists
            self.cursor.execute("SELECT productId FROM Product WHERE productId = ?", (product_data.getProductId(),))
            if self.cursor.fetchone():
                print(f"Product ID {product_data.getProductId()} already exists. Please enter a different product ID.")
                return

            # Insert product into database
            self.cursor.execute("INSERT INTO Product (productId, productName, description, price, quantityInStock, type) VALUES (?, ?, ?, ?, ?, ?)",
                                (product_data.getProductId(), product_data.getProductName(), product_data.getDescription(), product_data.getPrice(), product_data.getQuantityInStock(), product_data.getType()))
            self.conn.commit()
            print("Product created successfully.")
        except Exception as e:
            self.conn.rollback()
            print("Error creating product:", str(e))

    def create_user(self, user_data):
        try:
        # Insert user into database
            self.cursor.execute("INSERT INTO Newuser (username, password, role) VALUES (?, ?, ?)",
                                (user_data['username'], user_data['password'], user_data['role']))
            self.conn.commit()
            print("User created successfully.")
        except Exception as e:
            self.conn.rollback()
            print("Error creating user:", str(e))

           

    def get_all_products(self):
        try:
            # Retrieve all products from the database
            self.cursor.execute("SELECT * FROM Product")
            products = self.cursor.fetchall()

            if products:
                print("Existing Products:")
                for product in products:
                    print(f"Product ID: {product[0]}, Name: {product[1]}, Description: {product[2]}, Price: {product[3]}, Quantity in Stock: {product[4]}, Type: {product[5]}")  # Assuming productId, productName, description, price, quantityInStock, and type are the first six columns
            else:
                print("No products found.")

            return products

        except Exception as e:
            print("Error getting all products:", str(e))
            return []

    def get_order_by_user(self, user_id):
        try:
            # Retrieve orders for a specific user from the database
            self.cursor.execute("SELECT * FROM Orders WHERE userId=?", (user_id,))
            orders = self.cursor.fetchall()

            if orders:
                print("Orders fetched successfully:")
                for order in orders:
                    # Extract order details
                    order_id = order[2]
                    user_id = order[0]
                    product_id = order[1]

                    # Fetch product details from the Product table
                    self.cursor.execute("SELECT productName FROM Product WHERE productId=?", (product_id,))
                    product_details = self.cursor.fetchone()

                    # Extract product name from the fetched details
                    product_name = product_details[0] if product_details else "Unknown Product"

                    # Print order details including product name
                    print(f"Order ID: {order_id}, User ID: {user_id}, Product ID: {product_id}, Product Name: {product_name}")

            else:
                print("No orders found for the user.")

            return orders

        except Exception as e:
            print("Error getting orders by user:", str(e))
            return []

        