
import streamlit as st
import requests

st.set_page_config(page_title="Therapist Office", layout="wide")

st.sidebar.title("Therapist Office")
view = st.sidebar.radio("Menu", ["Messages", "Appointments", "Medication", "Zoom Meetings"])

if view == "Messages":
    st.header("Open Mic")
    st.write("**Topic:** Movie Night / Open Mic")
    st.write("**Time:** 8:00 PM")
    st.write("**Hospital:** Greenwood Psychiatric")
    st.button("Join Zoom")

elif view == "Appointments":
    st.header("Appointments")
    res = requests.get("http://localhost:5000/appointments")
    if res.status_code == 200:
        for a in res.json():
            st.write(f"- **{a['date']}** at {a['time']} ({a['type']})")

elif view == "Medication":
    st.header("Parent/Guardian Profile")
    g = requests.get("http://localhost:5000/guardian").json()
    st.write("**Vitals:**", g["vitals"])
    st.write("**Medication:**")
    for m in g["medication"]:
        st.write(f"- {m['name']} {m['dose']}")
    st.write("**Hospital:**", g["hospital"])
    st.button("Request a Visit")

elif view == "Zoom Meetings":
    e = requests.get("http://localhost:5000/events").json()
    st.header("Zoom Event")
    st.write(f"**{e['topic']}** at {e['time']}")
    st.write("Hosted by", e["hospital"])
    st.markdown(f"[Join Event]({e['link']})")
