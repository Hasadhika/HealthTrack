
const API_BASE = "/api";

const patientInput = document.getElementById("patientId");
const symptomForm = document.getElementById("symptomForm");
const severityInput = document.getElementById("severity");

let currentHistory = [];

// Display today's date
function initializeDashboard() {
    const today = new Date();
    const localDate = [
        today.getFullYear(),
        String(today.getMonth() + 1).padStart(2, "0"),
        String(today.getDate()).padStart(2, "0")
    ].join("-");

    document.getElementById("currentDate").textContent =
        today.toLocaleDateString("en-IN", {
            day: "numeric",
            month: "short",
            year: "numeric"
        });

    document.getElementById("entryDate").value = localDate;
    document.getElementById("entryDate").max = localDate;

    loadDashboard();
}

// Update severity slider
severityInput.addEventListener("input", () => {
    document.getElementById("severityValue").textContent =
        `${severityInput.value} / 10`;
});

// Display messages
function showMessage(message, type) {
    const element = document.getElementById("formMessage");
    element.textContent = message;
    element.className = `message ${type}`;
}

// Load patient dashboard
async function loadDashboard() {
    const patientId = patientInput.value.trim();

    if (!patientId) {
        showMessage("Please enter a valid patient ID.", "error");
        return;
    }

    try {
        await Promise.all([
            loadHistory(patientId),
            loadInsights(patientId)
        ]);
    } catch (error) {
        console.error("Dashboard loading error:", error);
    }
}

// Load weekly symptom history
async function loadHistory(patientId) {
    const response = await fetch(
        `${API_BASE}/symptoms/${encodeURIComponent(patientId)}/weekly`
    );

    if (!response.ok) {
        throw new Error("Unable to load symptom history.");
    }

    const records = await response.json();

    currentHistory = records;

    renderHistory(records);
    renderStatistics(records);
}

// Render history table
function renderHistory(records) {
    const tbody = document.getElementById("historyBody");

    tbody.replaceChildren();

    if (records.length === 0) {
        const row = document.createElement("tr");
        const cell = document.createElement("td");

        cell.colSpan = 5;
        cell.className = "empty-state";
        cell.textContent = "No symptom records available.";

        row.appendChild(cell);
        tbody.appendChild(row);
        return;
    }

    records.forEach(record => {
        const row = document.createElement("tr");

        const values = [
            new Date(`${record.entry_date}T00:00:00`).toLocaleDateString("en-IN"),
            record.symptom,
            `${record.severity}/10`,
            `${record.duration_hours} hrs`,
            record.possible_trigger || "Not specified"
        ];

        values.forEach((value, index) => {
            const cell = document.createElement("td");
            cell.textContent = value;

            if (index === 2) {
                const severity = document.createElement("span");
                severity.className =
                    "severity-pill " +
                    (record.severity <= 3
                        ? "severity-low"
                        : record.severity <= 6
                            ? "severity-medium"
                            : "severity-high");

                severity.textContent = value;
                cell.replaceChildren(severity);
            }

            row.appendChild(cell);
        });

        tbody.appendChild(row);
    });
}

// Calculate weekly statistics
function renderStatistics(records) {
    const total = records.length;

    const average = total
        ? records.reduce((sum, item) => sum + item.severity, 0) / total
        : 0;

    const highest = total
        ? Math.max(...records.map(item => item.severity))
        : 0;

    const frequency = {};

    records.forEach(record => {
        const name = record.symptom.trim();

        frequency[name] = (frequency[name] || 0) + 1;
    });

    const common = Object.keys(frequency).length
        ? Object.entries(frequency).sort((a, b) => b[1] - a[1])[0][0]
        : "--";

    document.getElementById("totalEntries").textContent = total;
    document.getElementById("averageSeverity").textContent =
        `${average.toFixed(1)}/10`;
    document.getElementById("highestSeverity").textContent =
        `${highest}/10`;
    document.getElementById("commonSymptom").textContent = common;
}

// Load AI-assisted insights
async function loadInsights(patientId) {
    const response = await fetch(
        `${API_BASE}/insights/${encodeURIComponent(patientId)}`
    );

    if (!response.ok) {
        throw new Error("Unable to load insights.");
    }

    const result = await response.json();

    renderFrequency(result.symptom_frequency || {});
    renderInsights(result.insights || []);
    renderTriggers(result.trigger_analysis || []);
}

// Render symptom frequency bars
function renderFrequency(frequency) {
    const container = document.getElementById("frequencyChart");

    container.replaceChildren();

    const entries = Object.entries(frequency);

    if (!entries.length) {
        container.textContent = "No symptom data available.";
        container.className = "empty-state";
        return;
    }

    container.className = "";

    const maximum = Math.max(...entries.map(item => item[1]), 1);

    entries.forEach(([symptom, count]) => {
        const wrapper = document.createElement("div");
        wrapper.className = "frequency-item";

        const heading = document.createElement("div");
        heading.className = "frequency-heading";

        const name = document.createElement("span");
        name.textContent = symptom;

        const number = document.createElement("strong");
        number.textContent = `${count} entries`;

        heading.append(name, number);

        const track = document.createElement("div");
        track.className = "progress-track";

        const fill = document.createElement("div");
        fill.className = "progress-fill";
        fill.style.width = `${count / maximum * 100}%`;

        track.appendChild(fill);
        wrapper.append(heading, track);
        container.appendChild(wrapper);
    });
}

// Render generated insights
function renderInsights(insights) {
    const container = document.getElementById("insightList");

    container.replaceChildren();

    if (!insights.length) {
        container.textContent = "No insights available yet.";
        container.className = "empty-state";
        return;
    }

    container.className = "";

    insights.forEach(message => {
        const item = document.createElement("div");

        item.className = "insight-item";
        item.textContent = `✧ ${message}`;

        container.appendChild(item);
    });
}

// Render potential trigger associations
function renderTriggers(triggers) {
    const container = document.getElementById("triggerList");

    container.replaceChildren();

    if (!triggers.length) {
        const message = document.createElement("p");
        message.className = "empty-state";
        message.textContent =
            "No recurring trigger associations identified.";

        container.appendChild(message);
        return;
    }

    triggers.forEach(trigger => {
        const item = document.createElement("div");
        item.className = "trigger-item";

        const name = document.createElement("strong");
        name.textContent = trigger.trigger;

        const details = document.createElement("span");
        details.textContent =
            `${trigger.occurrences} entries · Average severity ${trigger.average_severity}/10`;

        item.append(name, details);
        container.appendChild(item);
    });
}

// Submit symptom form
symptomForm.addEventListener("submit", async event => {
    event.preventDefault();

    const patientId = patientInput.value.trim();
    const symptom = document.getElementById("symptom").value.trim();
    const entryDate = document.getElementById("entryDate").value;
    const duration = Number(document.getElementById("duration").value);
    const severity = Number(severityInput.value);
    const trigger = document.getElementById("trigger").value.trim();
    const notes = document.getElementById("notes").value.trim();

    if (!patientId || !symptom || !entryDate) {
        showMessage("Please fill in all required fields.", "error");
        return;
    }

    if (severity < 1 || severity > 10) {
        showMessage("Severity must be between 1 and 10.", "error");
        return;
    }

    if (!Number.isFinite(duration) || duration <= 0 || duration > 168) {
        showMessage("Duration must be greater than 0 and at most 168 hours.", "error");
        return;
    }

    const payload = {
        patient_id: patientId,
        symptom: symptom,
        severity: severity,
        duration_hours: duration,
        entry_date: entryDate,
        possible_trigger: trigger || null,
        notes: notes || null
    };

    const submitButton = symptomForm.querySelector("button[type='submit']");
    submitButton.disabled = true;
    submitButton.textContent = "Saving...";

    try {
        const response = await fetch(`${API_BASE}/symptoms`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(
                result.detail || "Unable to save symptom."
            );
        }

        showMessage("Symptom recorded successfully!", "success");

        symptomForm.reset();
        severityInput.value = 5;
        document.getElementById("severityValue").textContent = "5 / 10";

        initializeFormDate();

        await loadDashboard();

    } catch (error) {
        showMessage(error.message, "error");
    } finally {
        submitButton.disabled = false;
        submitButton.textContent = "+ Save Symptom";
    }
});

function initializeFormDate() {
    const today = new Date();

    const localDate = [
        today.getFullYear(),
        String(today.getMonth() + 1).padStart(2, "0"),
        String(today.getDate()).padStart(2, "0")
    ].join("-");

    document.getElementById("entryDate").value = localDate;
    document.getElementById("entryDate").max = localDate;
}

// Refresh buttons
document.getElementById("refreshButton").addEventListener(
    "click",
    loadDashboard
);

document.getElementById("loadButton").addEventListener(
    "click",
    loadDashboard
);

initializeDashboard();

