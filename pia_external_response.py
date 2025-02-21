import os
import torch
import datetime
import time

# Langchain 
from langchain.chains import create_tagging_chain
from langchain import HuggingFacePipeline
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# Prompt templates
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import PromptTemplate
# Chains
from langchain.chains import LLMChain
from langchain.chains import SimpleSequentialChain
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
## ConversationBufferWindowMemory
from langchain.memory import ConversationBufferWindowMemory
# Q&A over documents

from langchain.vectorstores import DocArrayInMemorySearch
from IPython.display import display, Markdown

from langchain.indexes import VectorstoreIndexCreator

from langchain.indexes.vectorstore import VectorstoreIndexCreator 

# Chatbot
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.memory import ConversationBufferMemory
from langchain_community.document_loaders.pdf import PyPDFLoader

from langchain_together import ChatTogether

from pia_internal_processing import pia_internal_processing

class pia_response_generation(pia_internal_processing):
    def __init__(self):
        super().__init__()
        self.initiate_pia()
        self.bio_prompt = """"""

    def output_user_info(self):
        user_info_str = """\
             {bio}
             """.format(bio = self.bio_prompt)
        user_info_str += self.get_user_info_string()
        return user_info_str
    
    def generate_meal_plan(self):
        meal_plan_prompt_temp = self.prompt_templates["dialogue_states_prompt_templates"]["meal_plan_prompt_template"]
        meal_plan_prompt = ChatPromptTemplate.from_template(meal_plan_prompt_temp)
        meal_plan_chain = meal_plan_prompt | self.pia_chat_model
        response = meal_plan_chain.invoke({"user_info": self.user_info_prompt})
        # Move to internal processing
        # if self.current_meal_plan:
        #     self.meal_plan_history[self.current_meal_plan["Timestamp"]] = self.current_meal_plan["meal_plan"] 
        # self.current_meal_plan["Timestamp"] = "Meal_plan_{}".format(time.time())
        # self.current_meal_plan["meal_plan"] = response.content
        return response.content
    
    def generate_consolidated_nutrition_advice(self):
        cons_nutrition_advice_prompt_temp = self.prompt_templates["dialogue_states_prompt_templates"]["consolidated_nutrition_advice_template"]
        cons_nutrition_advice_prompt = ChatPromptTemplate.from_template(cons_nutrition_advice_prompt_temp)
        cons_nutrition_advice_chain = cons_nutrition_advice_prompt | self.pia_chat_model
        response = cons_nutrition_advice_chain.invoke({"user_info": self.user_info_prompt})
        return response.content
    
    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        store = self.store
        if session_id not in store:
            store[session_id] = InMemoryChatMessageHistory()
        return store[session_id]
    
    def response_prompt(self, action, message):
        pia_personalised_prompt = self.prompt_templates["pia_prompt"] + self.user_info_prompt
        return pia_personalised_prompt

    def pia_response(self, prompt, message):
    # def pia_response(self, message, chat_history):
        # pass modified prompt
        pia_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system", prompt
                ),
                MessagesPlaceholder(variable_name="messages")
            ]
        )
        runnable = pia_prompt | self.pia_chat_model
        with_message_history = RunnableWithMessageHistory(runnable, self.get_session_history)
        config = {"configurable": {"session_id": "abc2"}}
        response = with_message_history.invoke([HumanMessage(content=message)],
                                              config = config)
        return response

    def pia_chat_old(self, message, history):
        history_langchain_format = []
        for user, pia in history:
            history_langchain_format.append(HumanMessage(content=user))
            history_langchain_format.append(SystemMessage(content=pia))
        history_langchain_format.append(HumanMessage(content=message))
        action = self.pia_categorise_input(message)
        response_prompt = self.response_prompt(action, message)
        self.pia_understand_user(action, message)
        response = self.pia_response(response_prompt, message)

        for word in response.split():
            yield word + " "
            time.sleep(0.05)
        # chat_history.append((message, response))
