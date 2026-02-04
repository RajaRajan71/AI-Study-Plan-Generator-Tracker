import streamlit as st
from transformers import pipeline
import json
import os
import re

# --- PAGE SETUP ---
st.set_page_config(page_title="AI Study Planner", page_icon="📚", layout="wide")

# This file stores your progress locally on the server
DATA_FILE = "study_tasks.json"

@st.cache_resource
def load_ai():
    # Changed to 'text2text-generation' to fix the KeyError
    return pipeline("text2text-generation", model="google/flan-t5-small")

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
    goal_input = st.text_input("What are you learning?", value=user_data["goal"], placeholder="e.g. Python Basics")
    duration = st.number_input("Duration (Days)", min_value=1, max_value=30, value=user_data.get("days", 7))
    
    if st.button("🚀 Generate Plan"):
        # Explicit instruction for the T5 model
        prompt = f"generate a study plan: {goal_input} for {duration} days. List Day 1, Day 2, etc."
        with st.spinner("AI is crafting your roadmap..."):
            # Using the text2text generation pipeline
            result = ai_model(prompt, max_new_tokens=150)[0]["generated_text"]
            
            # Simple logic to turn generated text into a checklist
            sentences = re.split(r'Day \d+:|Day \d+ -', result)
            tasks = []
            day_count = 1
            for s in sentences:
                clean_s = s.strip()
                if len(clean_s) > 3 and day_count <= duration:
                    tasks.append({"day": day_count, "task": clean_s, "done": False})
                    day_count += 1
            
            user_data = {"goal": goal_input, "days": duration, "tasks": tasks, "weekly_plan": [result]}
            save_data(user_data)
            st.rerun()

# --- MAIN DASHBOARD ---
if user_data["tasks"]:
    st.title(f"📖 Study Tracker: {user_data['goal']}")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("✅ Daily Roadmap")
        for i, t in enumerate(user_data["tasks"]):
            user_data["tasks"][i]["done"] = st.checkbox(f"Day {t['day']}: {t['task']}", value=t["done"], key=f"t_{i}")
        
        if st.button("💾 Save Progress"):
            save_data(user_data)
            st.success("Progress saved!")

    with col2:
        st.subheader("📊 Statistics")
        total = len(user_data["tasks"])
        completed = sum(1 for t in user_data["tasks"] if t["done"])
        percent = int((completed / total) * 100) if total > 0 else 0
        
        st.metric("Completion Rate", f"{percent}%")
        st.progress(percent / 100)
        
        if percent == 100:
            st.balloons()
            st.success("Goal Achieved! 🏆")
else:
    st.info("👋 Welcome! Enter your goal in the sidebar and click 'Generate Plan' to start.")
