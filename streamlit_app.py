import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError
streamlit.title('my moms new healthy diner')
streamlit.header('Breakfast menu')
streamlit.text('🥣omega 3, blueberry oatmeal')
streamlit.text('🥗kale, spinach & rocket smoothe')
streamlit.text(' 🐔 hard-boiled free range egg')
streamlit.text('🥑 Avacado toast') 
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
#streamlit.dataframe(my_fruit_list)
fruits_selected =streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Banana','Apple'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)
def get_fruityvice_data(this_fruit_choice):
       fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
       fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
       return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
      streamlit.error("please select a fruit to get information.")
  else:
    ##  import requests
     back_from_function = get_fruityvice_data(fruit_choice)
     streamlit.dataframe(back_from_function)
      
except URLError as e:
    streamlit.error()




#streamlit.stop()




#import snowflake.connector
streamlit.header("The Fruit load list contains:")
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
         my_cur.execute("select * from fruit_load_list")
         return my_cur.fetchall()
if streamlit.button('Get Fruit Load List'):
       my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
       my_data_rows = get_fruit_load_list()
       my_cnx.close()
       streamlit.dataframe(my_data_rows)
 
#streamlit.stop()
       
#my_cur = my_cnx.cursor()
#my_cur.execute("SELECT * from fruit_load_list")
#my_data_rows = my_cur.fetchall()
#streamlit.header("The Fruit load list contains:")
#streamlit.dataframe(my_data_rows)

#fruit_choice = streamlit.text_input('What fruit would you like to add?','jackfruit')
#streamlit.write('Thanks for adding', fruit_choice)
#import requests
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

#my_cur.execute("insert into fruit_load_list values ('from streamlit')")

def insert_row_snowflake(new_fruit):
       with my_cnx.cursor() as my_cur:
              my_cur.execute("insert into fruit_load_list values ('" + add_my_fruit + "')")
              return "thanks for adding " + new_fruit
add_my_fruit = streamlit.text_input('what fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   back_from_function = insert_row_snowflake(add_my_fruit)
   streamlit.text(back_from_function)


