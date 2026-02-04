import streamlit as st
from transformers import pipeline
import json
import os
import re

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Study Planner", page_icon="📚", layout="wide")

DATA_FILE = "study_tasks.json"

@st.cache_resource
def load_ai():
    # Using 'summarization' task to avoid the RuntimeError on cloud servers
    return pipeline("summarization", model="google/flan-t5-small") 

ai_model = load_ai()

# --- DATA PERSISTENCE ---
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                pass
    return {"goal": "", "days": 30, "tasks": [], "weekly_plan": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

user_data = load_data()

# --- SIDEBAR ---
with st.sidebar:
    st.header("🎯 Learning Goal")
    goal_input = st.text_input("What do you want to learn?", value=user_data["goal"])
    duration = st.number_input("Duration (Days)", min_value=1, max_value=30, value=user_data.get("days", 7))
    
    if st.button("🚀 Generate AI Plan"):
        prompt = f"Create a study plan for {goal_input} for {duration} days. List Day 1: Task, Day 2: Task."
        with st.spinner("AI is thinking..."):
            result = ai_model(prompt, max_new_tokens=100)[0]["generated_text"]
            # Logic to extract days
            daily = re.findall(r"Day\s*\d+.*", result)
            tasks = []
            for i, d in enumerate(daily[:duration]):
                tasks.append({"day": i + 1, "task": d, "done": False})
            
            user_data = {"goal": goal_input, "days": duration, "tasks": tasks, "weekly_plan": [result]}
            save_data(user_data)
            st.rerun()

# --- MAIN UI ---
if user_data["tasks"]:
    st.title(f"📖 Tracker: {user_data['goal']}")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("✅ Tasks")
        for i, t in enumerate(user_data["tasks"]):
            user_data["tasks"][i]["done"] = st.checkbox(f"{t['task']}", value=t["done"], key=f"task_{i}")
        
        if st.button("💾 Save Progress"):
            save_data(user_data)
            st.success("Progress Saved!")

    with col2:
        st.subheader("📊 Progress")
        total = len(user_data["tasks"])
        done = sum(t["done"] for t in user_data["tasks"])
        progress = int((done / total) * 100) if total > 0 else 0
        st.metric("Completion", f"{progress}%")
        st.progress(progress / 100)
else:
    st.info("Enter a goal in the sidebar to generate your plan!")
