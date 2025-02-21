from pia_external_response import pia_response_generation

class pia(pia_response_generation):
    def __init__(self):
        super().__init__()
        self.initiate_pia()
        self.store = {}
        self.current_user = {}
    
    def new_user(self, user_bio):
        self.current_user_count += 1
        user_id = self.current_user_count
        self.users[user_id] = {}
        self.current_user = {"current_meal_plan": {}, "meal_plan_history": {}, "current_goals": {}, 
                      "current_health_issues": {}, "preferences": {"likes": {}, "dislikes": {}},
                    "past_preferences": {"likes": {}, "dislikes": {}}, "user_bio": user_bio}
        self.users[user_id] = self.current_user
        self.set_user_bio(user_bio)
        str_message = """Hi {name}, your entry is successful, your user ID is: {user_id} \n
        You can now start chatting with pia""".format(name = user_bio["name"], user_id = user_id)
        return str_message
    
    def existing_user(self, user_id):
        user_id = int(user_id)
        if user_id in self.users.keys():
            self.set_user_bio(self.users[user_id]["user_bio"])
            self.current_user = self.users[user_id]
            str_message =  "Welcome back {name}! You can now start chatting with Pia".format(name = self.users[user_id]["user_bio"]["name"])
            return str_message
        else:
            return  "Your user ID is not found"

    def set_user_bio(self, bio_hash):
        self.bio_hash = bio_hash
        if "BMI" not in self.bio_hash:
            self.bio_hash["BMI"] = self.calculate_bmi()
        self.bio_prompt = self.bio_format()
        self.user_info_prompt = self.get_user_info_prompt()

    def bio_format(self):
        bio_prompt = """
        Name: {}
        Age: {}
        Gender: {}
        Height (in metres): {}
        Weight (in Kgs): {}
        BMI: {}
        Allergens and dietary restrictions: {}
        Religious beliefs: {}
        Ethnicity: {}
        Current location: {}
        """.format(self.bio_hash["name"], self.bio_hash["age"], self.bio_hash["gender"],
                   self.bio_hash["height"], self.bio_hash["weight"], 
                   self.bio_hash["BMI"], self.bio_hash["allergens_and_restrictions"], 
                   self.bio_hash["religious_beliefs"], self.bio_hash["ethnicity"],
                   self.bio_hash["current_location"])
        return bio_prompt
    
    def calculate_bmi(self):
        bmi = float(self.bio_hash["weight"])/(float(self.bio_hash["height"])**2)
        return bmi
    
    def pia_chat(self, message, history):
        # Internal Dialog state tracking
        dialogue_state = self.pia_dialogue_state_tracking(message)
        # Internal processing
        self.pia_understand_user(dialogue_state, message)
        # External Dialog state tracking
        response_prompt = self.response_prompt(dialogue_state, message)
        # External response generation
        response = self.pia_response(response_prompt, message)
        return response.content

    
    