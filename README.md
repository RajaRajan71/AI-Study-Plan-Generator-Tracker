# AI Study Plan Generator & Tracker 📚

### 🚀 Deployed Application
**Live Link:** https://huggingface.co/spaces/rajann/study.planner

---

## 📖 Project Overview
Learners often struggle to structure their study time and maintain consistency. This **AI-powered Study Plan Generator & Tracker** solves this by creating personalized, time-bound roadmaps based on a user's specific goals and availability. It moves beyond static lists by allowing users to track their progress in real-time.

## 🧠 Plan Generation Logic
The application utilizes the `google/flan-t5-base` Large Language Model (LLM) to act as a personal tutor.
* **Input Processing:** It takes the user's Learning Goal, Target Duration, and Daily Availability.
* **Dynamic Prompting:** These inputs are converted into a structured prompt that instructs the AI to generate a chronological task list.
* **Topic Sequencing:** The model ensures foundational topics are introduced before advanced concepts to create a realistic learning curve.

## 📊 Progress Tracking Mechanism
The tracking system is designed to provide immediate feedback and maintain accountability.
* **Live Calculation:** Progress is calculated using the following formula:
  $$\text{Total Progress} = \left( \frac{\text{Completed Daily Tasks}}{\text{Total Days in Plan}} \right) \times 100$$
* **Real-time Metrics:** As users check off tasks, the "Remaining Days" and "Status" metrics update instantly to reflect their current standing.
* **Data Persistence:** The app uses a `study_tasks.json` file to store user progress. This ensures that when a learner returns to the app, their checked tasks and progress are automatically reloaded.

## 🛤 Sample User Journey
1. **Goal Setup:** A user enters "Python for Data Science" with a 30-day target and 2 hours of daily availability.
2. **AI Generation:** The AI generates a 30-day roadmap with specific milestones for each week.
3. **Daily Execution:** The user completes the Day 1 task and marks it as finished.
4. **Instant Feedback:** The dashboard updates to show **3% Progress** and **29 Days Remaining**, with a status of **"On Track."**

---

## 🛠 Tech Stack
* **Backend:** Python
* **Frontend:** Streamlit
* **AI Model:** Hugging Face `google/flan-t5-base`
* **Storage:** JSON
* **Deployment:** Hugging Face Spaces
