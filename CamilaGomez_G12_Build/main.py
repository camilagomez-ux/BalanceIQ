

import streamlit as st
from models import BalanceIQModel


def track_choice(choice, scores=None):

    if scores is None:
        scores = {
            "academic_pressure": 50,
            "focus_score": 70,
            "balance_score": 65
        }

    scores = scores.copy()

    if choice == "1":
        scores["academic_pressure"] += 15
        scores["focus_score"] -= 10
        scores["balance_score"] -= 10
        message = "You selected: Increase study workload."

    elif choice == "2":
        scores["academic_pressure"] -= 10
        scores["focus_score"] += 10
        scores["balance_score"] += 15
        message = "You selected: Take a structured break."

    else:
        return None

    for key in scores:
        scores[key] = max(0, min(100, scores[key]))

    if scores["balance_score"] < 60:
        warning = "Your current routine may be difficult to sustain."
    elif scores["academic_pressure"] > 60:
        warning = "Your academic pressure is increasing."
    else:
        warning = "Your routine is maintaining a good balance."

    return {
        "scores": scores,
        "message": message,
        "warning": warning
    }


# Initialize the model
if "model" not in st.session_state:
    st.session_state.model = BalanceIQModel()

model = st.session_state.model

# Page title
st.title("BalanceIQ")
st.write("Track your academic pressure, focus, and balance.")

# Display current scores
scores = model.get_scores()

st.subheader("Your Current Scores")

col1, col2, col3 = st.columns(3)

col1.metric("Academic Pressure", scores["academic_pressure"])
col2.metric("Focus Score", scores["focus_score"])
col3.metric("Balance Score", scores["balance_score"])

st.divider()

# User choices
st.subheader("Choose Your Next Action")

if st.button("Increase Study Workload"):
    result = track_choice("1", model.get_scores())
    model.update_scores(result["scores"])

    st.session_state.last_message = result["message"]
    st.session_state.last_warning = result["warning"]

if st.button("Take a Structured Break"):
    result = track_choice("2", model.get_scores())
    model.update_scores(result["scores"])

    st.session_state.last_message = result["message"]
    st.session_state.last_warning = result["warning"]

# Display messages
if "last_message" in st.session_state:
    st.success(st.session_state.last_message)
    st.info(st.session_state.last_warning)

st.divider()

# Activity input form
st.subheader("Track Your Activity")

with st.form("activity_form"):

    activity_name = st.text_input("Activity Name")

    duration = st.number_input(
        "Duration (minutes)",
        min_value=1,
        max_value=600,
        value=60
    )

    exertion = st.selectbox(
        "Exertion Level",
        ["Low", "Moderate", "High"]
    )

    submitted = st.form_submit_button("Save Activity")

    if submitted:
        if activity_name.strip():
            model.update_activity(
                activity_name,
                duration,
                exertion
            )
            st.success("Activity saved successfully!")
        else:
            st.warning("Please enter an activity name.")

# Display saved activity
st.divider()
st.subheader("Last Saved Activity")

activity = model.get_activity()

st.write("Activity:", activity["name"])
st.write("Duration:", activity["duration"], "minutes")
st.write("Exertion:", activity["exertion"])
