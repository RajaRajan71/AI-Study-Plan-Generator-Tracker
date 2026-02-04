import streamlit as st
from transformers import pipeline
import json
import os
import re

# --- PAGE SETUP ---
st.set_page_config(page_title="AI Study Planner", page_icon="📚", layout="wide")

DATA_FILE = "study_tasks.json"

@st.cache_resource
def load_ai():
    # 'text-generation' is the valid task name in Transformers 5.0.0 logs
    return pipeline("text-generation", model="google/flan-t5-small", trust_remote_code=True)

ai_model = load_ai()

# --- DATA PERSISTENCE ---
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                pass
    return {"goal": "", "days": 7, "tasks": [], "weekly_plan": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

user_data = load_data()

# --- SIDEBAR ---
with st.sidebar:
    st.header("🎯 Learning Goal")
    goal_input = st.text_input("What are you learning?", value=user_data["goal"], placeholder="e.g. Python")
    duration = st.number_input("Duration (Days)", min_value=1, max_value=30, value=user_data.get("days", 7))
    
    if st.button("🚀 Generate Plan"):
        # We use a structured prompt to help the 'text-generation' task
        prompt = f"Objective: Create a study plan for {goal_input}. Duration: {duration} days. Format: Day 1: Task, Day 2: Task."
        with st.spinner("AI is thinking..."):
            # max_new_tokens ensures the AI doesn't cut off halfway
            result = ai_model(prompt, max_new_tokens=150, truncation=True)[0]["generated_text"]
            
            # Clean the output to remove the prompt itself if it's repeated
            clean_result = result.replace(prompt, "").strip()
            
            # Split by "Day X:" to create checkboxes
            parts = re.split(r'Day \d+[:\-]', clean_result)
            tasks = []
            day_num = 1
            for p in parts:
                task_text = p.strip()
                if len(task_text) > 2 and day_num <= duration:
                    tasks.append({"day": day_num, "task": task_text, "done": False})
                    day_num += 1
            
            user_data = {"goal": goal_input, "days": duration, "tasks": tasks, "weekly_plan": [clean_result]}
            save_data(user_data)
            st.rerun()

# --- MAIN DASHBOARD ---
if user_data["tasks"]:
    st.title(f"📖 {user_data['goal']} Tracker")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("✅ Checklist")
        for i, t in enumerate(user_data["tasks"]):
            user_data["tasks"][i]["done"] = st.checkbox(f"Day {t['day']}: {t['task']}", value=t["done"], key=f"t_{i}")
        
        if st.button("💾 Save Progress"):
            save_data(user_data)
            st.success("Progress saved!")

    with col2:
        st.subheader("📊 Stats")
        total = len(user_data["tasks"])
        completed = sum(1 for t in user_data["tasks"] if t["done"])
        percent = int((completed / total) * 100) if total > 0 else 0
        st.metric("Completion", f"{percent}%")
        st.progress(percent / 100)
else:
    st.info("Enter your goal in the sidebar and click 'Generate Plan'.")
