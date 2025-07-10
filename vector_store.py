import pandas as pd
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.docstore.document import Document
from dotenv import load_dotenv
import os
import sys
import shutil

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ ERROR: OPENAI_API_KEY not found.")
    sys.exit(1)
print("✅ OPENAI_API_KEY loaded.")

# Set vector DB directory
persist_dir = "chroma_ayurvedic_db"
if os.path.exists(persist_dir):
    print(f"⚠️ Removing old vector store at '{persist_dir}'.")
    shutil.rmtree(persist_dir)

# Load your dataset
df = pd.read_csv("data/ayurvedic_medicines_10k.csv")
df.columns = df.columns.str.strip()

# Create documents for embedding
documents = []
for _, row in df.iterrows():
    content = f"""{row['Medicine_Name']} is an Ayurvedic medicine in the form of {row['Form']}, manufactured by {row['Manufacturer']}. 
It is primarily used for {row['Used_For']} and contains main ingredients such as {row['Main_Ingredients']}. 
The recommended dosage is {row['Dosage']}. This medicine is currently {row['Availability_Status'].lower()} and priced at ₹{row['Price']}.
It has an expiry date of {row['Expiry_Date']} and is marked as '{row['Approval_Status']}'.
Reported side effects include: {row['Side_Effects']}."""
    
    documents.append(Document(page_content=content))

# Initialize embeddings
embedding = OpenAIEmbeddings(model="text-embedding-3-small")

# Create and persist the vector store
vectordb = Chroma.from_documents(
    documents=documents,
    embedding=embedding,
    persist_directory=persist_dir
)
vectordb.persist()

print("✅ Vector store created successfully from your 10K Ayurvedic dataset.")
