from langchain.embeddings import HuggingFaceEmbeddings
from core.VectorStoreClient import Client
from core.Agent import RecommenderAgent
from langchain.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME")
ENCODE_KWARGS = {'normalize_embeddings': True} # set True to compute cosine similarity
MODEL_KWARGS = {'device': 'cpu'}

LLAMA_MODEL_NAME = os.getenv("LLAMA_MODEL_NAME")
LLAMA_MODEL_BASENAME = os.getenv("LLAMA_MODEL_BASENAME")

OPENAI_MODEL_NAME = "gpt-3.5-turbo-1106"# os.getenv("OPENAI_MODEL_NAME")
OPENAI_KEY = "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"#os.getenv("OPENAI_API_KEY")


class CoreRecommendation:
    def __init__(self) -> None:
        self.embeddingModel = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL_NAME,
            encode_kwargs=ENCODE_KWARGS,
            model_kwargs=MODEL_KWARGS
        )
        if(OPENAI_KEY!=''):
            print(f"model name = {OPENAI_MODEL_NAME}")
            self.llm = ChatOpenAI(temperature=0.3, model_name=OPENAI_MODEL_NAME,api_key = OPENAI_KEY)
        else:
            from langchain.callbacks.manager import CallbackManager
            from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
            from langchain.llms import LlamaCpp
            from huggingface_hub import hf_hub_download

            model_path = hf_hub_download(repo_id=LLAMA_MODEL_NAME, filename=LLAMA_MODEL_BASENAME)
            callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
            self.llm = LlamaCpp(
                model_path=model_path,
                callback_manager=callback_manager,
                verbose=True, # Verbose is required to pass to the callback manager
                temperature=0.0,
                n_batch=2,
                n_ctx=8000#15000
            )
            

    def init_components(self,collection_name:str,resources:list[dict]):
        self.resourcesClient = Client(resources=resources,collection_name=collection_name)
        vectordb = self.resourcesClient.create_collection(embedding_model=self.embeddingModel)
        self.agent = RecommenderAgent(vectordb=vectordb,llm=self.llm)
        self.agent.initAgent()
    
    def get_recommendation(self,user):
        text = self.get_text_for_user(user=user)
        response = self.agent.executeAgent(string=text)
        return tuple((user, response))
    
    def get_recommendatios(self,users):
        responses = []
        for user in users:
            response = self.get_recommendation(user=user)
            responses.append(response)
        return responses


    def get_text_for_user(self,user:dict):
        text = "{\n"
        for (key,value) in user.items():
            text+=f"{key}: {value}\n"
        text+="}\n"
        return text

  