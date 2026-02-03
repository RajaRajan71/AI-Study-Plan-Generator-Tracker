import streamlit as st
from transformers import pipeline
import json
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Study Planner & Tracker", page_icon="📚", layout="wide")

DATA_FILE = "study_tasks.json"

@st.cache_resource
def load_ai():
    # Model used for plan generation
    return pipeline("text2text-generation", model="google/flan-t5-base")

ai_model = load_ai()

# --- DATA STORAGE LOGIC ---
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                data = json.load(f)
                # Safety check: Ensure days is at least 1
                if data.get("days", 0) < 1:
                    data["days"] = 30
                return data
            except:
                pass
    return {"goal": "", "days": 30, "tasks": [], "weekly_plan": ""}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

user_data = load_data()

# --- SIDEBAR: INPUTS ---
with st.sidebar:
    st.header("🎯 Define Goal")
    goal_input = st.text_input("Learning Goal", value=user_data["goal"], placeholder="e.g. Python basics")
    
    # Safe duration input
    saved_days = user_data.get("days", 30)
    duration = st.number_input("Target duration (days)", min_value=1, max_value=365, value=max(1, saved_days))
    hours = st.slider("Daily study hours", 1, 12, 2)
    
    if st.button("🚀 Generate AI Plan"):
        prompt = f"Create a {duration}-day study plan for {goal_input} ({hours} hours daily). Include Weekly summary + Day X: Task."
        with st.spinner("AI is generating..."):
            raw_text = ai_model(prompt, max_new_tokens=512)[0]['generated_text']
            tasks = [{"day": i+1, "task": t.strip(), "done": False} 
                     for i, t in enumerate(raw_text.split('.')[:duration]) if t.strip()]
            user_data = {"goal": goal_input, "days": duration, "tasks": tasks, "weekly_plan": f"Focus on {goal_input} fundamentals."}
            save_data(user_data)
            st.rerun()

# --- MAIN TRACKER ---
if user_data["tasks"]:
    st.title(f"📖 Tracker: {user_data['goal']}")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("✅ Tasks")
        for i, item in enumerate(user_data["tasks"]):
            user_data["tasks"][i]["done"] = st.checkbox(f"Day {item['day']}: {item['task']}", value=item['done'], key=f"c_{i}")
        if st.button("💾 Save Progress"):
            save_data(user_data)
            st.success("Synced!")
    with col2:
        st.subheader("📊 Status")
        total = len(user_data["tasks"])
        done = sum(1 for t in user_data["tasks"] if t["done"])
        pct = int((done / total) * 100) if total > 0 else 0
        st.metric("Completion", f"{pct}%")
        st.write(f"**Remaining Days:** {total - done}")
        st.write(f"**Status:** {'On Track' if pct > 0 else 'Ready'}")
        st.progress(pct / 100)
        st.info(user_data.get("weekly_plan", ""))
else:
    st.info("Define your goal in the sidebar to start.")
