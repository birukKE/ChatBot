# import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAI, ChatGoogleGenerativeAI 
from langchain_google_genai.chat_models import ChatGoogleGenerativeAIError
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline
import data_base
import config
import env_config

# from langchain.prompts import ChatPromptTemplate 
from langgraph.checkpoint.memory import InMemorySaver  
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate


class ChatHistory:
    def __init__(self, window_size = 20, buffer_size = 40):
        self.summary = ""
        self.chat_history = []
        self.window_size = window_size
        self.buffer_size = buffer_size
    
    def add_one_to_history(self, message, isHumanMessage):
        if isHumanMessage:
            self.chat_history.append(HumanMessage(message))
        else:
            self.chat_history.append(AIMessage(message))

        if len(self.chat_history) >= self.buffer_size:
            self.summerize(self.chat_history)
            n = len(self.chat_history)-1
            self.chat_history = self.chat_history[n-self.window_size:n]


    def set_chat_history(self, chat_history):
        self.chat_history = chat_history
            
    def clear_history(self):
        self.chat_history.clear()

    
    def add_many_to_history(self, messages):
        # message will look like [{'messenger': "human", "message": "hello"}, ...]
        self.chat_history = [HumanMessage(message['message']) if message.get('messenger') == 'human' else AIMessage(message['message']) for message in messages]
        if len(self.chat_history) > self.window_size:
            self.summerize(self.chat_history)
            self.chat_history = self.chat_history[-self.window_size:]

    def summerize(self, chat_history):
        cutoff = max(0, len(chat_history) - self.window_size)
        copy_list = chat_history[:cutoff]
        if not copy_list and not self.summary:
            return
        print("------------------------- ", copy_list)
        formatted_lines = []
        for message in copy_list:
            if isinstance(message, HumanMessage):
                formatted_lines.append(f"User: {message.content}")
            elif isinstance(message, AIMessage):
                formatted_lines.append(f"AI: {message.content}")
            else:
                formatted_lines.append(str(message))

        get_string = "Previous summary: " + self.summary + "\n" + "\n".join(formatted_lines)

        prompt = PromptTemplate.from_template(config.prompt_summerize)
        model = ChatGoogleGenerativeAI(model = 'gemini-3.5-flash', api_key = env_config.api_key, temperature=0.7)
        chain = prompt | model
        response = chain.invoke({"context": get_string})
        self.summary = response


    
    def get_chat_history(self):
        if self.summary: 
            history = [item for item in self.chat_history]
            history.insert(0, SystemMessage(f"Previous chat summary: {self.summary}"))
            return history
        return self.chat_history


class RagChain():
    def __init__(self, db = data_base.VectorDatabase(), model_id = 'gemini-3.5-flash'):
        self.model = ChatGoogleGenerativeAI(model = model_id, api_key = env_config.api_key, temperature=0.7)

        # self.chat_history = []
        self.chat_object = ChatHistory()
        self.retriever = db.vector_db.as_retriever()
        self.rag_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant. Use this contect:\n{context}"),
            # ("context", "{context}"),
            ("placeholder", "{chat_history}"),
            ("human", "{query}")
        ])

        self.rag_chain = (
                        {"context": self.retriever | self.the_doc, 
                         "chat_history": lambda _: self.chat_object.get_chat_history(),
                         "query": RunnablePassthrough()}
                        | self.rag_prompt
                        | self.model
                        | StrOutputParser()
                    )
    
    def query_gemini(self, query):
        try:
            response = self.rag_chain.invoke(query)
            self.chat_object.add_one_to_history(query, isHumanMessage=True)
            self.chat_object.add_one_to_history(response, isHumanMessage=False)
        except ChatGoogleGenerativeAIError as e:
            response = "You have either reached your Gemini API quotas or the server is overloaded. Try again later."
       
        return response

    # This function creates a query for the pubmed or creates a summary title
    # depending on prompt_def arg passed to it
    def query_database(self, user_query, prompt_def):
        prompt = PromptTemplate.from_template(prompt_def)
        chain = prompt | self.model
        response = chain.invoke({"context": user_query})
        return response.content[0]["text"]
    
    def the_doc(self, paragraphs):
        return "\n".join([para.page_content for para in paragraphs])
    

# rc = RagChain()
# if __name__ == "__main__":
#     rc = RagChain()

#     while True:
#         user_query = input("Your query: ")
#         response = rc.query_gemini(query=user_query)
#         print(f"Bot: {response}")
