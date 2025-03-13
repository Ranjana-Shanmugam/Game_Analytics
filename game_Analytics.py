import streamlit as st
import mysql.connector
import pandas as pd
import re 

# Function to fetch data from Database 1 (sample)
def get_data(table_name):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="sample"
    )
    
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, connection)
    
    # Close the connection
    connection.close()
    
    return df

# Function to fetch data from Database 2 (compl)
def get_data_db2(table_name):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="compl"
    )
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, connection)
    
    # Close the connection
    connection.close()
    
    return df
#Function to fetch data from Database 3(doubles)
def get_data_db3(table_name):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="doubles"
)
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, connection)
    
    # Close the connection
    connection.close()
    
    return df

# Streamlit UI
st.title('🎾 *TENNIS RANKING EXPLORER*')

# Sidebar to select the database & table
table_choice = st.sidebar.radio("Select Table", ["Categories", "Competitions", "Complexes", "Venues","Competitor","Competitor_Rankings"])

# Initialize session state for button toggle
if "show_data" not in st.session_state:
    st.session_state.show_data = False

# Define button behavior
def toggle_data():
    st.session_state.show_data = not st.session_state.show_data

# Button to toggle data
st.button("Show/Hide Data", on_click=toggle_data)

# Display the selected table's data if the button is clicked
if st.session_state.show_data:
    
        if table_choice == "Categories":
            df = get_data("categories")
            st.subheader("📂 Categories Table")
            st.write(df)

        elif table_choice == "Competitions":
            df = get_data("competitions")
            st.subheader("🏆 Competitions Table")
            st.write(df)
    
    
        elif table_choice == "Complexes":
            df = get_data_db2("complexes")
            st.subheader("🏟️ Complexes Table")
            st.write(df)

        elif table_choice == "Venues":
            df = get_data_db2("venues")
            st.subheader("📍 Venues Table")
            st.write(df)
        elif table_choice == "Competitor":
            df=get_data_db3("competitor")
            st.subheader("🏃Competitors Table")
            st.write(df)
        elif table_choice == "Competitor_Rankings":
            df=get_data_db3("competitor_rankings")
            st.subheader("🏅Competitor_Rankings Table")
            st.write(df)
st.markdown("---")

#competitor and competitor_ranking details
# sql connection (xampp)
def get_connection():
    return mysql.connector.connect(
        host="localhost",  # e.g., "localhost"
        user="root",
        password="",
        database="doubles"
    )

# Fetch competitor ranking data
def fetch_competitor_rankings(rank):
    conn = get_connection()
    query = "SELECT * FROM competitor_rankings WHERE `rank` = %s"
    df = pd.read_sql(query, conn, params=(rank,))
    conn.close()
    return df

# Fetch competitor details data
def fetch_competitor_data(rank):
    conn = get_connection()
    query = """
        SELECT c.*
        FROM competitor c
        JOIN competitor_rankings cr ON c.competitor_id = cr.competitor_id
        WHERE cr.rank = %s
    """
    df = pd.read_sql(query, conn, params=(rank,))
    conn.close()
    return df

st.title("🎯Competitor Rankings & Details")

#  Sidebar Section
st.sidebar.markdown("---")
st.sidebar.header("⭐Select Rank")

selected_rank = st.sidebar.slider("Rank", min_value=1, max_value=100, value=1)



# Fetch data from MySQL
rankings_data = fetch_competitor_rankings(selected_rank)
competitor_data = fetch_competitor_data(selected_rank)

# Display Competitor Rankings
st.subheader(f"👉Competitor Rankings for Rank {selected_rank}")
if not rankings_data.empty:
    st.dataframe(rankings_data)  
else:
    st.warning(f"No rank details available  for rank :{selected_rank}.")

# Display Competitor Details
st.subheader(f"👉Competitor Details for Rank {selected_rank}")
if not competitor_data.empty:
    st.dataframe(competitor_data)  
else:
    st.warning(f"No competitor details available for rank {selected_rank}.")

#slider for displaying venues 

st.markdown("---")


#Mysql database connection
def connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",  
            user="root",
            password="",
            database="compl"
        )
        return conn
    except mysql.connector.Error as err:
        st.error(f"Database Connection Error: {err}")
        return None


#Complexes and venues details
def venues(complex_id):
    conn = connection()
    if conn is None:
        return pd.DataFrame()
    
    query = "SELECT * FROM complexes WHERE complex_id = %s"
    try:
        df = pd.read_sql(query, conn, params=(complex_id,))
        
    except Exception as e:
        st.error(f" Error fetching venue details: {e}")
        df = pd.DataFrame()
    conn.close()
    return df

#  Fetching complex details
def complexes(complex_id):
    conn = connection()
    if conn is None:
        return pd.DataFrame()
    
    query = """
        SELECT v.* FROM venues v
        JOIN complexes c ON v.complex_id = c.complex_id
        WHERE v.complex_id = %s
    """
    try:
        df = pd.read_sql(query, conn, params=(complex_id,))
        
    except Exception as e:
        st.error(f" Error fetching complex details: {e}")
        df = pd.DataFrame()
    conn.close()
    return df


st.title("📍 VENUES DETAILS")

st.sidebar.markdown("---")
st.sidebar.header("📍 Enter Complex ID")

#  Get user input  "sr:complex:35290"
user_input = st.sidebar.text_input("Enter Complex ID", "sr:complex:81815")

selected_id = user_input  # Keep full format

#  Fetch data from MySQL
venues_data = venues(selected_id)
complexes_data = complexes(selected_id)

# Display Venue Details
st.subheader(f"👉 VENUE DETAILS for {user_input}")
if not venues_data.empty:
    st.dataframe(venues_data)
else:
    st.warning(f"😔No data available for {user_input}.")

# Display Complex Details
st.subheader(f"👉 COMPLEX DETAILS for {user_input}")
if not complexes_data.empty:
    st.dataframe(complexes_data)
else:
    st.warning(f"😔 No data available for {user_input}.")
#categories and competitions
#sql data base connection
import streamlit as st
import mysql.connector
import pandas as pd

# Database connection
import streamlit as st
import mysql.connector
import pandas as pd

# Database connection
def connections():
    try:
        conn = mysql.connector.connect(
            host="localhost",  
            user="root",
            password="",
            database="sample"
        )
        return conn
    except mysql.connector.Error as err:
        st.error(f"Database Connection Error: {err}")
        return None

# Fetch category details
def categories(category_id):
    conn = connections()
    if conn is None:
        return pd.DataFrame()
    
    query = "SELECT * FROM categories WHERE category_id = %s"
    try:
        df = pd.read_sql(query, conn, params=(category_id,))
    except Exception as e:
        st.error(f"Error fetching category details: {e}")
        df = pd.DataFrame()
    finally:
        conn.close()
    return df

# Fetch competition details
def competitions(category_id):
    conn = connections()
    if conn is None:
        return pd.DataFrame()
    
    query = """
        SELECT ca.* FROM categories ca
        JOIN competitions c ON ca.category_id = c.category_id
        WHERE ca.category_id = %s
    """
    try:
        df = pd.read_sql(query, conn, params=(category_id,))
    except Exception as e:
        st.error(f"Error fetching competition details: {e}")
        df = pd.DataFrame()
    finally:
        conn.close()
    return df

# Streamlit UI
st.title("🎯 Competitions and Categories Details")

st.sidebar.markdown('---')
st.sidebar.header("🏃🏻‍♂️ Select Category ID")

# Dropdown in the sidebar
selected_option = st.sidebar.selectbox(
    "Choose the category_id:",
    ["sr:category:1012", "sr:category:1474", "sr:category:1475", "sr:category:1476",
     "sr:category:181", "sr:category:213", "sr:category:2400", "sr:category:2414",
     "sr:category:2516", "sr:category:2517", "sr:category:3", "sr:category:6",
     "sr:category:72", "sr:category:74", "sr:category:76", "sr:category:785",
     "sr:category:79", "sr:category:871"]
)

# Fetch data from MySQL
categories_data = categories(selected_option)
competitions_data = competitions(selected_option)

# Display Category Details
st.subheader(f"👉 CATEGORIES DETAILS for {selected_option}")
if not categories_data.empty:
    st.dataframe(categories_data)
else:
    st.warning(f"😔 No data available for {selected_option}.")

# Display Competition Details
st.subheader(f"👉 COMPETITIONS DETAILS for {selected_option}")
if not competitions_data.empty:
    st.dataframe(competitions_data)
else:
    st.warning(f"😔 No data available for {selected_option}.")










