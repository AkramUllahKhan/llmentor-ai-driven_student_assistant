from services.chroma_service import ChromaService

# use this to load the data into the Chroma vector store only needed once
ChromaService().loader()
