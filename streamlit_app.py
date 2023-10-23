# main python file
import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


# 🥣 🥗 🐔 🥑🍞
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Hard-Boiled Free-Range Egg')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]


# Display the table on the page.
streamlit.dataframe(fruits_to_show)

def get_fruity_choice(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
  


# new section for fruity vice api calls
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error('Please select a fruit to get more information')
  else:
    streamlit.write('The user entered ', fruit_choice)
    back_from_function = get_fruity_choice(fruit_choice)    
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()

streamlit.header('My fruit load list contains:')
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from fruit_load_list")
    return my_cur.fetchall()

if streamlit.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])  
  my_data_rows = get_fruit_load_list()
  my_cnx.close()
  streamlit.dataframe(my_data_rows)

#streamlit.stop()
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("INSERT INTO fruit_load_list values ('" + new_fruit + "')")
    return 'Thanks for adding a new fruit to snowflake: ' + new_fruit
  
add_fruit_choice = streamlit.text_input('What fruit would you like information about? - ')
if streamlit.button('Add a fruit to the list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])  
  back_from_function = insert_row_snowflake(add_fruit_choice)
  streamlit.text(back_from_function)
  
#streamlit.write('The user entered ', add_fruit_choice)
#my_cur.execute("INSERT INTO fruit_load_list values ('" + new_fruit + "')")



