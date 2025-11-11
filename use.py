import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain.tools import tool

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = "mi-base-conocimiento"

if not OPENAI_API_KEY or not PINECONE_API_KEY:
    raise EnvironmentError("Falta configurar OPENAI_API_KEY o PINECONE_API_KEY en el archivo .env")

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    openai_api_key=OPENAI_API_KEY
)

vector_store = PineconeVectorStore(
    index_name=INDEX_NAME,
    embedding=embeddings,
    pinecone_api_key=PINECONE_API_KEY
)

model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    request_timeout=30,
    max_retries=2,
    openai_api_key=OPENAI_API_KEY
)

@tool
def buscar_contexto(consulta: str) -> str:
    """Busca información relevante en la base de conocimiento sobre historia de la humanidad."""
    try:
        documentos = vector_store.similarity_search(consulta, k=3)

        if not documentos:
            return "No se encontraron documentos históricos relevantes."

        resultados = []
        for doc in documentos:
            titulo = doc.metadata.get("titulo", "Sin título")
            categoria = doc.metadata.get("categoria", "N/A")
            autor = doc.metadata.get("autor", "Desconocido")
            contenido = doc.page_content[:500].strip().replace("\n", " ")
            resultados.append(
                f"📜 **{titulo}**\nCategoría: {categoria}\nAutor: {autor}\nFragmento: {contenido}..."
            )

        return "\n\n".join(resultados)

    except Exception as e:
        return f"⚠️ Error al buscar en Pinecone: {str(e)}"


tools = [buscar_contexto]

prompt = ChatPromptTemplate.from_messages([
    ("system",
     "Eres un historiador experto con acceso a una base de conocimiento sobre la historia de la humanidad. "
     "Usa la herramienta de búsqueda cuando sea necesario para encontrar información sobre civilizaciones antiguas, "
     "procesos históricos, guerras, imperios, cultura, religión, arte, ciencia y evolución social. "
     "Responde siempre en español, con precisión y de manera didáctica, "
     "incluyendo contexto histórico cuando sea apropiado."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)

def hacer_pregunta(pregunta: str):
    """Envía una pregunta al agente histórico."""
    print(f"\n❓ Pregunta: {pregunta}\n")
    print("📚 Respuesta:\n")

    try:
        respuesta = agent_executor.invoke({"input": pregunta})
        print(respuesta["output"])
    except Exception as e:
        print(f"⚠️ Error al procesar la pregunta: {str(e)}")

if __name__ == "__main__":
    print("=" * 65)
    print(" 🏛️  Sistema RAG con Pinecone y ChatGPT ")
    print(" 🕰️  Especializado en Historia de la Humanidad ")
    print("=" * 65)
    print("\nTemas: civilizaciones | guerras | imperios | religión | arte | ciencia | cultura")
    print("Escribe 'salir' para terminar.\n")

    while True:
        pregunta = input("💬 Tu pregunta: ").strip()
        if pregunta.lower() in {"salir", "exit", "quit"}:
            print("\n👋 ¡Hasta luego, amante de la historia!\n")
            break

        if pregunta:
            hacer_pregunta(pregunta)
