# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title("Example Streamlit App :balloon:")
st.write("Replace the code in this example app with your own code! And if you're new to Streamlit, here are some helpful links: are below")

name_on_order=st.text_input('name on smoothie')
st.write('The name on your smoothie will be',name_on_order)

cnx=st.connection("snowflake")
session=cnx.session()
#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
st.dataframe(data=my_dataframe, use_container_width=True)

ingredient_list = st.multiselect(
    "Choose ingredient"
    ,my_dataframe
    ,max_selections=5
)

if ingredient_list:
    #st.write(ingredient_list)
    #st.text(ingredient_list)
    ingredients_string=''
    for fruit_chosen in ingredient_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+fruit_chosen)
        sf_df= st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)

    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                values ('""" + ingredients_string + """','""" +name_on_order + """' )"""
    
    #st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Button')
    
    if time_to_insert :
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
        





