import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain.output_parsers import CommaSeparatedListOutputParser

import os
import re

load_dotenv()

# support_arabic_text(all=True)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Vazir&display=swap');

body {
    font-family: 'Vazir', sans-serif;
    font-weight: bold;
}

/* Specific styles for headers and titles */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Vazir', sans-serif;
    text-align: right;
    font-weight: bold;
}

/* Increase the font size of the tabs */
.stTabs .stTab {
    font-size: 20px;  /* Adjust the size as needed */
    padding: 10px;    /* Adjust padding for better spacing */
}



/* Align tab text to the right */
.stTabs {
    direction: rtl;
}

/* Align the content of the tabs to the right */
.stTabContent {
    text-align: right;
}

.stHeader{
    text-align: right;
}

.stNumberInput {
    text-align: left;  /* Align text to the right */
}

.centered-link {
    display: flex;
    justify-content: center; /* Center horizontally */
    align-items: center; /* Center vertically if needed */
    height: 10vh; /* Optional: Set height to fill the viewport */
    font-size: 20px;
}

a {
    text-decoration: none; /* Remove underline */
}

a:hover {
    text-decoration: none; /* Underline on hover */
}
</style>
""", unsafe_allow_html=True)


# Set the title of the app
st.title("دستیار سئو آرگونز")

# Cache the Groq model
@st.cache_resource
def load_groq_model():
    # Initialize your Groq model here
    model = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="gemma2-9b-it")
    return model

# Load the cached Groq model
groq_model = load_groq_model()

parser = CommaSeparatedListOutputParser()



# Create tabs
tab1, tab2 = st.tabs(["جستجو", "اصلاح متن"])

# Tab 1: Search
with tab1:
    st.header("جستجو کلمات کلیدی در سئو")
    
    # Text area input
    text_input = st.text_area("متن خود را برای تجزیه و تحلیل سئو وارد کنید:")
    
    # Numeric input field
    numeric_input = st.number_input("یک مقدار عددی وارد کنید (تعداد کلمات کلیدی):", min_value=2, step=1, max_value=100)
    
    system = "You are as a Google SEO assistant for improving the Persian contents in SEO analytics from 2023 onwards."
    
    
    # Search button
    if st.button("جستجو"):
        
            prompt = ChatPromptTemplate.from_messages([
                ("system", system),
                ("human", "Offer top most searched {keys_num} keywords for the {content} with considering the SEO analytics to improve it. Just the words and their search counts without any extra explanation. The Keywords should be in Persian, non-repetitive, and at most two-parts and no more. All content should be Persian.")
            ])
            
            
            chain = prompt | groq_model | parser
            
            result = chain.invoke({"keys_num": numeric_input, "content":  text_input})[:numeric_input]
            # Define the regex pattern
            pattern = r'^\d+\.\s.*$'  # Matches 'عدد. متن' pattern
            # Filter the list using list comprehension
            filtered_items = [s for s in result if re.match(pattern, s)]
            
            st.write("نتیجه کلمات کلیدی شما:")
            st.write(filtered_items)

# Tab 2: Fix
with tab2:
    
    system = "You are as a professional Google SEO Assistant for improving Persian Contents ranks based on Google SEO policy. "
    st.header("اصلاح متن از لحاظ سئو")
    
    # Text area input for fixing
    fix_input = st.text_area("متنی را که می‌خواهید اصلاح کنید وارد کنید:")
    
    # Fix button
    if st.button("اصلاح متن"):
        prompt = ChatPromptTemplate.from_messages([
            ("system", system),
            ("human", "Take the {content} and optimize it for better ranking according to Google's search engine policies. Return the entire text in Persian. Do not provide any additional explanation. Make hard revision on the content and Generate new words.")
        ])
        parser = StrOutputParser()
        chain = prompt | groq_model | parser
        st.write("متن اصلاح شده شما:")
        st.write(chain.invoke({"content": fix_input}))
        


st.markdown('<div class="centered-link"><a href="https://donito.me/akademi_arman">Support Us &#x2764;</a></div>', unsafe_allow_html=True)