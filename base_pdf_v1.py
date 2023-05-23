from typing import Optional

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import UnstructuredURLLoader
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.document_loaders import GoogleDriveLoader
from google.auth.exceptions import RefreshError

import requests
import google
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

class KnowledgeBase:
    def __init__(self, source: str):
        logger.info("Building knowledge base....")

        logger.info("Connecting to folder.....")
        loader = GoogleDriveLoader(folder_id="1Cmat7LIISE4E6gsqtm6Ywa4-nLo6dazG", credentials_path="credentials.json")
        documents = loader.load()

        logger.info("{n} file ditemukan", n=len(documents))

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0)
        doc_texts = text_splitter.split_documents(documents)
        logger.info("{n} jumlah chunk file", n=len(doc_texts))

        logger.info("Building the vector database.....")
        embeddings = OpenAIEmbeddings()
        docsearch = Chroma.from_documents(doc_texts, embeddings)

        logger.info("Building the retrieval chain.....")
        self.chain = RetrievalQAWithSourcesChain.from_chain_type(
            ChatOpenAI(),
            chain_type="map_reduce",
            retriever=docsearch.as_retriever()
        )

        self.credentials = None

        logger.info("Knowledge base created")

    def ask(self, query: str):
        return self.chain({"question": query}, return_only_outputs=True)
    
       
    def refresh_google_auth_token(self, credentials):
        try:
            credentials.refresh(requests.Request())
        except google.auth.exceptions.RefreshError as e:
        # The token has expired or been revoked.
            error_description = e.args[1]['error_description']
            raise RefreshError(f"Token refresh failed: {error_description}")
        except Exception as e:
            raise RefreshError(f"Token refresh failed: {str(e)}")
        return credentials

    
    def refresh_auth_token(self):
        if self.credentials is None:
            logger.error("Credentials not set. Please set the credentials before refreshing the token.")
            return
        
        try:
            self.credentials = self.refresh_google_auth_token(self.credentials)
            logger.info("Authentication token refreshed")
        except RefreshError as e:
            logger.error(str(e))

    
    
    logger.info("Proses selesai")
