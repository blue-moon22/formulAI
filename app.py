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



# App framework
st.title("🪄🧪 FormulAI")
prompt = st.text_input("What would you like to formulate?")

# Prompt templates
ingredients_template = PromptTemplate(
    input_variables = ['chemical','csvdata'],
    template = "Write me the ingredients for a formulation that includes {chemical} while leveraging current formulations found in: {csvdata}, if the chemical is not directly in csvdata suggest a similar chemical. do not mention dataset in response. The function of the ingredients should be in the format: 'ingredient: (function) for example: 'Glycerin: (Humectant)"
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
if prompt:
    csvdata = csvagent.run(prompt)
    ingredients = ingredients_chain.run(chemical=prompt, csvdata=csvdata)
    wiki_research = wiki.run(prompt) 
    protocol = protocol_chain.run(ingredients=ingredients, wikipedia_research=wiki_research)
    
    st.write(ingredients)
    st.write(protocol) 

    with st.expander('Ingredients History'): 
        st.info(ingredients_memory.buffer)

    with st.expander('Protocol History'): 
        st.info(protocol_memory.buffer)

    with st.expander('Wikipedia Research'): 
        st.info(wiki_research)

        
""" 
    with st.expander('CSV History'): 
        st.info(csv_memory.buffer) """