def test_get_cart(client, make_user):
    user, headers = make_user("cart@example.com", "123")

    response = client.get("/cart/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["user_id"] == user["id"]
    assert "items" in response.json()


def test_add_to_cart(client, make_user, admin_headers):
    _, headers = make_user("cart2@example.com", "123")
    res_prod = client.post(
        "/products/",
        headers=admin_headers,
        json={"name": "Test Prod", "slug": "test-prod", "price": 100, "stock": 5},
    )
    product_id = res_prod.json()["id"]

    response = client.post(
        f"/cart/items?product_id={product_id}&quantity=2",
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Product added to cart"
