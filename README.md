My Personal Book Collection App 📚
A web application built with Streamlit and Python to manage and track your personal book collection. This project demonstrates Object-Oriented Programming (OOP) principles, data persistence with SQLite, and a fully interactive web interface for CRUD (Create, Read, Update, Delete) operations.

✨ Features
Add New Books: Easily add books to your collection through a simple form.
View & Filter: See your entire collection and filter it by reading status or genre.
Edit & Delete: Full CRUD functionality to update book details or remove them from your collection.
Reading Statistics: Visualize your reading habits with a pie chart showing the status of your books.
Recommendations: Get book recommendations based on your most-read genres.
Persistent Storage: All data is securely saved in an SQLite database.

🛠️ Technology Stack
Backend: Python, Object-Oriented Programming (OOP)
Frontend: Streamlit
Database: SQLite
Data Manipulation: Pandas
Visualization: Matplotlib

🚀 Running the Application
There are two ways to run this application:

Option 1: Via Streamlit Cloud (Easiest)
The application is deployed and publicly accessible. No installation is required.

👉 Access the live app here https://koleksibuku-app.streamlit.app/

Option 2: Running Locally
If you want to run the application on your own machine, follow these steps.

1. Clone the Repository


git clone <your-repository-url>
cd <repository-directory-name>

2. Create a Virtual Environment & Install Dependencies
It's recommended to use a virtual environment to manage project dependencies.


# Create a virtual environment
python -m venv venv

# Activate it (Windows)
.\venv\Scripts\activate

# Activate it (macOS/Linux)
source venv/bin/activate

# Install the required libraries
pip install streamlit pandas matplotlib

3. Set Up the Database
This command will create the data_buku.db file and populate it with some initial example data. You only need to run this once.
Bash
python setup_db.py

4. Run the Streamlit App
Now, you can start the application.
streamlit run streamlit_app.py
Your web browser should automatically open with the application running.
