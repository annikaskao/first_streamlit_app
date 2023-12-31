import streamlit
import pandas
import snowflake.connector
import requests
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Lime', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

# Create the repeatable code block (called a function)
def get_fruityvice_date(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

# New Secion to Display fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")
try: 
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select fruit to get information.")
  else:
    back_from_function = get_fruityvice_date(fruit_choice)
    streamlit.dataframe(back_from_function)

except URLError as e:
  streamlit.error()


# streamlit.write('The user entered ', fruit_choice)

# import requests
# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
# Removing line to only show table
# streamlit.text(fruityvice_response.json())  # just writes the data to the screen

# Normalizes the json version of the response
# fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# Outputs a table to the screen
# streamlit.dataframe(fruityvice_normalized)

# don't run anything past here while we troubleshoot
# streamlit.stop()

# import snowflake.connector

streamlit.header("View Our Fruit List - Add Your Favorites!")
# Snoeflake-related functions
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from fruit_load_list")
    return my_cur.fetchall()

# Add button to load fruit 
if streamlit.button('Get Fruit List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  my_cnx.close()
  streamlit.dataframe(my_data_rows)
  
# my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
# my_cur = my_cnx.cursor()
# my_cur.execute("select * from fruit_load_list")
# my_data_rows = my_cur.fetchall()
# streamlit.dataframe(my_data_rows)

# Allow the enduser to add a fruit to the list 
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values ('" + add_my_fruit +"')")
    return "Thanks for adding " + add_my_fruit


add_my_fruit = streamlit.text_input('What fruit would you like to add?')

if streamlit.button('Add a Fruit to the List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function = insert_row_snowflake(add_my_fruit)
  streamlit.text(back_from_function)


# streamlit.write('Thanks for adding ', add_my_fruit)

# This will not work correctly, but just go with it 
# my_cur.execute("insert into fruit_load_list values ('from streamlit')")
