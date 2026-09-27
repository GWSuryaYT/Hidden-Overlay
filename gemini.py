from google import genai
from dotenv import load_dotenv
import os
import chromadb
from chunker import chunky
import uuid

#Enable or disbale the context memory:
context = True #this will save the contexts in the database using chromadb :> will cost api and some time too bcz in background many stuffs are doing its job :>
previousmsg = False #recomended
both = False


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
    for one_chunk in all_text_chunks:

        collection.add(
            ids = [str(uuid.uuid4())],
            documents= [one_chunk],
            embeddings= [gemini_encodding(one_chunk)]
        )

def context_call(text, top_k:int=2):
    embedding = gemini_encodding(text=text)
    query_results = collection.query(
        query_embeddings= [embedding],
        n_results= top_k
    )
    docs = query_results.get('documents', [[]])[0]
    return "\n".join(docs)

def response(text:str, previous_msg):
    if previousmsg:
        interaction = ai_client.interactions.create(
            input= f'''You are a helpful ai assistant who help users requests. User Query: {text}
Privous message: {previous_msg}''',
            model="gemini-3.1-flash-lite"
         )
        results = interaction.output_text
    elif context:
        interaction = ai_client.interactions.create(
            input= f'''You are a helpful ai assistant who help users requests. User Query: {text}
contexts {context_call(text=text)}''',
            model="gemini-3.1-flash-lite"
        )
        #first store the user's query
        store(paragraph=text)
        #now store the results
        results = interaction.output_text
        store(paragraph=results)

    elif both:
        interaction = ai_client.interactions.create(
            input= f'''You are a helpful ai assistant who help users requests. User Query: {text}
previous message: {str(previous_msg)}
contexts {context_call(text=text)}''',
            model="gemini-3.1-flash-lite"
        )
        #first store the user's query
        store(paragraph=text)
        #now store the results
        results = interaction.output_text
        store(paragraph=results)  
    #now we will save the data here:
    return results
