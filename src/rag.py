# import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain_google_genai.chat_models import ChatGoogleGenerativeAIError
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
import data_base
import config

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
load_dotenv()

class ChatHistory:
    def __init__(self, window_size = 20, buffer_size = 40):
        self.summary = ""
        self.prev_messages = []
        self.window_size = window_size
        self.buffer_size = buffer_size
        self.model = ChatGoogleGenerativeAI(model = 'gemini-3.5-flash', 
                                            api_key = os.getenv("API_KEY"), 
                                            temperature=0.7)
        prompt = PromptTemplate.from_template(config.prompt_summerize)
        self.summary_chain = (prompt | self.model | StrOutputParser())

    
    def add_one_to_history(self, message, isHumanMessage):
        if isHumanMessage:
            self.prev_messages.append(HumanMessage(message))
        else:
            self.prev_messages.append(AIMessage(message))

        if len(self.prev_messages) >= self.buffer_size:
            cutoff = min(self.window_size, len(self.prev_messages))
            self.summerize(self.prev_messages[0:cutoff])
            n = len(self.prev_messages)-1
            #keep the last half messages as they are
            self.prev_messages = self.prev_messages[n-self.window_size:n] 


    def add_many_to_history(self, messages):
        self.prev_messages = [HumanMessage(message['message']) 
                              if message.get('messenger') == 'human' 
                              else AIMessage(message['message']) 
                              for message in messages]
        
        if len(self.prev_messages) > self.window_size:
            cutoff = min(self.window_size, len(self.prev_messages))
            self.summerize(self.prev_messages[0:cutoff])
            self.prev_messages = self.prev_messages[-self.window_size:]


    def set_chat_history(self, chat_history):
        self.prev_messages = chat_history
            
    def clear_history(self):
        self.prev_messages.clear()
        self.summary = ""

    
    def summerize(self, chat_history):
        if not chat_history and not self.summary:
            return
        formatted_lines = []
        for message in chat_history:
            if isinstance(message, HumanMessage):
                formatted_lines.append(f"User: {message.content}")
            else:
                formatted_lines.append(f"AI: {message.content}")
                
        get_string = "Previous summary: " + self.summary + "\n" + "\n".join(formatted_lines)
        response = self.summary_chain.invoke({"context": get_string})
        self.summary = response


    
    def get_chat_history(self):
        if self.summary: 
            history = [item for item in self.prev_messages]
            history.insert(0, SystemMessage(f"Previous chat summary: {self.summary}"))
            return history
        return self.prev_messages

class RagChain():
    def __init__(self, db = data_base.VectorDatabase(), model_id = 'gemini-3.5-flash'):
        self.model = ChatGoogleGenerativeAI(
            model = model_id, 
            api_key = os.getenv("API_KEY"), 
            temperature=0.7)

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

    # This function creates a query for the pubmed or creates a summary title depending on prompt_def arg passed to it
    def query_database(self, user_query, prompt_def):
        prompt = PromptTemplate.from_template(prompt_def)
        chain = prompt | self.model
        response = chain.invoke({"context": user_query})
        return response.content[0]["text"]
    
    def the_doc(self, paragraphs):
        return "\n".join([para.page_content for para in paragraphs])
    
