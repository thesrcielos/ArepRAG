import json
import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from pinecone import Pinecone, ServerlessSpec

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = "mi-base-conocimiento"


def cargar_documentos(ruta_json):
    with open(ruta_json, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    documentos = []
    for item in datos:
        contenido = f"Título: {item['titulo']}\n\n{item['contenido']}"
        metadata = item["metadata"]

        documentos.append(
            Document(
                page_content=contenido,
                metadata={
                    "id": item["id"],
                    "titulo": item["titulo"],
                    "categoria": metadata["categoria"],
                    "subcategoria": metadata["subcategoria"],
                    "fecha": metadata["fecha"],
                    "autor": metadata["autor"],
                    "nivel": metadata["nivel"],
                    "tags": ", ".join(metadata["tags"]),
                    "idioma": metadata["idioma"],
                    "tiempo_lectura": metadata["tiempo_lectura"]
                },
            )
        )
    return documentos


def crear_indice():
    pc = Pinecone(api_key=PINECONE_API_KEY)
    if INDEX_NAME not in pc.list_indexes().names():
        print(f"Creando índice '{INDEX_NAME}'...")
        pc.create_index(
            name=INDEX_NAME,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
        print(f"Índice '{INDEX_NAME}' creado correctamente.")
    else:
        print(f"El índice '{INDEX_NAME}' ya existe.")


def indexar_conocimiento(ruta_json):
    print("\nCargando documentos...")
    documentos = cargar_documentos(ruta_json)
    print(f"{len(documentos)} documentos cargados.")

    print("\nDividiendo documentos en fragmentos...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200, add_start_index=True
    )
    fragmentos = splitter.split_documents(documentos)
    print(f"{len(fragmentos)} fragmentos generados.")

    print("\nConfigurando Pinecone...")
    crear_indice()

    print("\nCreando embeddings...")
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small", openai_api_key=OPENAI_API_KEY
    )

    print("\nIndexando documentos en Pinecone...")
    vector_store = PineconeVectorStore.from_documents(
        documents=fragmentos,
        embedding=embeddings,
        index_name=INDEX_NAME
    )

    print("\nIndexación completada con éxito.")
    return vector_store


if __name__ == "__main__":
    ruta_archivo = "data/documentos.json"

    if not os.path.exists(ruta_archivo):
        print(f"Error: No se encontró el archivo {ruta_archivo}")
        print("Verifica la ruta y vuelve a intentarlo.")
        exit(1)

    store = indexar_conocimiento(ruta_archivo)
    print(f"\nTu base de conocimiento está lista en Pinecone. (índice: {INDEX_NAME})")
