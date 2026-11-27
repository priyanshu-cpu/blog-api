def test_register_user(client, user_data):

    response = client.post(
        "/register",
        json=user_data
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == user_data["email"]
    assert "password" not in data
    assert "hashed_password" not in data


def test_duplicate_email(client, registered_user):

    response = client.post(
        "/register",
        json=registered_user
    )

    assert response.status_code == 409