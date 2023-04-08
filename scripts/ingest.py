import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
import pinecone
from dotenv import load_dotenv

print("Starting ingesting data.")

# Load environment variables from .env file
BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR + "\\..\\", '.env'))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

try:
    pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)
except:
    print("PINECONE error to connect.")

#load data
dirpath = os.path.dirname(__file__) + "\\..\\data\\"
filelist = os.listdir(dirpath)

if len(filelist) == 0:
    print("Data directory is empty.")
    exit(0)

#Create chunks from data loaded
textSplitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap  = 200,
)

docs = list()
for file in filelist:
    filepath = dirpath + file
    loader = PyPDFLoader(filepath)
    pages = loader.load_and_split()
    docs = docs + textSplitter.split_documents(pages)
    print("File " + file + " loaded." )

print("All files loaded. Starting create embeddings and storing the data in the vector database.")

#Create and store the embeddings in the vectorStore
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
vectorstore = Pinecone.from_documents(docs,embeddings,index_name=PINECONE_INDEX_NAME)

print("Ingestion completed!")




