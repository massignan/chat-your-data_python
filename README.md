# chat-your-data_python

This project aims to provide a conversational experience with your own data using ChatGPT-like model, LangChain, Pinecone and OpenAI, all developed in Python your own data saved in one ou more PDF's files.

This app was developed using the followings referemces:

[chat-your-data](https://github.com/hwchase17/chat-your-data) developed by HwChase17

[gpt4-pdf-chatbot-langchain](https://github.com/mayooear/gpt4-pdf-chatbot-langchain) developed by Maio


# Prerequisites

## Packages

First, make sure to install the following Python packages:

```bash
pip install langchain
```
```bash
pip install openai
```
```bash
pip install PyPDF
```
```bash
pip install dotenv
```
```bash
pip install gradio
```

## Pinecone

Create an account in [Pinecone](http:\\pinecones.io) and get your API key.

The STARTER plan is all you need to test the code. Pay attention to limitation of just onde index (database).

Create an index with the followings configuration to use OpenAI ChatGPT API:

Metric: cosine
Dimensions: 1536

## OpenAI

Create an account in [OpenAI](https:\\openai.com) and get your API key.

## Environment variables

## Set up .env file:

Using you [Pinecone](http:\\pinecones.io) and [OpenAI](https:\\openai.com) API keys set up the .env file.


```bash
OPENAI_API_KEY =  *type your OpenAI key*

PINECONE_API_KEY = *type your Pinecone key*

PINECONE_ENVIRONMENT = *type the Pincone environment, like eu-west1-gcp*

PINECONE_INDEX_NAME = *type the Pinecone index name*
```

# Ingest Data

This script will load the **`.pdf`** file as text and will create the [embeddings](https://towardsdatascience.com/neural-network-embeddings-explained-4d028e6f0526) using [OpenAI](https:\\openai.com) ChatGPT model.

The embeddings wil be saved in [Pinecone](http:\\pinecones.io) [vector database](https://www.pinecone.io/learn/vector-database/#:~:text=A%20vector%20database%20indexes%20and,vector%20noun).

Save your **`.pdf`**  files data source in **`./data`** directory.

Run the scripts ingest.py in **`./scripts`** directory.

If necessary, adjust the data chunk sizes and overlap tunning these values in **`textSplitter = RecursiveCharacterTextSplitter(chunk_size,chunk_overlap)`**.

# Query Data

In the file  (**`query.py`**) there is the [prompt](https://en.wikipedia.org/wiki/Prompt_engineering) to create a condensate question in order to create a conversional experience. Also, there is the [prompt](https://en.wikipedia.org/wiki/Prompt_engineering) to question and answer (Q&A).

Adjust the [prompts](https://en.wikipedia.org/wiki/Prompt_engineering) if necessary.

# Front End

The Chat bot was developed using [Gradio](https://gradio.app) to create a user friendly UI to chat with you data.

# Running

Run the application and use the webrowser to use the chat.

```bash
py app.py
```

# Example

Was used the [World Bank Annual Report 2022 Downloads](https://www.worldbank.org/en/about/annual-report#anchor-annual) as example.

