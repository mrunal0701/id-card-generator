AI Resume Builder

An intelligent, web-based Resume Builder application built with Python, Flask, and SQLite. This project helps users create professional resumes by entering their personal details, education, work experience, skills, and projects. It also provides domain-based resume recommendations to help users improve their resume content.

🚀 Features
User Authentication: Sign up, log in, and log out functionality.
Resume Generator: Create resumes by entering personal and professional information.
Database Integration: Store user accounts and resume data using SQLite.
AI-Style Recommendations: Get suggested resume objectives, skills, and tips based on your career domain.
Multiple Career Domains: Includes recommendations for Software Engineers, Data Scientists, and Marketing Specialists.
Personalized Content: Save contact details, education, work experience, projects, skills, and profile photo information.
Session Management: Restrict access to the resume generator to logged-in users.
Responsive Web Interface: Uses HTML templates to provide a browser-based experience.
🛠️ Technologies Used
Backend: Python, Flask
Database: SQLite
Frontend: HTML, CSS, JavaScript
Data Handling: Python JSON module
Version Control: Git and GitHub
📂 Project Structure
text
id-card-generator/
│
├── app.py                  # Main Flask application
├── resume_builder.db       # SQLite database (generated locally)
├── templates/
│   ├── index.html          # Home page
│   ├── login.html          # Login page
│   ├── signup.html         # Registration page
│   ├── generator.html      # Resume builder interface
│   └── user_list.html      # User list page
│
├── static/                 # CSS, JavaScript, images, if present
├── requirements.txt        # Python dependencies, if present
└── README.md               # Project documentation


Note: The filenames and folders above are illustrative. Adjust them to match your actual project structure.

⚙️ Installation and Setup
1. Clone the Repository
bash
git clone https://github.com/mrunal0701/id-card-generator.git
cd id-card-generator

2. Create a Virtual Environment (Recommended)
bash
python -m venv venv


Activate it on
