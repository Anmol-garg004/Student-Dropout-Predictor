import pandas as pd
import numpy as np
import gradio as gr
from fastapi import FastAPI

# -----------------------------
# Default Dataset
# -----------------------------
def generate_sample_data():
    data = {
        "student_id": list(range(1, 21)),
        "name": ["Arjun","Aanya","Rohan","Diya","Aditya","Anika","Karan","Meera","Vikram","Shruti",
                 "Krishna","Trisha","Sanya","Kabir","Neha","Aryan","Ishita","Manav","Riya","Lakshmi"],
        "gender": ["Male","Female","Male","Female","Male","Female","Male","Female","Male","Female",
                   "Male","Female","Female","Male","Female","Male","Female","Male","Female","Female"],
        "age": np.random.randint(16, 19, 20),
        "grade": np.random.randint(45, 100, 20),
        "attendance_rate": np.round(np.random.uniform(0.5, 1.0, 20), 2),
        "previous_failures": np.random.randint(0, 3, 20),
        "study_hours_per_week": np.random.randint(2, 20, 20),
        "parent_phone": [str(9876500000 + i) for i in range(20)]
    }
    return pd.DataFrame(data)

# -----------------------------
# Dropout Risk Prediction Logic
# -----------------------------
def predict_dropout(df):
    risk_scores = []
    for _, row in df.iterrows():
        risk = 0
        if row["grade"] < 60:
            risk += 0.4
        if row["attendance_rate"] < 0.7:
            risk += 0.3
        if row["previous_failures"] > 0:
            risk += 0.2
        if row["study_hours_per_week"] < 5:
            risk += 0.1
        risk_scores.append(risk)
    df["dropout_risk"] = np.round(risk_scores, 2)
    df["risk_level"] = df["dropout_risk"].apply(
        lambda x: "High" if x >= 0.6 else ("Medium" if x >= 0.3 else "Low")
    )
    return df

last_predictions = predict_dropout(generate_sample_data())
student_progress = {}

# -----------------------------
# Skill Rebuilder AI
# -----------------------------
skill_resources = {
    "Math": {
        "Algebra": "https://www.khanacademy.org/math/algebra",
        "Trigonometry": "https://www.khanacademy.org/math/trigonometry",
        "Geometry": "https://www.khanacademy.org/math/geometry"
    },
    "Science": {
        "Organic Chemistry": "https://nptel.ac.in/courses/104/106/104106125/",
        "Physics Mechanics": "https://www.youtube.com/watch?v=kKKM8Y-u7ds",
        "Biology Basics": "https://ncert.nic.in/textbook.php?lebo1=1-3"
    },
    "English": {
        "Grammar": "https://www.englishgrammar101.com/",
        "Writing Skills": "https://www.coursera.org/learn/academic-english-writing",
        "Reading Comprehension": "https://www.khanacademy.org/test-prep/sat/reading-writing"
    }
}

def skill_rebuilder(student_id):
    global last_predictions, student_progress
    student_row = last_predictions[last_predictions['student_id'] == student_id]
    
    if student_row.empty:
        return "❌ Student ID not found."
    
    student = student_row.iloc[0]
    recommendations = []
    
    if student['grade'] < 60:
        recommendations.append(("Math - Algebra Basics", skill_resources["Math"]["Algebra"]))
        recommendations.append(("English - Writing Skills", skill_resources["English"]["Writing Skills"]))
    elif 60 <= student['grade'] < 75:
        recommendations.append(("Math - Trigonometry Practice", skill_resources["Math"]["Trigonometry"]))
        recommendations.append(("Science - Organic Chemistry", skill_resources["Science"]["Organic Chemistry"]))
    else:
        recommendations.append(("Advanced Math - Geometry", skill_resources["Math"]["Geometry"]))
        recommendations.append(("English - Reading Comprehension", skill_resources["English"]["Reading Comprehension"]))
    
    if student['attendance_rate'] < 0.7:
        recommendations.append(("Motivation & Time Management", "https://www.youtube.com/watch?v=4T3iY8j4Zs4"))
    
    if student['previous_failures'] > 1:
        recommendations.append(("Extra Remedial Classes Portal", "https://nptel.ac.in/"))
    
    if student['study_hours_per_week'] < 5:
        recommendations.append(("Study Habits Improvement", "https://www.youtube.com/watch?v=QVCa0j5gKg0"))
    
    completed = student_progress.get(student_id, 0)
    badge = "🏅 Beginner" if completed < 2 else "🥈 Intermediate" if completed < 4 else "🥇 Pro"
    
    response = f"🎯 **Skill Rebuilder Plan for {student['name']} (ID {int(student_id)})**\n\n"
    for i, (topic, link) in enumerate(recommendations, 1):
        response += f"{i}. 📘 {topic} → [Start Now]({link})\n"
    
    response += f"\n🏆 Progress: {completed} modules completed → Current Badge: {badge}\n"
    response += "✅ Complete 2 more modules to level up!"
    return response

def mark_module_completed(student_id):
    global student_progress
    if student_id not in student_progress:
        student_progress[student_id] = 0
    student_progress[student_id] += 1
    return f"✅ Progress updated for Student {student_id}! Total Completed: {student_progress[student_id]}"

# -----------------------------
# Custom CSS for Website Look
# -----------------------------
custom_css = """
/* -------------------------
   CSS Variables (Light + Dark Mode)
------------------------- */
:root {
    --bg-color: #f9fafb;
    --text-color: #1f2937;
    --heading-color: #111827;
    --card-bg: #ffffff;
    --primary: #4f46e5;
    --primary-hover: #3730a3;
    --secondary: #6366f1;
    --accent: #3b82f6;
    --border-radius: 12px;
    --shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}
[data-theme="dark"] {
    --bg-color: #111827;
    --text-color: #f3f4f6;
    --heading-color: #ffffff;
    --card-bg: #1f2937;
    --primary: #6366f1;
    --primary-hover: #818cf8;
    --secondary: #4f46e5;
    --accent: #3b82f6;
    --shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
}

/* -------------------------
   Global Styles
------------------------- */
#root {
    background: var(--bg-color);
    font-family: 'Segoe UI', Tahoma, sans-serif;
    color: var(--text-color);
    min-height: 100vh;
    transition: background 0.3s ease, color 0.3s ease;
}
.gradio-container {
    max-width: 1100px !important;
    margin: auto;
    padding: 15px;
}
h1, h2, h3 {
    font-weight: 700 !important;
    color: var(--heading-color) !important;
    margin-bottom: 10px;
}
p, label {
    font-size: 15px;
    line-height: 1.6;
}

/* -------------------------
   Navigation Bar
------------------------- */
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: var(--primary);
    color: white;
    padding: 12px 20px;
    border-radius: var(--border-radius);
    box-shadow: var(--shadow);
}
.navbar a {
    color: white;
    text-decoration: none;
    margin: 0 10px;
    font-weight: 500;
    transition: color 0.3s;
}
.navbar a:hover {
    color: var(--accent);
}

/* -------------------------
   Cards & Panels
------------------------- */
.gr-block, .gr-tab, .gr-panel {
    background: var(--card-bg) !important;
    border-radius: var(--border-radius) !important;
    padding: 20px !important;
    box-shadow: var(--shadow);
    margin-top: 15px !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.gr-block:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 14px rgba(0,0,0,0.12);
}

/* -------------------------
   Buttons
------------------------- */
.gr-button {
    background: var(--primary) !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 10px 22px !important;
    font-weight: bold !important;
    transition: background 0.3s ease, transform 0.2s ease;
    box-shadow: var(--shadow);
}
.gr-button:hover {
    background: var(--primary-hover) !important;
    transform: translateY(-2px);
}
.gr-button:active {
    transform: scale(0.97);
}

/* -------------------------
   Forms & Inputs
------------------------- */
input, textarea, select {
    border: 1px solid #d1d5db !important;
    border-radius: 8px !important;
    padding: 10px !important;
    font-size: 14px;
    width: 100%;
    transition: border 0.3s, box-shadow 0.3s;
}
input:focus, textarea:focus, select:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.3);
    outline: none;
}
label {
    font-weight: 600;
    margin-bottom: 6px;
    display: inline-block;
}

/* -------------------------
   Tables
------------------------- */
table {
    border-collapse: collapse;
    width: 100%;
    background: var(--card-bg);
    border-radius: var(--border-radius);
    overflow: hidden;
    box-shadow: var(--shadow);
}
th, td {
    text-align: left;
    padding: 12px;
}
tr:nth-child(even) {
    background: #f3f4f6;
}
[data-theme="dark"] tr:nth-child(even) {
    background: #1e293b;
}

/* -------------------------
   Animations
------------------------- */
.fade-in {
    animation: fadeIn 0.6s ease-in-out;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(5px); }
    to { opacity: 1; transform: translateY(0); }
}

/* -------------------------
   Footer
------------------------- */
footer {
    text-align: center;
    margin-top: 40px;
    font-size: 14px;
    color: var(--text-color);
}


"""

# -----------------------------
# Gradio UI with Styling
# -----------------------------
with gr.Blocks() as demo:
    gr.HTML("<div style='text-align:center; padding:15px; background:#4f46e5; color:white; font-size:22px; font-weight:bold; border-radius:10px;'>🎓 AI-Powered Dropout Prediction & Skill Rebuilder System</div>")

    with gr.Tab("📊 Dashboard"):
        gr.Markdown("### Upload Student Data (CSV)")
        file_upload = gr.File(label="Upload CSV", file_types=[".csv"])
        student_table = gr.DataFrame(value=last_predictions, interactive=False)

        def load_csv(file):
            global last_predictions
            if file is None:
                df = generate_sample_data()
            else:
                df = pd.read_csv(file.name)
            last_predictions = predict_dropout(df)
            return last_predictions

        file_upload.change(load_csv, file_upload, student_table)

    with gr.Tab("🔮 Dropout Prediction"):
        gr.Markdown("### Enter Student Data for Prediction")
        with gr.Row():
            grade = gr.Number(label="Grade")
            attendance = gr.Number(label="Attendance Rate")
            failures = gr.Number(label="Previous Failures")
            study_hours = gr.Number(label="Study Hours/Week")
        predict_btn = gr.Button("Predict Dropout Risk")
        result = gr.Textbox(label="Prediction Result")
        
        def predict_single(grade, attendance, failures, study_hours):
            temp = pd.DataFrame([{
                "grade": grade,
                "attendance_rate": attendance,
                "previous_failures": failures,
                "study_hours_per_week": study_hours
            }])
            temp = predict_dropout(temp)
            return f"Risk Level: {temp['risk_level'][0]} (Score {temp['dropout_risk'][0]})"
        
        predict_btn.click(predict_single, [grade, attendance, failures, study_hours], result)

    with gr.Tab("🛠 Skill Rebuilder AI"):
        gr.Markdown("### Personalized Micro-Skill Recommendations")
        skill_student_id = gr.Number(label="Enter Student ID")
        skill_btn = gr.Button("🎯 Generate Plan")
        skill_output = gr.Markdown()
        skill_btn.click(fn=skill_rebuilder, inputs=skill_student_id, outputs=skill_output)
        
        gr.Markdown("### Update Progress")
        progress_id = gr.Number(label="Enter Student ID to Mark Module Completed")
        progress_btn = gr.Button("✅ Mark Completed")
        progress_output = gr.Textbox()
        progress_btn.click(fn=mark_module_completed, inputs=progress_id, outputs=progress_output)

    gr.HTML("<footer>© 2025 Student Success AI | Built with ❤️</footer>")

# Create the FastAPI app for Vercel
app = FastAPI()

# Mount the Gradio demo to the FastAPI app at the root
app = gr.mount_gradio_app(app, demo, path="/")

if __name__ == "__main__":
    demo.launch(css=custom_css)
