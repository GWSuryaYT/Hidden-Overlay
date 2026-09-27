from google import genai
from dotenv import load_dotenv
import os
import chromadb
from chunker import chunky

chunk = chunky()

chroma = chromadb.PersistentClient('./context_store')
collection = chroma.get_or_create_collection(name='VectorStorage')

load_dotenv()


def api():
    return os.getenv("GEMINI_KEY")

print(api())

ai_client = genai.Client(api_key=api())



def gemini_encodding(text):

    encoddings = ai_client.models.embed_content(
        model="gemini-embedding-2",
        contents= text,
    )
    results = encoddings.embeddings
    result_vector = results[0].values

    return result_vector


def store(paragraph:str, chunk_size:int=20, overlap:int=10):

    #get the chunks = 
    all_text_chunks = chunk.chunk_maker(paragraph=paragraph, overlap=overlap,chunk_size=chunk_size)

    #now we can just save them one by one
    id_chunk =1
    for one_chunk in all_text_chunks:

        collection.add(
            ids = str(id_chunk),
            documents= one_chunk,
            embeddings= gemini_encodding(one_chunk)
        )
        id_chunk+=1

def context_call(text, top_k:int=2):
    embedding = gemini_encodding(text=text)
    query_results = collection.query(
        query_embeddings= [embedding],
        n_results= top_k
    )

    return query_results

def response(text):

    interaction = ai_client.interactions.create(
        input= f'''You are a helpful ai assistant who help users requests. User Query: {text}
Context of similar type: {context_call(text=text)}''', # we will make it a function tool later.
        model="gemini-3.1-flash-lite"
    )

    #now we will save the data here:
    
    #first save the input text
    store(paragraph=text)
    results = interaction.output_text
    store(paragraph=results)
    return results
