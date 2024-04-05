# Streamlit app for Baby Names by the Generations
# Dylan Bay lab 9
# Fair Attribution: Some functions were modified with help from Claude and further modified again for own use

import streamlit as st
import pandas as pd
import plotly.express as px

# load data from URL
# url = 'https://github.com/esnt/Data/raw/main/Names/popular_names.csv'
# df = pd.read_csv(url)

# local option:
# df = read_csv("popular_names.csv")

# cached URL option:
@st.cache_data
def load_data():
    url = 'https://github.com/esnt/Data/raw/main/Names/popular_names.csv'
    return pd.read_csv(url)
df = load_data()


# define generations as dict, mostly from Pew definitions, years inclusive
gendict = {
   "GI Gen": (1901, 1927),
   "Silent": (1928, 1945),
   "Boomer": (1946, 1964),
   "Gen X": (1965, 1980),
   "Millennial": (1981, 1996),
   "Gen Z": (1997, 2012),
   "Gen Alpha": (2013, 2024)
}

# begin streamlit stuff
st.title("Baby Names by the Generations")

# get input for use everywhere, default John
default_name = "Jamie"
input_name = st.text_input("Enter a name:", default_name)
input_name = input_name.lower().capitalize()  # in case we have lower-case lovers
# lets them also choose generations to display, defaulted to most expected four
# chosen_gens = st.multiselect("Select generations:", list(gendict.keys()), ["Boomer", "Gen X", "Millennial", "Gen Z"])
# changed my mind, default to ALL:
chosen_gens = st.multiselect("Select generations:", list(gendict.keys()), default = list(gendict.keys()))

namedf = df[df["name"] == input_name]

# external link, formatted to give context/meaning of name
external_link = f"https://www.behindthename.com/name/{input_name.lower()}"
# this works for me, hope it works for others too?
if st.button("Name Context (Click to open link)"):
   st.write(f"Opening {external_link}")
   import webbrowser
   webbrowser.open(external_link)
# alternate method, generates in-browser link instead:
# external_link = f"https://www.behindthename.com/name/{input_name.lower()}"
# if input_name:
    # st.button("Name Context (Click to generate link)", on_click = st.markdown(f"[Click Me!]({external_link})")

# main section (graph)
chartdf = []  # further filtering for display purposes will happen here
for generation, year_range in gendict.items():
   if generation in chosen_gens:
       # displays only selected generations with if statement, filters data using year dict values below
       generation_data = namedf[(namedf["year"] >= year_range[0]) & (namedf["year"] <= year_range[1])]
       total_n = generation_data["n"].sum()
       chartdf.append({"Generation": generation, "Total": total_n}) # ensures main chart data is straightforward to graph
main_chart = px.bar(chartdf, x = "Generation", y = "Total", title = "Name Popularity (Absolute) by Generation", color_discrete_sequence = ["#66C2A5"])
st.plotly_chart(main_chart)

# sidebar pie chart
piedf = namedf[namedf["year"].isin([year for generation in chosen_gens for year in range(gendict[generation][0], gendict[generation][1] + 1)])]
pie_chart = px.pie(piedf, values = "n", names = "sex", title = "Usage as a Male vs Female Name",
                   color_discrete_sequence = ["#FC8D62", "#8DA0CB"],
                   category_orders = {"sex": ["M", "F"]})
st.sidebar.plotly_chart(pie_chart, use_container_width=True)
           
