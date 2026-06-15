import pandas as pd

test_cases = [
    # Users
    {
        "ID": "TC-001",
        "Module": "Users",
        "Test Case Name": "Create User - Success",
        "Steps": "Send POST to /users/ with valid email, name, phone, password",
        "Expected Result": "HTTP 200, returns user object with ID",
        "Priority": "High"
    },
    {
        "ID": "TC-002",
        "Module": "Users",
        "Test Case Name": "Create User - Duplicate Email",
        "Steps": "Send POST to /users/ with an email that already exists",
        "Expected Result": "HTTP 400, detail: 'Email already registered'",
        "Priority": "Medium"
    },
    {
        "ID": "TC-003",
        "Module": "Users",
        "Test Case Name": "Read User Detail",
        "Steps": "Send GET to /users/{user_id}",
        "Expected Result": "HTTP 200, returns user details",
        "Priority": "High"
    },
    # Products
    {
        "ID": "TC-004",
        "Module": "Products",
        "Test Case Name": "Create Product",
        "Steps": "Send POST to /products/ with basic product info",
        "Expected Result": "HTTP 200, returns product with ID",
        "Priority": "High"
    },
    {
        "ID": "TC-005",
        "Module": "Products",
        "Test Case Name": "List Products",
        "Steps": "Send GET to /products/",
        "Expected Result": "HTTP 200, returns a list of products",
        "Priority": "High"
    },
    {
        "ID": "TC-006",
        "Module": "Products",
        "Test Case Name": "Get Product Detail",
        "Steps": "Send GET to /products/{product_id}",
        "Expected Result": "HTTP 200, returns product details",
        "Priority": "High"
    },
    # Cart
    {
        "ID": "TC-007",
        "Module": "Cart",
        "Test Case Name": "Get or Initialize Cart",
        "Steps": "Send GET to /cart/{user_id}",
        "Expected Result": "HTTP 200, returns cart object (creates new if not exists)",
        "Priority": "Medium"
    },
    {
        "ID": "TC-008",
        "Module": "Cart",
        "Test Case Name": "Add Item to Cart",
        "Steps": "Send POST to /cart/items with cart_id, product_id, quantity",
        "Expected Result": "HTTP 200, message: 'Product added to cart'",
        "Priority": "Medium"
    },
    # Orders
    {
        "ID": "TC-009",
        "Module": "Orders",
        "Test Case Name": "Create Order",
        "Steps": "Send POST to /orders/ with user_id, address, items list",
        "Expected Result": "HTTP 200, returns order with items",
        "Priority": "High"
    },
    {
        "ID": "TC-010",
        "Module": "Orders",
        "Test Case Name": "Get Order Detail",
        "Steps": "Send GET to /orders/{order_id}",
        "Expected Result": "HTTP 200, returns full order details",
        "Priority": "High"
    },
    {
        "ID": "TC-011",
        "Module": "Orders",
        "Test Case Name": "List User Order History",
        "Steps": "Send GET to /orders/user/{user_id}",
        "Expected Result": "HTTP 200, returns list of orders for the user",
        "Priority": "Medium"
    }
]

df = pd.DataFrame(test_cases)
file_name = "HoaDongDuong_TestPlan.xlsx"

try:
    df.to_excel(file_name, index=False)
    print(f"Successfully exported test plan to {file_name}")
except Exception as e:
    print(f"Error: {e}")
