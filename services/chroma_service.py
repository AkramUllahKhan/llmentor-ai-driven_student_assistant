import os
import time
import shutil
from tqdm import tqdm
from dotenv import load_dotenv
from utils.custom_logger import log
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
import requests
import threading
from concurrent.futures import ThreadPoolExecutor
load_dotenv()


class ChromaService:
    def loader(self):
        try:
            start_time = time.time()
            
            # Initialize the embeddings function from OpenAI
            embeddings = OpenAIEmbeddings()

            # Initialize the Chroma vector store
            log.info("Initializing Chroma vector store")
            if os.path.exists("./chromadb"):
                log.info("Removing existing Chroma vector store")
                shutil.rmtree("./chromadb")
            vectorstore = Chroma(
                persist_directory="./chromadb",
                embedding_function=embeddings,
                collection_name="uet"
            )

            log.info("Scraping Links")
            all_chunks = []
            DATASET = []
            links = [
                'https://www.uetpeshawar.edu.pk/',
                'https://www.uetpeshawar.edu.pk/vision-mission.php',
                'https://www.uetpeshawar.edu.pk/statutes&rules.php',
                'https://www.uetpeshawar.edu.pk/vcwelcome.php',
                'https://www.uetpeshawar.edu.pk/aboutuet.php',
                'https://www.uetpeshawar.edu.pk/facultyece.php',
                'https://www.uetpeshawar.edu.pk/facultymcie.php',
                'https://www.uetpeshawar.edu.pk/facultycame.php',
                'https://www.uetpeshawar.edu.pk/facultyaah.php',
                'http://uspcase.uetpeshawar.edu.pk/',
                'https://www.uetpeshawar.edu.pk/aral/index.html',
                'https://www.uetpeshawar.edu.pk/cdc.php',
                'https://www.uetpeshawar.edu.pk/cec/index.html',
                'https://cisnr.com/',
                'https://www.uetpeshawar.edu.pk/eec.php',
                'https://www.uetpeshawar.edu.pk/emnet/emnet.htm',
                'https://www.uetpeshawar.edu.pk/itc.php',
                'https://www.facebook.com/NIUIP',
                'https://www.uetpeshawar.edu.pk/oric/index.php',
                'https://www.uetpeshawar.edu.pk/STAMP/index.html',
                'https://www.uetpeshawar.edu.pk/tic/tic.html',
                'https://www.uetpeshawar.edu.pk/ncbc/index.html',
                'https://www.uetpeshawar.edu.pk/haina.php',
                'http://ncai.cisnr.com/',
                'http://www.enggentrancetest.pk/uet/',
                'https://www.uetpeshawar.edu.pk/dpgs/index.php',
                'https://www.uetpeshawar.edu.pk/abbottabad.php',
                'https://www.uetpeshawar.edu.pk/bannu.php',
                'https://www.uetpeshawar.edu.pk/jalozai.php',
                'https://www.uetpeshawar.edu.pk/kohat.php',
                'https://www.uetpeshawar.edu.pk/cms/index.html',
                'https://www.uetpeshawar.edu.pk/online_class.php',
                'https://www.uetpeshawar.edu.pk/qec-new/index.html',
                'https://www.uetpeshawar.edu.pk/oric/index.php',
                'https://www.uetpeshawar.edu.pk/cdc.php',
                'http://bit.ly/UETP-Alumni-Registration',
                'https://www.uetpeshawar.edu.pk/downloads.php',
                'https://www.uetpeshawar.edu.pk/contactus.php'
            ]
            for url in tqdm(links):
                html_content = self.fetch_html(url)
                if html_content:
                    chunks = self.split_into_chunks(html_content)
                    all_chunks.extend(chunks)   
            if all_chunks:
                log.info("Loading Links into VectorDatabase")
                for i in tqdm(all_chunks):
                    Chroma.add_texts(vectorstore,[i])
            root_path = './dataset'
            DATASET = []
            items = os.listdir(root_path)
            for i in items:
                loader = PyPDFLoader(f"{root_path}/{i}")
                pages = loader.load_and_split()
                DATASET.extend(pages)
            if DATASET:
                log.info("Loading PDF into VectorDataBase")
                for i in tqdm(DATASET):
                    Chroma.add_texts(vectorstore, [i.page_content])

            log.info("Data loaded successfully")
            log.warning(f"Time taken to load data: {round(time.time() - start_time, 2)} seconds")
        except Exception as e:
            log.error(f"Error in loader: {e}", exc_info=True)

    def retriver(self, question, k=4):
        try:
            start_time = time.time()
            # Initialize the embeddings function from OpenAI
            embeddings = OpenAIEmbeddings()
            vectorstore = Chroma(
                persist_directory="./chromadb",
                embedding_function=embeddings,
                collection_name="uet"
                )
            log.info("Retrieving documents from Chroma vector store")
            DOCS = []
            for i in vectorstore.similarity_search(question, k=k):
                DOCS.append(i.page_content)
            if len(DOCS) == 0:
                DOCS.append("Sorry, I couldn't find any relevant documents")
            log.warning(f"Time taken to retrieve documents: {round(time.time() - start_time,2)} seconds")
            return DOCS
        except Exception as e:
            log.error(f"Error in retriver: {e}", exc_info=True)
            return ["Sorry, I couldn't find any relevant documents"]


    def fetch_html(self,url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.text
            else:
                return ''
        except Exception as e:
            log.info(f"Error fetching {url}: {e}")
            return ''

    def split_into_chunks(self,text, chunk_size=4000):
        return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
