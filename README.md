📊 LangChain SQL Agent — Chat With Your Database

An interactive Streamlit application that allows users to chat directly with a SQL database—either SQLite or MySQL—using LangChain, Groq LLaMA 3.1, and the SQL Agent Toolkit.

You can ask natural language questions like:

"Show me all students who scored above 80."
"What is the average age of students?"

The agent automatically converts your question into SQL, runs it, and explains the results.

🚀 Features

✔ Chat with SQLite (student.db)
✔ Connect to your own MySQL database
✔ GROQ-powered LLaMA 3.1 for reasoning
✔ Uses LangChain SQLDatabaseToolkit
✔ Fully interactive Streamlit UI
✔ Auto–SQL generation + result explanation
✔ Message history like an AI chatbot

▶️ How to Run
1️⃣ Install dependencies
pip install -r requirements.txt

2️⃣ Add your .env file

Create .env:

GROQ_API_KEY=your_real_key_here

3️⃣ Start the app
streamlit run app.py

🖥 How It Works

User selects SQLite or MySQL

LangChain loads the database using SQLDatabase

SQL Agent + Groq LLaMA 3.1 generates SQL queries

Results appear with explanations

🧑‍💻 Author

Shehjad Patel
AI Engineer | LangChain | LLM Apps | Python
GitHub: https://github.com/Shehjad2019