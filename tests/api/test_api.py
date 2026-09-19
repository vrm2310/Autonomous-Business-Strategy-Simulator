from fastapi.testclient import TestClient

from abss.api.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "ABSS",
    }


def test_create_and_get_company() -> None:
    create_response = client.post(
        "/companies",
        json={
            "name": "API Test Company",
            "industry": "Technology",
        },
    )

    assert create_response.status_code == 201

    company = create_response.json()

    assert company["id"] is not None
    assert company["name"] == "API Test Company"
    assert company["industry"] == "Technology"

    company_id = company["id"]

    get_response = client.get(f"/companies/{company_id}")

    assert get_response.status_code == 200

    retrieved_company = get_response.json()

    assert retrieved_company["id"] == company_id
    assert retrieved_company["name"] == "API Test Company"
    assert retrieved_company["industry"] == "Technology"


def test_create_and_get_simulation_cycle() -> None:
    company_response = client.post(
        "/companies",
        json={
            "name": "Simulation Test Company",
            "industry": "Retail",
        },
    )

    assert company_response.status_code == 201

    company_id = company_response.json()["id"]

    create_response = client.post(
        "/simulations/cycles",
        json={
            "company_id": company_id,
        },
    )

    assert create_response.status_code == 201

    cycle = create_response.json()

    assert cycle["id"] is not None
    assert cycle["company_id"] == company_id
    assert cycle["status"] == "created"
    assert cycle["started_at"] is not None
    assert cycle["completed_at"] is None

    cycle_id = cycle["id"]

    get_response = client.get(
        f"/simulations/cycles/{cycle_id}",
    )

    assert get_response.status_code == 200

    retrieved_cycle = get_response.json()

    assert retrieved_cycle["id"] == cycle_id
    assert retrieved_cycle["company_id"] == company_id
    assert retrieved_cycle["status"] == "created"


def test_update_simulation_cycle_status() -> None:
    company_response = client.post(
        "/companies",
        json={
            "name": "Status Test Company",
            "industry": "Finance",
        },
    )

    assert company_response.status_code == 201

    company_id = company_response.json()["id"]

    create_response = client.post(
        "/simulations/cycles",
        json={
            "company_id": company_id,
        },
    )

    assert create_response.status_code == 201

    cycle_id = create_response.json()["id"]

    update_response = client.patch(
        f"/simulations/cycles/{cycle_id}/status",
        json={
            "status": "running",
        },
    )

    assert update_response.status_code == 200

    updated_cycle = update_response.json()

    assert updated_cycle["id"] == cycle_id
    assert updated_cycle["status"] == "running"
    assert updated_cycle["completed_at"] is None