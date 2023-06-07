# FormulAI

LangChain/GPT 3.5 App for generating ingredients and protocols for formulations

## Prerequisites

Get an [OpenAI API Key](https://platform.openai.com/account/api-keys) and set it as your environmental variable `OPENAI_API_KEY`. (Also need to set a billing and usage limit.)

## Install

```
git clone https://github.com/blue-moon22/formulAI.git
cd formulAI

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Quickstart

```
streamlit run app.py
```

## To Do

- Use [Apify](https://python.langchain.com/en/latest/modules/agents/tools/examples/apify.html) to search [WIPO](https://patentscope.wipo.int/search/en/search.jsf)
- Prompt design (which healthcare companies, chemical, what is chemical similar to, search all similar compounds)

## Resources

- [LangChain Crash Course: Build a AutoGPT app in 25 minutes!](https://www.youtube.com/watch?v=MlK6SIjcjE8)
- [LangChain](https://python.langchain.com/)
