import os
import datetime
import time
from dotenv import load_dotenv

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
# Q&A over documentse
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.document_loaders import CSVLoader
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

from pia_prompts import pia_prompt_templates

load_dotenv()


class pia_internal_processing(pia_prompt_templates):
    def __init__(self):
        super().__init__()
        self.initiate_pia()
        self.store = {}
        self.current_user_count = 0
        self.users = {}
        self.bio_prompt = """"""

    def initiate_pia(self):
        # llm = HuggingFaceEndpoint(
        # repo_id="meta-llama/Meta-Llama-3-8B-Instruct",
        # task="text-generation",
        # max_new_tokens=512,
        # do_sample=False,
        # repetition_penalty=1.03,
        # )
        # self.pia_chat_model = ChatHuggingFace(llm=llm)

        # Define model
        self.pia_chat_model = ChatTogether(
        together_api_key = os.getenv("TOGETHER_API_KEY"),
        model="meta-llama/Meta-Llama-3-70B-Instruct-Lite",
        )
    
    def pia_dialogue_state_tracking(self, message):
        dialogue_state_tracking_prompt = self.dialogue_state_tracking_prompt_template()
        chain = dialogue_state_tracking_prompt | self.pia_chat_model
        response = chain.invoke(input = message) #.split('\n')[0].lstrip()
        action = response.content
        return action
        
    # Identify, store and respond to user's new goal
    # To do - confirm the identified goal?
    def identify_user_goals(self, message):
        goals_prompt = self.prompt_templates["dialogue_states_prompt_templates"]["goals_prompt_template"]
        goals_prompt_temp = ChatPromptTemplate.from_messages({goals_prompt})
        goal_chain = goals_prompt_temp | self.pia_chat_model
        response = goal_chain.invoke(message)
        goal = response.content
        return goal
        
    def identify_health_issues(self, message):
        health_issue_prompt = self.prompt_templates["dialogue_states_prompt_templates"]["health_issue_prompt_template"]
        health_issue_prompt_temp = ChatPromptTemplate.from_messages({health_issue_prompt})
        health_issue_chain = health_issue_prompt_temp | self.pia_chat_model
        response = health_issue_chain.invoke(message) 
        health_issue = response.content
        return health_issue
    
    def identify_user_like(self, message):
        user_like_prompt = self.user_likes_prompt()
        user_like_prompt_temp = ChatPromptTemplate.from_messages({user_like_prompt})
        user_like_chain = user_like_prompt_temp | self.pia_chat_model
        response = user_like_chain.invoke(message) 
        user_like = response.content
        return user_like
    
    def identify_user_dislike(self, message):
        user_dislike_prompt = self.user_likes_prompt()
        user_dislike_prompt_temp = ChatPromptTemplate.from_messages({user_dislike_prompt})
        user_dislike_chain = user_dislike_prompt_temp | self.pia_chat_model
        response = user_dislike_chain.invoke(message) 
        user_dislike = response.content
        return user_dislike

    def track_user_goals(self, message):
        goal = self.identify_user_goals(message)
        # goal = goal.split('\n')[0]
        if goal not in self.current_user["current_goals"].keys():
            self.current_user["current_goals"][goal] = {"start_date": time.time(), "chat_message": message} # Store the identified goal      

    def track_user_health_issues(self, message):
        health_issue = self.identify_health_issues(message)
        if health_issue not in self.current_user["current_health_issues"].keys():
            self.current_user["current_health_issues"][health_issue] = {"start_date": time.time(), "chat_message": message} # Store the identified goal

    def track_user_preferences(self, message):
        user_preferences_tracking_prompt = self.user_preferences_tracking_prompt()
        chain = user_preferences_tracking_prompt | self.pia_chat_model
        response = chain.invoke(input = message) #.split('\n')[0].lstrip()
        preference_type = response.content
        if preference_type == "Likes":
            user_like = self.identify_user_like(message)
            self.current_user["preferences"]["likes"][user_like] = {"start_date": time.time(), "chat_message": message} 
        elif preference_type == "Dislikes":
            user_dislike = self.identify_user_dislike(message)
            self.current_user["preferences"]["dislikes"][user_dislike] = {"start_date": time.time(), "chat_message": message}

    def pia_understand_user(self, dialogue_state, message):
        if dialogue_state == "Health and lifestyle goals":
            self.track_user_goals(message)
        elif dialogue_state == "Health issues and illnesses":
            self.track_user_health_issues(message)
        elif dialogue_state == "Track user preferences":
            self.track_user_preferences(message)
        else:
            pass
        self.user_info_prompt = self.get_user_info_prompt()

    def get_info_string_from_list(self, list):
        str = ""
        for i in range(len(list)):
            str += list[i]
            if i != (len(list)-1):
               str += ", "    
        return str

    def get_user_info_string(self):
        goals = list(self.current_user["current_goals"].keys())
        health_issues = list(self.current_user["current_health_issues"].keys())
        likes = list(self.current_user["preferences"]["likes"].keys())
        dislikes = list(self.current_user["preferences"]["dislikes"].keys())
        user_info_string = """"""
        
        if goals:
            goals_string = self.get_info_string_from_list(goals)
            user_info_string += self.prompt_templates["user_info_prompts"]["current_goals_prompt"].format(goals = goals_string)
            
        if health_issues:
            current_health_issues_string = self.get_info_string_from_list(health_issues)
            user_info_string += self.prompt_templates["user_info_prompts"]["current_health_issues_prompt"].format(
                health_issues = current_health_issues_string)
            
        if likes or dislikes:
            user_preferences_prompt = self.prompt_templates["user_info_prompts"]["user_preferences_prompt"]
            if likes:
                user_likes_string = self.get_info_string_from_list(likes)
                user_preferences_prompt += self.prompt_templates["user_info_prompts"]["user_likes_prompt"].format(
                    likes = user_likes_string)
            if dislikes:
                user_dislikes_string = self.get_info_string_from_list(dislikes)
                user_preferences_prompt += self.prompt_templates["user_info_prompts"]["user_dislikes_prompt"].format(
                    dislikes = user_dislikes_string)
            user_info_string += user_preferences_prompt
        return user_info_string
        

    def get_user_info_prompt(self):
        if self.current_user: 
            user_info_prompt_template = self.prompt_templates["user_info_prompts"]["user_info_prompt_base"]
            user_info_prompt = user_info_prompt_template.format(
                name = self.bio_hash["name"], user_bio = self.bio_prompt)
            user_info_string = self.get_user_info_string()
            user_info_prompt += user_info_string
            return user_info_prompt
        else:
            return ""
    
    