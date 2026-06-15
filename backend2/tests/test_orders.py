def create_product(client, admin_headers, slug="order-prod", stock=10):
    response = client.post(
        "/products/",
        headers=admin_headers,
        json={"name": "Order Prod", "slug": slug, "price": 50000, "stock": stock},
    )
    assert response.status_code == 200
    return response.json()


def test_create_order(client, make_user, admin_headers):
    user, headers = make_user("order@example.com", "123")
    product = create_product(client, admin_headers)

    order_data = {
        "user_id": user["id"],
        "total_price": 100000,
        "status": "pending",
        "payment_method": "cod",
        "shipping_address": "123 Main St",
        "items": [
            {"product_id": product["id"], "quantity": 2, "price": 50000}
        ],
    }
    response = client.post("/orders/", headers=headers, json=order_data)
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == user["id"]
    assert float(data["total_price"]) == 100000
    assert len(data["items"]) == 1
    assert data["items"][0]["product_id"] == product["id"]
    assert float(data["items"][0]["price"]) == 50000


def test_create_order_ignores_client_prices(client, make_user, admin_headers):
    user, headers = make_user("order_price@example.com", "123")
    product = create_product(client, admin_headers, slug="order-price-prod", stock=10)

    response = client.post(
        "/orders/",
        headers=headers,
        json={
            "user_id": user["id"],
            "total_price": 1,
            "status": "pending",
            "payment_method": "cod",
            "shipping_address": "123 Main St",
            "items": [
                {"product_id": product["id"], "quantity": 2, "price": 1}
            ],
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert float(data["total_price"]) == 100000
    assert float(data["items"][0]["price"]) == 50000


def test_get_order_detail(client, make_user, admin_headers):
    user, headers = make_user("order_detail@example.com", "123")
    product = create_product(client, admin_headers, slug="order-detail-prod")

    order_data = {
        "user_id": user["id"],
        "total_price": 100,
        "status": "confirmed",
        "payment_method": "bank",
        "shipping_address": "Test",
        "items": [{"product_id": product["id"], "quantity": 1, "price": 1}],
    }
    res_order = client.post("/orders/", headers=headers, json=order_data)
    order_id = res_order.json()["id"]

    response = client.get(f"/orders/{order_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["status"] == "confirmed"


def test_get_user_orders(client, make_user):
    _, headers = make_user("user_order@example.com", "123")

    response = client.get("/orders/my-orders", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_cancel_order_restores_stock(client, make_user, admin_headers):
    _, headers = make_user("order_cancel@example.com", "123")
    product = create_product(client, admin_headers, slug="order-cancel-prod", stock=5)

    order_response = client.post(
        "/orders/",
        headers=headers,
        json={
            "total_price": 1,
            "status": "pending",
            "payment_method": "cod",
            "shipping_address": "123 Main St",
            "items": [{"product_id": product["id"], "quantity": 2, "price": 1}],
        },
    )
    assert order_response.status_code == 200

    stock_after_order = client.get(f"/products/{product['id']}").json()["stock"]
    assert stock_after_order == 3

    cancel_response = client.patch(
        f"/orders/{order_response.json()['id']}/status?status=cancelled",
        headers=admin_headers,
    )
    assert cancel_response.status_code == 200

    stock_after_cancel = client.get(f"/products/{product['id']}").json()["stock"]
    assert stock_after_cancel == 5
