
import streamlit as st

from main import track_choice
from search_engine import search_balance, balance_data
from sequence_logic import analyze_log
from structures import UserSession
from models import BalanceIQModel

st.set_page_config(
    page_title="BalanceIQ",
    page_icon="🧠",
    layout="wide"
)
# CONNECT TO JSON DATABASE
database = BalanceIQModel()

# LOAD DATA FROM JSON DATABASE

if "scores" not in st.session_state:
    st.session_state.scores = database.get_scores().copy()

if "activity" not in st.session_state:
    saved_activity = database.get_activity()

    st.session_state.activity = UserSession(
        saved_activity["name"],
        saved_activity["duration"],
        saved_activity["exertion"]
    )


# SIDEBAR
st.sidebar.title("🧠 BalanceIQ")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Track Choices", "Search Student", "Analyze Daily Log"]
)


# DASHBOARD

# DASHBOARD
if page == "Dashboard":

    st.title("🧠 BalanceIQ")
    st.subheader("The Aha! Moment: The Hidden Truth")

    st.write(
        "Discover how academic choices affect your academic success "
        "and personal well-being."
    )

    st.divider()

    scores = st.session_state.scores

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📚 THE EXPECTATION")

        st.warning(
            "Studying more means better grades and greater academic success."
        )

        st.metric("Expected Academic Performance", "90%")
        st.progress(0.90)

        st.caption("The belief: More studying always means more success.")

    with col2:
        st.subheader("⚠️ THE HIDDEN TRUTH")

        st.error(
            "Too much academic pressure can reduce sleep, free time, "
            "motivation, and personal well-being."
        )

        st.metric(
            "Personal Balance",
            f"{scores['balance_score']}%",
            delta=f"{scores['balance_score'] - 65}%",
            delta_color="normal"
        )

        st.progress(scores["balance_score"] / 100)

        st.caption("The reality: Academic success needs balance.")

    st.divider()

    st.subheader("📊 Your Current Academic Scores")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Academic Pressure",
        f"{scores['academic_pressure']}%"
    )

    col2.metric(
        "Focus Score",
        f"{scores['focus_score']}%"
    )

    col3.metric(
        "Balance Score",
        f"{scores['balance_score']}%"
    )

    st.divider()

    st.subheader("💡 THE BIG REALIZATION")

    st.success(
        "Getting good grades should not mean sacrificing your "
        "sleep, free time, and mental well-being. Balance is also success."
    )
    if st.button("📊 See How My Choices Affect My Balance"):
        result = track_choice("1", st.session_state.scores)
        st.session_state.scores = result["scores"]
        database.update_scores(result["scores"])
        st.rerun()


# TRACK CHOICES

elif page == "Track Choices":

    st.title("📊 Track Your Academic Choices")

    st.write("Choose an action to see how it affects your scores.")

    # INCREASE STUDY WORKLOAD
    if st.button("📚 Increase Study Workload"):

        result = track_choice("1", st.session_state.scores)

        st.session_state.scores = result["scores"]
        database.update_scores(result["scores"])
        st.success(result["message"])
        st.rerun()

    # TAKE A STRUCTURED BREAK
    if st.button("🌿 Take a Structured Break"):

        result = track_choice("2", st.session_state.scores)

        st.session_state.scores = result["scores"]
        database.update_scores(result["scores"])
        st.success(result["message"])
        st.rerun()

    scores = st.session_state.scores

    st.divider()
    st.subheader("Updated Scores")

    col1, col2, col3 = st.columns(3)

    col1.metric("Academic Pressure", f"{scores['academic_pressure']}%")
    col2.metric("Focus Score", f"{scores['focus_score']}%")
    col3.metric("Balance Score", f"{scores['balance_score']}%")

    st.progress(scores["balance_score"] / 100)

    if scores["balance_score"] < 60:
        st.warning("Your current routine may be difficult to sustain.")
    elif scores["academic_pressure"] > 60:
        st.info("Your academic pressure is increasing.")
    else:
        st.success("Your routine is maintaining a good balance.")

    st.divider()

    # RECORD AN ACTIVITY
    st.subheader("Record an Activity")

    activity = st.text_input("Activity name")

    duration = st.number_input(
        "Duration in minutes",
        min_value=1,
        max_value=600,
        value=30
    )

    exertion = st.selectbox(
        "Exertion Level",
        ["Low", "Moderate", "High"]
    )

    if st.button("Save Activity"):

        if activity.strip():

            st.session_state.activity = UserSession(
                activity, int(duration), exertion
            )

            database.update_activity(
                activity,
                int(duration),
                exertion
            )

            st.success("Activity saved successfully!")

        else:
            st.warning("Please enter an activity.")
# SEARCH STUDENT
elif page == "Search Student":

    st.title("🔎 Search Student")

    query = st.text_input("Enter student name")

    if st.button("Search"):

        if query.strip():

            results = search_balance(balance_data, query)

            if results:

                for student, information in results.items():

                    st.success(f"Student found: {student}")

                    st.metric(
                        "Focus Score",
                        f"{information['focus_score']}%"
                    )

                    st.write(
                        f"Stress Level: {information['stress_level']}"
                    )

                    st.subheader("Weekly Focus Logs")
                    st.table(information["weekly_logs"])

            else:
                st.warning("Student not found.")

        else:
            st.warning("Enter a student name.")