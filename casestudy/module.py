from dao.OrderProc import OrderProcessor
from entity.user import User
from entity.product import Product
from entity.order import Order
from exceptions import usernotfound,ordernotfound  

class MainMenu:
    @staticmethod
    def main_menu(cursor, conn):
        order_processor = OrderProcessor(cursor, conn)

        while True:
            print("\n=== Welcome to the order management app ===")
            print("1. Create Order")
            print("2. Cancel Order")
            print("3. Create Product")
            print("4. Create User")
            print("5. Get All Products")
            print("6. Get Order by User")
            print("7. Exit")

            choice = input("Enter your choice: ")

            try:
                if choice == '1':
                    # Get existing user IDs
                    cursor.execute("SELECT userId FROM [User]")
                    existing_user_ids = [str(row.userId) for row in cursor.fetchall()]
                    print("Existing User IDs:", ", ".join(existing_user_ids))

                    # Get existing product IDs
                    cursor.execute("SELECT productId FROM Product")
                    existing_product_ids = [str(row.productId) for row in cursor.fetchall()]
                    print("Existing Product IDs:", ", ".join(existing_product_ids))

                    user_id = input("Enter user ID: ")
                    product_ids = input("Enter product IDs (comma-separated): ").split(",")
                    order_processor.create_order(user_id, product_ids)
                elif choice == '2':
                    # Get existing order IDs
                    cursor.execute("SELECT orderId FROM Orders")
                    existing_order_ids = [str(row.orderId) for row in cursor.fetchall()]
                    print("Existing Order IDs:", ", ".join(existing_order_ids))

                    user_id = input("Enter user ID: ")
                    order_id = input("Enter order ID: ")
                    order_processor.cancel_order(user_id, order_id)
                elif choice == '3':
                    product_data = Product(None, None, None, None, None, None)
                    product_data.setProductId(input("Enter product ID: "))
                    product_data.setProductName(input("Enter product name: "))
                    product_data.setDescription(input("Enter product description: "))
                    product_data.setPrice(float(input("Enter product price: ")))
                    product_data.setQuantityInStock(int(input("Enter quantity in stock: ")))
                    product_data.setType(input("Enter product type: "))

                    order_processor.create_product(product_data)
                elif choice == '4':
                    user_data = {
                        'userId': input("Enter user ID: "),
                        'username': input("Enter username: "),
                        'password': input("Enter password: "),
                        'role': input("Enter role: ")
                    }
                    order_processor.create_user(user_data)
                elif choice == '5':
                    order_processor.get_all_products()
                elif choice == '6':
                    user_id = input("Enter user ID: ")
                    order_processor.get_order_by_user(user_id)
                elif choice == '7':
                    print("Exiting...")
                    break
                else:
                    print("Invalid choice. Please try again.")
            except Exception as e:
                if str(e) == "UserNotFound":
                    print("User not found. Please enter a valid user ID.")
                elif str(e) == "OrderNotFound":
                    print("Order not found. Please enter a valid order ID.")
                else:
                    print("An error occurred:", str(e))


if __name__ == "__main__":
    print("This is the main module.")
