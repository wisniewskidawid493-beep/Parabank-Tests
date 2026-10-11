import pytest
import requests

BASE_URL = "https://reqres.in/api"


@pytest.fixture
def default_headers():
    return {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }


# 1. Test POST: Tworzenie nowego użytkownika
def test_create_user_success(default_headers):
    endpoint = f"{BASE_URL}/users"
    payload = {
        "name": "Jan Kowalski",
        "job": "QA Automation Engineer"
    }

    response = requests.post(endpoint, json=payload, headers=default_headers)
    data = response.json()

    # Weryfikacja statusu 201 Created
    assert response.status_code == 201, f"Oczekiwano 201, dostano {response.status_code}"
    
    # Weryfikacja obecności kluczy generowanych przez serwer
    assert "id" in data, "Brak wygenerowanego 'id' w odpowiedzi"
    assert "createdAt" in data, "Brak znacznika czasu 'createdAt'"
    
    # Weryfikacja poprawności przesłanych danych
    assert data["name"] == payload["name"]
    assert data["job"] == payload["job"]


# 2. Test PUT: Aktualizacja danych użytkownika
def test_update_user_details(default_headers):
    user_id = 2
    endpoint = f"{BASE_URL}/users/{user_id}"
    payload = {
        "name": "Jan Kowalski",
        "job": "Senior QA Engineer"
    }

    response = requests.put(endpoint, json=payload, headers=default_headers)
    data = response.json()

    assert response.status_code == 200
    assert data["job"] == "Senior QA Engineer"
    assert "updatedAt" in data


# 3. Test walidacyjny (Negative Testing): Pobranie nieistniejącego użytkownika
def test_get_non_existing_user_returns_404(default_headers):
    invalid_user_id = 9999
    endpoint = f"{BASE_URL}/users/{invalid_user_id}"

    response = requests.get(endpoint, headers=default_headers)

    assert response.status_code == 404
    assert response.json() == {}, "Odpowiedź dla braku zasobu powinna być pustym obiektem JSON"


# 4. Sparametryzowany test walidujący różne role/stanowiska
@pytest.mark.parametrize("job_title", [
    ("DevOps"),
    ("Backend Developer"),
    ("Frontend Developer")
])
def test_create_user_with_different_jobs(default_headers, job_title):
    endpoint = f"{BASE_URL}/users"
    payload = {"name": "Test User", "job": job_title}

    response = requests.post(endpoint, json=payload, headers=default_headers)
    
    assert response.status_code == 201
    assert response.json()["job"] == job_title