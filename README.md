# chat-your-data_python

This project aims to provide a conversational experience with your own PDFs files data using ChatGPT-like model, LangChain, Pinecone and OpenAI, all developed in Python.

This app was developed using the followings references:

[chat-your-data](https://github.com/hwchase17/chat-your-data) developed by HwChase17

[gpt4-pdf-chatbot-langchain](https://github.com/mayooear/gpt4-pdf-chatbot-langchain) developed by Maio


# Prerequisites

## Packages

First, make sure to install the following Python packages:

```bash
pip install langchain
```
```bash
pip install pinecone-client
```
```bash
pip install openai
```
```bash
pip install tiktoken
```
Tiktokon - needed in order to for OpenAIEmbeddings
```bash
pip install PyPDF
```
```bash
pip install python-dotenv
```
```bash
pip install gradio
```


## Pinecone

Create an account in [Pinecone](http://pinecones.io) and get your API key.

The STARTER plan is all you need to test the code. Pay attention to limitation of just onde index (database) in STARTE plan. If necessary, delete de index created in order to test a new index.

Create an index with the followings configuration to use OpenAI ChatGPT API:

Metric: cosine

Dimensions: 1536

## OpenAI

Create an account in [OpenAI](https://openai.com) and get your API key.

## Environment variables

## Set up .env file:

Using your [Pinecone](http://pinecones.io) and [OpenAI](https://openai.com) API keys set up the .env file.


```bash
OPENAI_API_KEY =  *type your OpenAI key*

PINECONE_API_KEY = *type your Pinecone key*

PINECONE_ENVIRONMENT = *type the Pincone environment, like eu-west1-gcp*

PINECONE_INDEX_NAME = *type the Pinecone index name*
```

# Ingest Data

This script will load the **`.pdf`** file as text and will create the [embeddings](https://towardsdatascience.com/neural-network-embeddings-explained-4d028e6f0526) using [OpenAI](https://openai.com) ChatGPT model.

The embeddings wil be saved in [Pinecone](http://pinecones.io) [vector database](https://www.pinecone.io/learn/vector-database/#:~:text=A%20vector%20database%20indexes%20and,vector%20noun).

Save your **`.pdf`**  files data source in **`./data`** directory.

Run the scripts ingest.py in **`./scripts`** directory.

If necessary, adjust the data chunk and overlap values in **`textSplitter = RecursiveCharacterTextSplitter(chunk_size,chunk_overlap)`**.

# Query Data

In the file  (**`query.py`**) there is the [prompt](https://en.wikipedia.org/wiki/Prompt_engineering) condensate question used to create a conversional experience (question + chat history). Also, there is the [prompt](https://en.wikipedia.org/wiki/Prompt_engineering) to question and answer (Q&A).

Adjust the [prompts](https://en.wikipedia.org/wiki/Prompt_engineering) if necessary.

The [OpenAI model](https://platform.openai.com/docs/models) used is **`gpt-3.5-turbo`**. Go to  **`llm = OpenAI(temperature=0,model_name="gpt-3.5-turbo")`** in (**`query.py`**) to change the [OpenAI model](https://platform.openai.com/docs/models).

# Front End

The Chat bot was developed using [Gradio](https://gradio.app) to create a user friendly UI to chat with you data.

# Running

Run the application and use the webrowser to use the chat.

```bash
py app.py
```

# Example

It was used the [World Bank Annual Report 2022](https://www.worldbank.org/en/about/annual-report#anchor-annual) as data source example.

# Troubleshooting

## Pinecone

The STARTER plan has a limit of just one index per account. 

## SSL: CERTIFICATE_VERIFY_FAILED

If you address SSL errors, you can install the **`python-certifi-win32`** package. By doing so, the package will take over the **`certifi`** library utilized in HTTPS requests and integrate the Windows certificate repository to authenticate the certificate and ensure its validity. Just a simple installation of this package can solve the issue.

```bash
pip install python-certifi-win32
```
