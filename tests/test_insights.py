
from datetime import date, timedelta
from types import SimpleNamespace

from app.services.insights import generate_insights


def create_record(
    symptom,
    severity,
    trigger=None,
    days_ago=0
):
    return SimpleNamespace(
        symptom=symptom,
        severity=severity,
        duration_hours=2.0,
        entry_date=date.today() - timedelta(days=days_ago),
        possible_trigger=trigger
    )


def test_empty_insights():
    result = generate_insights([])

    assert result["total_entries"] == 0
    assert result["average_severity"] == 0
    assert result["highest_severity"] == 0
    assert result["symptom_frequency"] == {}
    assert result["trigger_analysis"] == []


def test_total_entries():
    records = [
        create_record("Headache", 5),
        create_record("Fatigue", 7)
    ]

    result = generate_insights(records)

    assert result["total_entries"] == 2


def test_average_severity():
    records = [
        create_record("Headache", 4),
        create_record("Fatigue", 8)
    ]

    result = generate_insights(records)

    assert result["average_severity"] == 6.0


def test_highest_severity():
    records = [
        create_record("Headache", 4),
        create_record("Fatigue", 9)
    ]

    result = generate_insights(records)

    assert result["highest_severity"] == 9


def test_symptom_frequency():
    records = [
        create_record("Headache", 5),
        create_record("Headache", 7),
        create_record("Fatigue", 4)
    ]

    result = generate_insights(records)

    assert result["symptom_frequency"] == {
        "Headache": 2,
        "Fatigue": 1
    }

    assert result["most_common_symptom"] == "Headache"


def test_recurring_trigger_analysis():
    records = [
        create_record("Headache", 7, "Stress"),
        create_record("Fatigue", 5, "Stress"),
        create_record("Headache", 4, "Lack of sleep")
    ]

    result = generate_insights(records)

    assert len(result["trigger_analysis"]) == 1

    trigger = result["trigger_analysis"][0]

    assert trigger["trigger"] == "stress"
    assert trigger["occurrences"] == 2
    assert trigger["average_severity"] == 6.0


def test_recurring_symptom_insight():
    records = [
        create_record("Headache", 5),
        create_record("Headache", 7)
    ]

    result = generate_insights(records)

    assert any(
        "Headache was reported 2 times" in message
        for message in result["insights"]
    )


def test_insights_api_empty_patient(client):
    response = client.get(
        "/api/insights/UNKNOWN001"
    )

    assert response.status_code == 200

    result = response.json()

    assert result["total_entries"] == 0
    assert result["average_severity"] == 0
    assert result["insights"]


def test_insights_api_with_records(client):
    payload = {
        "patient_id": "TESTINSIGHT",
        "symptom": "Headache",
        "severity": 8,
        "duration_hours": 2,
        "entry_date": date.today().isoformat(),
        "possible_trigger": "Stress"
    }

    first = client.post("/api/symptoms", json=payload)
    assert first.status_code == 201

    second_payload = {
        **payload,
        "entry_date": (
            date.today() - timedelta(days=1)
        ).isoformat()
    }

    second = client.post(
        "/api/symptoms",
        json=second_payload
    )

    assert second.status_code == 201

    response = client.get(
        "/api/insights/TESTINSIGHT"
    )

    assert response.status_code == 200

    result = response.json()

    assert result["total_entries"] == 2
    assert result["average_severity"] == 8.0
    assert result["most_common_symptom"] == "Headache"
    assert result["trigger_analysis"][0]["trigger"] == "stress"
