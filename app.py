import streamlit as st

control_rate = 0.6559
test_rate = 0.6929
lift = 0.0371

if __name__ == "__main__":
    st.title("Vanguard A/B Test Analysis")
    st.write("Experiment Results")
    
    st.metric(
        "Control Completion Rate",
        f"{control_rate:.2%}"
    )

    st.metric(
        "Test Completion Rate",
        f"{test_rate:.2%}"
    )

    st.metric(
        "Lift",
        f"{lift:.2%}"
    )