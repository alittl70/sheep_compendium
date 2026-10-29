# Import TestClient to simulate API requests
from fastapi.testclient import TestClient

# Import the FastAPI app instance from the controller module
from main import app

# Create a TestClient instance for the FastAPI app
client = TestClient(app)


# Define a test function for reading a specific sheep
def test_read_sheep():
    # Send a GET request to the endpoint "/sheep/1"
    response = client.get("/sheep/1")

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200

    # Assert that the response JSON matches the expected data
    assert response.json() == {
        # Expected JSON structure
        "id": 1,
        "name": "Spice",
        "breed": "Gotland",
        "sex": "ewe"
    }




# Define a test function for adding a new sheep
def test_add_sheep():
    # TODO: Prepare the new sheep data in a dictionary format.
    new_sheep = {
        "id": 7,
        "name": "Sully",
        "breed": "Suffolk",
        "sex": "ram"
    }

    # TODO: Send a POST request to the endpoint "/sheep" with the new sheep data.
    #  Arguments should be your endpoint and new sheep data.
    response = client.post("/sheep/", json=new_sheep)

    # TODO: Assert that the response status code is 201 (Created)
    assert response.status_code == 201

    # TODO: Assert that the response JSON matches the new sheep data
    assert response.json() == new_sheep

    # TODO: Verify that the sheep was actually added to the database by retrieving the new sheep by ID.
    #  include an assert statement to see if the new sheep data can be retrieved.
    get_response = client.get("/sheep/7")
    assert get_response.status_code == 200
    assert get_response.json() == new_sheep



# EXTRA CREDIT: Test reading all sheep
def test_read_all_sheep():
    response = client.get("/sheep/")
    assert response.status_code == 200

    all_sheep = response.json()
    # The database starts with 6 sheep, so there should be at least 6
    assert len(all_sheep) >= 6
    # Spice should be in the list
    assert {"id": 1, "name": "Spice", "breed": "Gotland", "sex": "ewe"} in all_sheep


# EXTRA CREDIT: Test updating a sheep
def test_update_sheep():
    updated_sheep = {
        "id": 2,
        "name": "Blondie",
        "breed": "Polypay",
        "sex": "ewe"
    }

    # Send a PUT request to update sheep 2
    response = client.put("/sheep/2", json=updated_sheep)
    assert response.status_code == 200
    assert response.json() == updated_sheep

    # Verify the change was saved
    get_response = client.get("/sheep/2")
    assert get_response.json()["sex"] == "ewe"


# EXTRA CREDIT: Test deleting a sheep
def test_delete_sheep():
    # Add a sheep to delete, so the original 6 sheep stay untouched
    temp_sheep = {"id": 8, "name": "Biscuit", "breed": "Babydoll", "sex": "ewe"}
    client.post("/sheep/", json=temp_sheep)

    # Send a DELETE request
    response = client.delete("/sheep/8")
    assert response.status_code == 204

    # Verify it's gone: reading it again should return 404
    get_response = client.get("/sheep/8")
    assert get_response.status_code == 404