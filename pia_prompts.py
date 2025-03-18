# Prompt template
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import PromptTemplate

class pia_prompt_templates():
    def __init__(self):
        self.prompt_templates = {
            "pia_prompt": self.pia_prompt_template(),
            "user_info_prompts": self.user_info_prompt_str(),
            "dialogue_state_tracking_prompt": self.dialogue_state_tracking_prompt_template(),
            "dialogue_states_prompts": self.dialogue_states_prompts(),
            "dialogue_states_prompt_templates": self.dialogue_states_prompt_templates(),
            "user_preferences_tracking_templates":  self.user_preferences_prompts()
        }

    def pia_prompt_template(self):
        pia_prompt_template = """\
        Your name is Pia, a friendly AI assistant playing the role of a nutrition coach. \
        Your job is to provide personalised nutrition and dietary advice based on the user information \
        that you have.
        """
        return pia_prompt_template

    def user_info_prompt_str(self):
        user_info_prompt_base = """\
        You are now in conversation with {name}

        This is the information about the user you have tracked so far:

        User bio:
        {user_bio}
        """
        
        current_goals_prompt = """
        Current health and lifestyle goals:\
        {goals}
        """

        current_health_issues_prompt = """
        Current health issues:\
        {health_issues}
        """

        user_preferences_prompt ="""
        User preferences:
        """
        user_likes_prompt = """
        Likes:\
        {likes}
        """
        user_dislikes_prompt = """
        Dislikes: \
        {dislikes}
        """

        user_info_prompts = {
            "user_info_prompt_base": user_info_prompt_base,
            "current_goals_prompt": current_goals_prompt,
            "current_health_issues_prompt": current_health_issues_prompt,
            "user_preferences_prompt": user_preferences_prompt,
            "user_likes_prompt": user_likes_prompt,
            "user_dislikes_prompt": user_dislikes_prompt
                            }
        return user_info_prompts
        

    def dialogue_state_tracking_prompt_template(self):
        dialogue_state_tracking_prompt_str = """\
        Given the user input below \
        select the category prompt best suited for what the user is talking about. \
        You will be given the names of the available prompts and a \
        description of what the prompt is best suited for. \
        You may also revise the original input if you think that revising \
        it will ultimately lead to a better response from the language model.
            
        << FORMATTING >>
        Return the name of the prompt selected
        ```
            
        REMEMBER: "destination" MUST be one of the candidate prompt \
        names specified below OR it can be "DEFAULT" if the input is not\
        well suited for any of the candidate prompts.\
            
        << CANDIDATE PROMPTS >>
        {destinations}
            
        << INPUT >>
        {{input}}
            
        << (remember to include only the name of the prompt selected)>>
        """
        dialogue_state_tracking_prompt_template = dialogue_state_tracking_prompt_str.format(
            destinations = self.router_prompt(self.dialogue_states_prompts())
        )
        dialogue_state_tracking_prompt = PromptTemplate(template = dialogue_state_tracking_prompt_template,
                                         input_variables=["input"]
                                        )
        return dialogue_state_tracking_prompt
    
    def user_preferences_tracking_prompt(self):
        user_preferences_tracking_prompt_str = """\
        Given the user input below \
        select the category prompt best suited for what the user is talking about. \
        You will be given the names of the available prompts and a \
        description of what the prompt is best suited for. \
        You may also revise the original input if you think that revising \
        it will ultimately lead to a better response from the language model.
            
        << FORMATTING >>
        Return the name of the prompt selected
        ```
            
        REMEMBER: "destination" MUST be one of the candidate prompt \
        names specified below OR it can be "DEFAULT" if the input is not\
        well suited for any of the candidate prompts.\
            
        << CANDIDATE PROMPTS >>
        {destinations}
            
        << INPUT >>
        {{input}}
            
        << (remember to include only the name of the prompt selected)>>
        """
        user_preferences_tracking_prompt_template = user_preferences_tracking_prompt_str.format(
            destinations = self.router_prompt(self.user_preferences_prompts())
        )
        user_preferences_tracking_prompt = PromptTemplate(template = user_preferences_tracking_prompt_template,
                                         input_variables=["input"]
                                        )
        return user_preferences_tracking_prompt

    def dialogue_states_prompts(self):
        dialogue_state_prompts_str = self.dialogue_states_prompt_templates()
        dialogue_state_prompts_infos = [
        {
            "name": "Health and lifestyle goals",  # Health and wellbeing?
            "description": "Good for understanding health and lifestyle goals of the user", 
            "prompt_template": dialogue_state_prompts_str["goals_prompt_template"]
        },
        {
            "name": "Health issues and illnesses", 
            "description": "Good for understanding health issues and illnesses of the user", 
            "prompt_template": dialogue_state_prompts_str["health_issue_prompt_template"]
        },
        {
            "name": "Consolidated nutrition advice",
            "description": "Good for providing consolidated nutrition advice", 
            "prompt_template": dialogue_state_prompts_str["consolidated_nutrition_advice_template"]        
        },
        {
            "name": "Meal plan", 
            "description": "Good for providing a meal plan", 
            "prompt_template": dialogue_state_prompts_str["meal_plan_prompt_template"]
        },
        {
            "name": "Food preferences",
            "description": "Good for tracking user's food preferences - likes and dislikes", 
            "prompt_template": dialogue_state_prompts_str["user_preferences_template"]
        }
        # {
        #     "name": "Checkin or Review", 
        #     "description": "Good for checking in and reviewing user's existing health goals and issues", 
        #     "prompt_template": categorisation_prompt_templates["question_template"]
        # },    
        ]
        return dialogue_state_prompts_infos
    
    def user_preferences_prompts(self):
        user_preferenes_prompt_infos = [
        {
            "name": "Likes",  # Health and wellbeing?
            "description": "Good for tracking user likes", 
            "prompt_template": self.user_likes_prompt()
        },
        {
            "name": "Dislikes", 
            "description": "Good for tracking user dislikes", 
            "prompt_template": self.user_dislikes_prompt()
        }]
        return user_preferenes_prompt_infos
    
    def goals_prompt(self):
        goals_prompt_str = """\
        Identify the health or lifestyle goal mentioned. Return only the identified goal. \
        Do not include anything else.

        {input} 
        """
        return goals_prompt_str
    
    def health_issue_prompt(self):
        health_issue_prompt_str = """\
        Identify the health issue mentioned. Return only the identified issue. \
        Do not include anything else. 

        {input} 
        """
        return health_issue_prompt_str
    
    def user_likes_prompt(self):
        user_likes_prompt_str = """\
        You need to identify \
        what food the user likes in this messaage. Return only the identified food \
        Do not include anything else.

        {input} 
        """
        return user_likes_prompt_str
    
    def user_dislikes_prompt(self):
        user_dislikes_prompt_str = """\
        You need to identify \
        what food the user dislikes in this messaage. Return only the identified food \
        Do not include anything else.

        {input} 
        """
        return user_dislikes_prompt_str
    
    def user_preferences_promp(self):
        user_dislikes_prompt_str = """\
        You need to identify \
        what food the user dislikes in this messaage. Return only the identified food \
        Do not include anything else.

        {input} 
        """
        return user_dislikes_prompt_str
    
    def meal_plan_prompt(self):
        meal_plan_prompt_str = """\
        Generate a meal plan for the week based on the user info \
        that you have:
        
        {user_info}
        """
        return meal_plan_prompt_str
    
    def consolidated_nutrition_advice_prompt(self):
        consolidated_nutrition_advice_str = """\
        Give detailed nutrition advice, \
        including recommended daily caloric intake, macronutrient breakdown \
        (carbs, protein, fats), and specific food suggestions based on the \
        user info that you have:

        {user_info}
        """
        return consolidated_nutrition_advice_str

    def dialogue_states_prompt_templates(self):
        dialogue_states_prompts_str = {
            "goals_prompt_template": self.goals_prompt(),
            "health_issue_prompt_template": self.health_issue_prompt(),
            "user_preferences_template": self.user_preferences_promp(),
            "meal_plan_prompt_template": self.meal_plan_prompt(),
            "consolidated_nutrition_advice_template": self.consolidated_nutrition_advice_prompt()
        }
        return dialogue_states_prompts_str

    
    def router_prompt(self, prompt_infos):
        # destination_chains = {}
        for p_info in prompt_infos:
            name = p_info["name"]
            prompt_template = p_info["prompt_template"]
            prompt = ChatPromptTemplate.from_template(template=prompt_template)
            # chain = ConversationChain(llm=llm, prompt=prompt)
            # destination_chains[name] = chain  
        destinations = [f"{p['name']}: {p['description']}" for p in prompt_infos]
        destinations_str = "\n".join(destinations)
        return destinations_str