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


Activate it on Windows PowerShell:

powershell
.\venv\Scripts\Activate.ps1

3. Install Dependencies
bash
pip install Flask


If your project has a requirements.txt file, you can install all listed dependencies with:

bash
pip install -r requirements.txt

4. Run the Application

Run the following command from the project directory:

bash
python app.py


The application initializes the SQLite database when started.

5. Open in Your Browser

Visit:

text
http://127.0.0.1:5000/


Create an account or log in to access the resume generator.

💡 How It Works
Register: Create an account with a username and password.
Log In: Authenticate to access the resume builder.
Enter Details: Add personal information, career objectives, education, experience, skills, and projects.
Get Recommendations: Receive suggested resume objectives, skills, and career-specific tips.
Save Resume Data: Submit resume information to the Flask backend, which stores it in the SQLite database.
Manage Your Session: Log out when finished.
🔗 Application Routes
Route	Method	Description
/	GET	Home page
/signup	GET, POST	User registration
/login	GET, POST	User authentication
/logout	GET	End the current session
/generator	GET	Access the resume builder
/save_data	POST	Save resume information
/recommend	POST	Get career-based recommendations
/users	GET	Display the user list
🗄️ Database Design

The application uses SQLite with two primary tables:

users: Stores user IDs, usernames, passwords, and account creation timestamps.
resumes: Stores resume information associated with a user, including contact details, education, work experience, skills, projects, template selection, and photo information.

Complex resume fields are serialized as JSON strings before being stored in the database.

🔮 Future Enhancements
Integrate a real AI language model for personalized resume suggestions.
Add multiple resume templates and live previews.
Export completed resumes as PDF files.
Add resume editing, retrieval, and deletion features.
Improve password security using password hashing.
Add form validation and stronger authentication controls.
Add job-description matching and ATS-friendly resume analysis.
Deploy the application to a cloud hosting platform.
🔐 Security Notes

This project is intended for learning and development. Before deploying it publicly:

Replace the hardcoded Flask secret key with an environment variable.
Hash passwords instead of storing them as plain text.
Disable Flask debug mode in production.
Add input validation and authorization checks to all relevant routes.
Avoid committing databases containing personal or sensitive user information.
👩‍💻 Author

Mrunal

GitHub: @mrunal0701

📄 License

This project is available for educational and personal development purposes. Add a license file if you intend to specify permissions for reuse and distribution.
