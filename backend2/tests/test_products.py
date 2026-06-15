def test_create_product(client, admin_headers):
    response = client.post(
        "/products/",
        headers=admin_headers,
        json={
            "name": "Dau goi buoi",
            "slug": "dau-goi-buoi",
            "description": "Dau goi giup moc toc",
            "price": 150000,
            "stock": 100,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Dau goi buoi"
    assert "id" in data


def test_read_products(client):
    response = client.get("/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_product_detail(client, admin_headers):
    res = client.post(
        "/products/",
        headers=admin_headers,
        json={
            "name": "Sap vuot toc",
            "slug": "sap-vuot-toc",
            "price": 200000,
            "stock": 50,
        },
    )
    product_id = res.json()["id"]

    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["slug"] == "sap-vuot-toc"
