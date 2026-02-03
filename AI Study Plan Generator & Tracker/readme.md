# AI Study Plan Generator & Tracker 📚

### 🚀 Deployed URL
[Insert your Hugging Face Space URL here]

### 📖 Project Overview
An intelligent AI-powered system designed to help learners plan, execute, and track their study journey. 

### 🧠 Plan Generation Logic
The application uses the `google/flan-t5-base` LLM to translate a learning goal and time constraints into a structured daily roadmap.

### 📊 Progress Tracking Mechanism
Progress is calculated as a percentage of completed daily tasks relative to the total planned duration. Data is persisted via JSON for continuous tracking.

### 🛤 Sample User Journey
1. User enters "Python for Data Analysis" for 30 days.
2. AI generates a custom daily task list.
3. User marks tasks as completed each day.
4. Dashboard updates Completion %, Remaining Days, and Status.