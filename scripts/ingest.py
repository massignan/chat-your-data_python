# LangChain imports
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import TextSplitter, RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone, FAISS
from langchain.vectorstores.base import VectorStore
from langchain.docstore.document import Document

# 3rd party imports
from dotenv import load_dotenv
import pinecone

# Python package imports
from typing import List, Type
import os
import pickle
import inspect


class Ingest():
    '''
    Class to handle the Ingestion process to load, embed and store data, based on multiple PDF files 
    for future reference on querying the data using AI.
    '''
    @classmethod
    def load_documents(cls, files: List[str], text_splitter: TextSplitter, verbose: bool = False) -> List[Document]:
        '''Wrapper method for loading documents in PDF format, using the PyPDFLoader.'''
        documents = []
        for file in files:
            loader = PyPDFLoader(file)
            pages = loader.load_and_split()
            documents.extend(text_splitter.split_documents(pages))
            if verbose:
                print(f"File {file} loaded." )
        return documents

    @classmethod
    def store(cls, documents: List[Document], store: Type[VectorStore], index_name: str, openai_api_key: str, local_file: bool = False, **kwargs) -> None:
        '''Method to create Embeddings and store in a VectorStore of type Pinecone or FAISS'''
        
        embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

        if not inspect.isclass(store):
            raise Exception('Store must be a class of type VectorStore.')
        
        if store is Pinecone:
            try:
                pinecone.init(
                    api_key = kwargs['pinecone_api_key'], 
                    environment = kwargs['pinecone_environment']
                )
            except KeyError as ke:
                print(f'{str(ke).upper()} must be provided.')
                raise ke
            except:
                raise Exception('PINECONE error to connect.')

        db = store.from_documents(documents, embeddings, index_name=index_name)
        if local_file:
            with open(f'{index_name}.pkl', 'wb') as f:
	            pickle.dump(db, f)


def main():
    BASEDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
    filelist = [os.path.join(BASEDIR, file) for file in os.listdir(BASEDIR) if '.PDF' in file.upper()]

    load_dotenv(os.path.join(BASEDIR, '..', '.env'))

    documents = Ingest.load_documents(
        files = filelist,
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1000,
            chunk_overlap = 200
        ),
        verbose = True
    )

    Ingest.store(
        documents = documents,
        store = FAISS,
        index_name = 'vectorstore',
        local_file = True,
        openai_api_key = os.getenv('OPENAI_API_KEY')
    )

if __name__ == '__main__':
    main()
