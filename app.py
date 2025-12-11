import streamlit as st
from pathlib import Path

# LangChain
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit, create_sql_agent
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler

from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq


# -------------------------------------------------------
# STREAMLIT UI
# -------------------------------------------------------
st.set_page_config(page_title="LangChain: Chat with SQL DB")
st.title("LangChain: Chat with SQL DB")

LOCALDB = "USE_LOCALDB"
MYSQL = "USE_MYSQL"

radio_opt = [
    "Use SQLite 3 Database - student.db",
    "Connect to your SQL Database"
]

selected_opt = st.sidebar.radio("Choose the DB you want to chat with:", radio_opt)

# ---------------- MySQL UI ----------------
if selected_opt == radio_opt[1]:
    db_uri = MYSQL
    mysql_host = st.sidebar.text_input("MySQL Host (default: localhost)", value="localhost")
    mysql_user = st.sidebar.text_input("MySQL User (e.g., root)", value="root")
    mysql_password = st.sidebar.text_input("MySQL Password", type="password")
    mysql_db = st.sidebar.text_input("MySQL Database (e.g., studentdb)")
else:
    db_uri = LOCALDB

api_key = st.sidebar.text_input("GROQ API Key", type="password")


# -------------------------------------------------------
# DATABASE CONFIGURATION FUNCTION
# -------------------------------------------------------
@st.cache_resource(ttl=7200)
def configure_db(db_uri, mysql_host=None, mysql_user=None, mysql_password=None, mysql_db=None):

    # --- SQLITE ----------------
    if db_uri == LOCALDB:
        db_file = (Path(__file__).parent / "student.db").absolute()
        creator = lambda: sqlite3.connect(f"{db_file}")

        return SQLDatabase(create_engine("sqlite:///", creator=creator))

    # --- MYSQL ----------------
    elif db_uri == MYSQL:

        if not (mysql_host and mysql_user and mysql_password and mysql_db):
            st.error("Please fill all MySQL details.")
            st.stop()

        # Build correct engine URL
        connection_url = f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"

        return SQLDatabase(
            create_engine(connection_url)
        )


# -------------------------------------------------------
# INITIALIZE DATABASE
# -------------------------------------------------------
if db_uri == MYSQL:
    db = configure_db(db_uri, mysql_host, mysql_user, mysql_password, mysql_db)
else:
    db = configure_db(db_uri)

st.success("Database connected successfully!")


# -------------------------------------------------------
# LLM SETUP
# -------------------------------------------------------
if not api_key:
    st.warning("Enter your GROQ API Key to continue.")
    st.stop()

llm = ChatGroq(
    groq_api_key=api_key,
    model_name="llama-3.1-8b-instant",
    streaming=True
)

st.success("LLM loaded successfully!")


# -------------------------------------------------------
# TOOLKIT + AGENT
# -------------------------------------------------------
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
)


# -------------------------------------------------------
# CHAT UI
# -------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


# USER QUERY
user_query = st.chat_input("Ask anything from your database...")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        stream_handler = StreamlitCallbackHandler(st.container())
        response = agent.run(user_query, callbacks=[stream_handler])
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)
