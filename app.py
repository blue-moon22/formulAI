import os
import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper
from langchain.chat_models import ChatOpenAI
from langchain.agents import create_csv_agent
from langchain.document_loaders import CSVLoader

import time
os.environ["OPENAI_API_KEY"] = ""

def addtodatabase(protocol,ingredients):
    #creates and adds to log database to log 
    #For ! Rating ! Time #

    logfile = open('log.txt','a')
    currenttime=time.time()
    logstring = protocol + "," + ingredients  + "," + str(currenttime) + ","
    logfile.write(logstring)
    logfile.close()

def addtodatabaserating(rating):
    #creates and adds to log database to log 
    #For ! Rating ! Time #

    logfile = open('log.txt','a')
    logstring = str(rating)  + ",\n"
    logfile.write(logstring)
    logfile.close()

# App framework
st.title("🪄🧪 FormulAI")
prompt = st.text_input("What would you like to formulate?")

# Adding options:
formula_options = ['Cream', 'Spray', 'Any']
selected_option = st.selectbox('Select an option:', formula_options)
st.write('You selected:', selected_option)

# Prompt templates
ingredients_template = PromptTemplate(
    input_variables = ['chemical','csvdata', 'selected_option'],
    template = "Write me the ingredients for a {selected_option} formulation that includes {chemical} while leveraging current formulations found in: {csvdata}, if the chemical is not directly in csvdata suggest a similar chemical. Do not mention dataset in response. The function of the ingredients should be in the format: 'ingredient: (function)', for example: 'Glycerin: (Humectant) in a bullet point format"
)

protocol_template = PromptTemplate(
    input_variables = ['ingredients', 'wikipedia_research'],
    template = "Write a protocol for putting together the {ingredients} while leveraging this wikipedia reserch:{wikipedia_research}."
)

# Memory 
ingredients_memory = ConversationBufferMemory(input_key='chemical', memory_key='chat_history')
protocol_memory = ConversationBufferMemory(input_key='ingredients', memory_key='chat_history')
csv_memory = ConversationBufferMemory(input_key='csvdata', memory_key='chat_history')

# LLMs
llm = OpenAI(model_name="gpt-3.5-turbo")
ingredients_chain = LLMChain(llm=llm, prompt=ingredients_template, verbose=True, output_key="ingredients", memory=ingredients_memory)
protocol_chain = LLMChain(llm=llm, prompt=protocol_template, verbose=True, output_key="protocol", memory=protocol_memory)
csvagent = create_csv_agent(OpenAI(temperature=0.2),'skincare_products_clean.csv',verbose=True, output_key="csvdata", memory=csv_memory)

wiki = WikipediaAPIWrapper()

# Show stuff on screen
if st.button('Submit Formulation Request'):
    st.spinner('Formulating...')
    csvdata = csvagent.run(prompt)
    ingredients = ingredients_chain.run(chemical=prompt, csvdata=csvdata, selected_option=selected_option)
    wiki_research = wiki.run(prompt) 
    protocol = protocol_chain.run(ingredients=ingredients, wikipedia_research=wiki_research)
    st.balloons()
    st.sidebar.write('## Ingredients')
    st.sidebar.write(ingredients)
        
    with st.container():

        st.write('## Protocol')
        st.write(protocol) 

    addtodatabase(protocol,ingredients)

    st.write('## Extra Information')
    with st.expander('Ingredients History'): 
        st.info(ingredients_memory.buffer)

    with st.expander('Protocol History'): 
        st.info(protocol_memory.buffer)

    with st.expander('Wikipedia Research'): 
        st.info(wiki_research)

st.write('### Feedback')
rating = st.number_input('Enter your rating for the supplied formulation')

if st.button('Submit Rating'):
    addtodatabaserating(rating)
