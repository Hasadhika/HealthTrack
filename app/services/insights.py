
import pandas as pd


def generate_insights(records):

    # Handle empty records
    if not records:
        return {
            "total_entries": 0,
            "average_severity": 0,
            "highest_severity": 0,
            "most_common_symptom": None,
            "symptom_frequency": {},
            "trigger_analysis": [],
            "insights": [
                "No symptom records available. Start logging symptoms to receive insights."
            ]
        }

    # Convert database records into a DataFrame
    data = []

    for record in records:
        data.append({
            "symptom": record.symptom.strip().title(),
            "severity": record.severity,
            "entry_date": record.entry_date,
            "duration_hours": record.duration_hours,
            "possible_trigger": (
                record.possible_trigger.strip().lower()
                if record.possible_trigger
                else None
            )
        })

    df = pd.DataFrame(data)

    # Basic statistical analysis
    total_entries = len(df)

    average_severity = round(
        float(df["severity"].mean()), 2
    )

    highest_severity = int(df["severity"].max())

    # Count symptom frequency
    symptom_frequency = df["symptom"].value_counts().to_dict()

    # Find the most common symptom
    most_common_symptom = (
        max(
            symptom_frequency,
            key=lambda symptom: symptom_frequency[symptom]
        )
        if symptom_frequency
        else None
    )

    insights = []

    # Recurring symptom analysis
    for symptom, count in symptom_frequency.items():

        if count >= 2:
            insights.append(
                f"{symptom} was reported {count} times. "
                "Consider discussing this recurring symptom "
                "with your healthcare provider."
            )

    # Average severity analysis
    if average_severity >= 7:
        insights.append(
            "Your average symptom severity is high. "
            "Consider discussing these entries with your healthcare provider."
        )

    # Highest severity analysis
    if highest_severity >= 9:
        insights.append(
            "You recorded a symptom with severity 9 or 10. "
            "Consider seeking prompt medical advice, especially if it is severe or worsening."
        )

    # Potential trigger analysis
    trigger_analysis = []

    trigger_df = df.dropna(subset=["possible_trigger"])

    if not trigger_df.empty:

        grouped = trigger_df.groupby("possible_trigger").agg(
            occurrences=("severity", "count"),
            average_severity=("severity", "mean")
        )

        for trigger, row in grouped.iterrows():

            occurrences = int(row["occurrences"])

            trigger_average = round(
                float(row["average_severity"]), 2
            )

            if occurrences >= 2:

                trigger_analysis.append({
                    "trigger": trigger,
                    "occurrences": occurrences,
                    "average_severity": trigger_average
                })

                insights.append(
                    f"Symptoms logged alongside '{trigger}' "
                    f"occurred {occurrences} times, with an average "
                    f"severity of {trigger_average}/10. "
                    "This is an observed association, not proof of causation."
                )

    # Severity trend analysis
    daily_severity = (
        df.groupby("entry_date")["severity"]
        .mean()
        .sort_index()
    )

    if len(daily_severity) >= 4:

        midpoint = len(daily_severity) // 2

        earlier_average = daily_severity.iloc[:midpoint].mean()

        recent_average = daily_severity.iloc[midpoint:].mean()

        if recent_average > earlier_average + 1:

            insights.append(
                "Average symptom severity has increased in recent entries. "
                "Consider discussing this trend with your healthcare provider."
            )

        elif recent_average < earlier_average - 1:

            insights.append(
                "Average symptom severity has decreased in recent entries."
            )

    # Default insight
    if not insights:
        insights.append(
            "No significant recurring patterns were identified. "
            "Continue tracking your symptoms."
        )

    # Return final analysis
    return {
        "total_entries": total_entries,
        "average_severity": average_severity,
        "highest_severity": highest_severity,
        "most_common_symptom": most_common_symptom,
        "symptom_frequency": symptom_frequency,
        "trigger_analysis": trigger_analysis,
        "insights": insights
    }
