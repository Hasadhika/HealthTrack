
# HealthTrack – Patient Symptom Tracker

HealthTrack is a patient-focused web application that allows users to record daily symptoms, monitor their health history, and receive insights based on their recorded data.

The application uses Python, FastAPI, SQLite, SQLAlchemy, and Pandas to provide symptom tracking and basic health pattern analysis.

> **Disclaimer:** HealthTrack is an educational assessment project. Its insights are informational and are not medical advice.

## Features

- Daily symptom logging.
- Symptom severity tracking (1–10).
- Symptom duration tracking.
- Optional trigger and notes fields.
- Input validation using Pydantic.
- Duplicate symptom entry prevention.
- Seven-day patient symptom history.
- Complete patient symptom history.
- Health insights and symptom frequency analysis.
- Average and highest severity calculations.
- Potential trigger pattern analysis.
- Interactive patient dashboard.
- Automated testing using Pytest.

## Technology Stack

| Category | Technology |
|---|---|
| Programming Language | Python |
| Backend Framework | FastAPI |
| Database | SQLite |
| ORM | SQLAlchemy |
| Data Analysis | Pandas |
| Validation | Pydantic |
| Frontend | HTML, CSS, JavaScript |
| API Documentation | Swagger UI |
| Testing | Pytest, HTTPX |
| Server | Uvicorn |

## System Architecture

The application follows a modular architecture with separate components for frontend interaction, API handling, database operations, and insights generation.

## Project Structure

```text
HealthTrack/
│
├── app/
│   ├── routes/
│   │   ├── symptoms.py
│   │   └── insights.py
│   │
│   ├── services/
│   │   └── insights.py
│   │
│   ├── static/
│   │   ├── style.css
│   │   └── script.js
│   │
│   ├── templates/
│   │   └── index.html
│   │
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_symptoms.py
│   └── test_insights.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation and Setup

### Prerequisites

- Python 3.10 or above
- pip
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/Hasadhika/HealthTrack.git
cd HealthTrack
```

### 2. Create a Virtual Environment

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the Application

```bash
python -m uvicorn app.main:app --reload
```

### 5. Access the Application

Dashboard:

http://127.0.0.1:8000/

Swagger API Documentation:

http://127.0.0.1:8000/docs

Health Check:

http://127.0.0.1:8000/health

The SQLite database is created locally when the application initializes.

## REST API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/symptoms` | Create a symptom entry |
| GET | `/api/symptoms/{patient_id}/weekly` | Retrieve the last seven calendar days of symptom history |
| GET | `/api/symptoms/{patient_id}` | Retrieve complete symptom history |
| GET | `/api/insights/{patient_id}` | Generate health insights |
| GET | `/health` | Check application status |

### Symptom Entry Example

POST `/api/symptoms`

Request Body:

```json
{
  "patient_id": "P001",
  "symptom": "Headache",
  "severity": 6,
  "duration_hours": 2,
  "entry_date": "2026-11-07",
  "possible_trigger": "Stress",
  "notes": "Mild headache during the afternoon"
}
```

### Validation Rules

- Patient ID cannot be empty.
- Symptom name cannot be empty.
- Severity must be between 1 and 10.
- Duration must be greater than zero and no more than 168 hours.
- Duplicate entries for the same patient, symptom, and date are rejected.
- Invalid request data returns HTTP 422.
- Duplicate entries return HTTP 409.

## Health Insights Engine

HealthTrack uses Pandas for analyzing recorded symptom data.

The insights engine provides:

1. **Total Entries:** Total number of recorded symptoms.
2. **Average Severity:** Average severity across recorded entries.
3. **Highest Severity:** Highest recorded symptom severity.
4. **Most Common Symptom:** Symptom reported most frequently.
5. **Symptom Frequency:** Number of occurrences of each symptom.
6. **Trigger Analysis:** Identifies repeated patient-reported trigger associations.
7. **Trend Analysis:** Compares symptom severity across different dates.

### Insights Methodology

The insights engine uses statistical calculations and rule-based analysis to identify patterns in patient records.

It does not train a machine learning model or predict medical conditions.

Repeated trigger associations are observations from patient entries and do not establish medical causation.

## Automated Testing

The project uses Pytest and FastAPI TestClient for automated testing.

Run the test suite:

```bash
python -m pytest -v
```

Run tests with a concise summary:

```bash
python -m pytest -q
```

### Test Coverage

| Test Area | Scenarios |
|---|---|
| Symptom Creation | Valid symptom entry |
| Input Validation | Empty and whitespace-only inputs |
| Severity Validation | Values below 1 and above 10 |
| Boundary Testing | Severity values 1 and 10 |
| Duration Validation | Invalid duration values |
| Duplicate Handling | Duplicate symptom entries |
| Multiple Symptoms | Different symptoms on the same date |
| Weekly History | Seven-day date filtering |
| Empty History | Patients without records |
| Complete History | Retrieving all patient records |
| Insights | Average and highest severity |
| Frequency Analysis | Most common symptom |
| Trigger Analysis | Repeated trigger associations |
| Empty Insights | Handling patients without records |

Tests use an isolated in-memory SQLite database to avoid modifying the application's local database.

## Key Design Decisions

**1. FastAPI**

FastAPI was selected to build lightweight REST APIs with automatic interactive documentation and request validation.

**2. SQLite**

SQLite provides simple local database storage without requiring a separate database server.

**3. SQLAlchemy**

SQLAlchemy separates database operations from API logic and provides ORM-based database access.

**4. Pydantic**

Pydantic validates incoming symptom data and ensures that required fields and severity limits are respected.

**5. Pandas**

Pandas simplifies symptom frequency calculations, severity analysis, and identification of recurring patterns.

**6. Modular Architecture**

Routes, services, database models, schemas, and frontend files are separated to improve maintainability and readability.

## Limitations

- The application does not implement user authentication.
- The application is designed for local demonstration.
- Insights are statistical and rule-based, not trained ML predictions.
- Trigger associations do not prove causation.
- The application is not intended for clinical diagnosis or production medical-data storage.

## AI Usage Disclosure

AI tools were used as development assistants during this project.

**Tool Used:** ChatGPT (OpenAI).

**Areas where AI assistance was used:**

- Debugging Python errors and implementation issues.
- Pydantic validation guidance.
- Pandas-based insights implementation guidance.
- Automated test-case scaffolding.
- Frontend styling and UI refinement.


**Developer verification:**

Adapted the suggested implementations, ran the application locally, tested the API through Swagger UI, verified symptom logging and history retrieval, checked validation and duplicate handling, and executed the automated Pytest suite.

AI-generated suggestions were reviewed and modified during implementation.

## Future Enhancements

- Interactive symptom trend charts.
- Exportable patient health reports.
- More advanced statistical analysis.
- Optional healthcare-provider report sharing.
- Improved accessibility and responsive design.

## Author

**Hasadhika Thottempudi**

GitHub: https://github.com/Hasadhika

---

Developed as a Python, AI/ML, and full-stack development assessment project.
