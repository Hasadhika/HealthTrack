
from datetime import date, timedelta

import pytest


def valid_payload(**overrides):
    payload = {
        "patient_id": "TEST001",
        "symptom": "Headache",
        "severity": 6,
        "duration_hours": 2,
        "entry_date": date.today().isoformat(),
        "possible_trigger": "Stress",
        "notes": "Mild headache"
    }

    payload.update(overrides)
    return payload


def test_create_symptom_success(client):
    response = client.post(
        "/api/symptoms",
        json=valid_payload()
    )

    assert response.status_code == 201
    assert response.json()["symptom"] == "Headache"
    assert response.json()["severity"] == 6


def test_empty_symptom_rejected(client):
    response = client.post(
        "/api/symptoms",
        json=valid_payload(symptom="")
    )

    assert response.status_code == 422


def test_whitespace_symptom_rejected(client):
    response = client.post(
        "/api/symptoms",
        json=valid_payload(symptom="   ")
    )

    assert response.status_code == 422


def test_invalid_severity_rejected(client):
    for severity in [0, 11]:
        response = client.post(
            "/api/symptoms",
            json=valid_payload(severity=severity)
        )

        assert response.status_code == 422


def test_valid_severity_boundaries(client):
    for severity in [1, 10]:
        response = client.post(
            "/api/symptoms",
            json=valid_payload(
                severity=severity,
                patient_id=f"PATIENT{severity}"
            )
        )

        assert response.status_code == 201


def test_invalid_duration_rejected(client):
    for duration in [0, -1, 169]:
        response = client.post(
            "/api/symptoms",
            json=valid_payload(duration_hours=duration)
        )

        assert response.status_code == 422


def test_whitespace_patient_id_rejected(client):
    response = client.post(
        "/api/symptoms",
        json=valid_payload(patient_id="   ")
    )

    assert response.status_code == 422


def test_duplicate_symptom_rejected(client):
    payload = valid_payload()

    first = client.post("/api/symptoms", json=payload)
    second = client.post("/api/symptoms", json=payload)

    assert first.status_code == 201
    assert second.status_code == 409


def test_different_symptoms_same_day_allowed(client):
    first = client.post(
        "/api/symptoms",
        json=valid_payload(symptom="Headache")
    )

    second = client.post(
        "/api/symptoms",
        json=valid_payload(symptom="Fatigue")
    )

    assert first.status_code == 201
    assert second.status_code == 201


def test_weekly_history(client):
    today = date.today()

    recent = valid_payload(
        entry_date=(today - timedelta(days=2)).isoformat()
    )

    old = valid_payload(
        patient_id="TEST001",
        symptom="Fatigue",
        entry_date=(today - timedelta(days=8)).isoformat()
    )

    client.post("/api/symptoms", json=recent)
    client.post("/api/symptoms", json=old)

    response = client.get("/api/symptoms/TEST001/weekly")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["symptom"] == "Headache"


def test_empty_weekly_history(client):
    response = client.get(
        "/api/symptoms/UNKNOWN001/weekly"
    )

    assert response.status_code == 200
    assert response.json() == []


def test_all_history(client):
    client.post(
        "/api/symptoms",
        json=valid_payload()
    )

    client.post(
        "/api/symptoms",
        json=valid_payload(
            symptom="Fatigue",
            entry_date=(date.today() - timedelta(days=10)).isoformat()
        )
    )

    response = client.get("/api/symptoms/TEST001")

    assert response.status_code == 200
    assert len(response.json()) == 2
