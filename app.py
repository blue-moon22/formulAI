import os
import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper
import time

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

# Prompt templates
ingredients_template = PromptTemplate(
    input_variables = ['chemical'],
    template = "Write me the ingredients for a formulation that includes {chemical}."
)

protocol_template = PromptTemplate(
    input_variables = ['ingredients', 'wikipedia_research'],
    template = "Write a protocol for putting together the {ingredients} while leveraging this wikipedia reserch:{wikipedia_research}."
)

# Memory 
ingredients_memory = ConversationBufferMemory(input_key='chemical', memory_key='chat_history')
protocol_memory = ConversationBufferMemory(input_key='ingredients', memory_key='chat_history')

# LLMs
llm = OpenAI(model_name="gpt-3.5-turbo")
ingredients_chain = LLMChain(llm=llm, prompt=ingredients_template, verbose=True, output_key="ingredients", memory=ingredients_memory)
protocol_chain = LLMChain(llm=llm, prompt=protocol_template, verbose=True, output_key="protocol", memory=protocol_memory)

wiki = WikipediaAPIWrapper()

# Show stuff on screen
if st.button('Submit Formulation Request'):
    ingredients = ingredients_chain.run(prompt)
    wiki_research = wiki.run(prompt) 
    protocol = protocol_chain.run(ingredients=ingredients, wikipedia_research=wiki_research)

    st.write(ingredients)
    st.write(protocol) 

    addtodatabase(protocol,ingredients)

    with st.expander('Ingredients History'): 
        st.info(ingredients_memory.buffer)

    with st.expander('Protocol History'): 
        st.info(protocol_memory.buffer)

    with st.expander('Wikipedia Research'): 
        st.info(wiki_research)



rating = st.number_input('Enter your rating for the supplied formulation')


if st.button('Submit Rating'):
    addtodatabaserating(rating)



