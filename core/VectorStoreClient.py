from langchain.vectorstores import Chroma
import os

class Client:
    def __init__(self, resources:list[dict],collection_name):
        self.resources = resources      
        self.collection_name=collection_name

    """ 
        Evaluador de existencia de la colleccion en la base de datos vectorial
    """
    def has_data(self):
        ruta = f"core\persists\{self.collection_name}"
        return os.path.exists(ruta)
    
   
    """
        metodo para formatear un recurso a texto
    """
    def get_text_for_resource(self,resource:dict):
        text = ""
        for (key,value) in resource.items():
            text+=f"{key}: {value}\n"
        return text

    """
    def get_documents_for_resources(self):
        docs = []
        for resource in self.resources:
            doc =  Document(page_content=self.get_text_for_product(resource), metadata={'source':self.get_text_for_product(resource)})
            docs.append(doc)
        return docs
    """

    def get_texts_for_resources(self):
        texts = []
        for resource in self.resources:
            text =  self.get_text_for_resource(resource)
            texts.append(text)
        return texts       
    
    def create_collection(self,embedding_model):
        ruta = f"core\persists\{self.collection_name}"
        if(self.has_data()):
            self.vectordb = Chroma(persist_directory = ruta, collection_name=self.collection_name, embedding_function= embedding_model)
        else:
            texts = self.get_texts_for_resources()
            ids = [str(resourse['id']) for resourse in self.resources]
            self.vectordb = Chroma.from_texts(texts=texts,persist_directory = ruta, metadatas=self.resources,embedding = embedding_model, collection_name=self.collection_name, ids = ids)
            print('Embeddings completed!')
        return self.vectordb
    
    def delete_collection(self):
        ruta = f"core\persists\{self.collection_name}"