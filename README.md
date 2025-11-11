# RAG  sobre Historia de la Humanidad

Este proyecto implementa un sistema de Recuperación Aumentada por Generación (RAG) para consultar información sobre la historia de la humanidad. Utiliza Pinecone como base de datos vectorial y modelos de OpenAI para generar respuestas precisas basadas en los datos almacenados.

## 📋 Características

- Búsqueda semántica de información histórica
- Respuestas generadas por IA basadas en contexto relevante
- Almacenamiento de vectores para búsquedas eficientes
- Interfaz de línea de comandos interactiva
- Especializado en temas históricos: civilizaciones, guerras, imperios, religión, arte, ciencia y cultura

## 🚀 Requisitos

Antes de comenzar, asegúrate de tener instalado:

- Python 3.9
- [Pip](https://pip.pypa.io/en/stable/) (gestor de paquetes de Python)
- Una cuenta en [OpenAI](https://platform.openai.com/) para obtener una API key
- Una cuenta en [Pinecone](https://www.pinecone.io/) para el almacenamiento vectorial

## 🔧 Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/tu-usuario/arep-taller8-RAG.git
   cd arep-taller8-RAG
   ```

2. Crea y activa un entorno virtual (recomendado):

   ```bash
   python -m venv venv
   # En Windows:
   .\venv\Scripts\activate
   # En macOS/Linux:
   source venv/bin/activate
   ```

3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

   ```
   OPENAI_API_KEY=tu_api_key_de_openai
   PINECONE_API_KEY=tu_api_key_de_pinecone
   ```

## 🏃 Ejecución

### 1. Cargar datos a Pinecone

Asegúrate de tener un archivo `data/documentos.json` en el proyecto con los datos históricos. Luego ejecuta:

```bash
python indexation.py
```

Este script creará un índice en Pinecone llamado `mi-base-conocimiento` y cargará los datos históricos, dividiéndolos en fragmentos para una búsqueda más eficiente.

### 2. Ejecutar el sistema RAG

Para iniciar el sistema de preguntas y respuestas:

```bash
python use.py
```

Una vez iniciado, podrás hacer preguntas sobre historia de la humanidad y el sistema buscará en la base de conocimiento para darte respuestas precisas basadas en los documentos indexados.

**Ejemplos de preguntas:**
- "¿Cuáles fueron las principales civilizaciones antiguas?"
- "Explícame sobre la Revolución Industrial"
- "¿Qué fueron las Cruzadas?"

Escribe `salir`, `exit` o `quit` para terminar la sesión.

## 🛠️ Estructura del proyecto

- `indexation.py`: Script para cargar y indexar documentos históricos en Pinecone
- `use.py`: Script principal que implementa la lógica del sistema RAG con agente conversacional
- `data/documentos.json`: Archivo de datos con información sobre historia de la humanidad
- `requirements.txt`: Dependencias del proyecto
- `.env`: Archivo para variables de entorno (no incluido en el repositorio)
- `assets/`: Carpeta con imágenes de evidencia del proyecto

## 📝 Notas adicionales

- Asegúrate de que tu archivo `data/documentos.json` tenga el formato correcto con los campos necesarios: `id`, `titulo`, `contenido` y `metadata`.
- El sistema está configurado para usar el modelo `gpt-4o-mini` de OpenAI y `text-embedding-3-small` para los embeddings.
- Los documentos se dividen automáticamente en fragmentos de 1000 caracteres con un solapamiento de 200 caracteres para mejorar la precisión de las búsquedas.
- El índice de Pinecone utiliza la métrica de similitud coseno y tiene una dimensión de 1536 (compatible con `text-embedding-3-small`).
- Puedes ajustar los parámetros de búsqueda en `use.py` según tus necesidades (por ejemplo, cambiar `k=3` en `similarity_search` para obtener más o menos resultados).

## Evidencia

![alt text](assets/img0.png)

![alt text](assets/img1.png)

![alt text](assets/img2.png)
