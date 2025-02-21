import os
import torch
import pdb
import datetime
import time
import random

# Gradio
import gradio as gr

import pia_prompts
import pia_
import pia_internal_processing

import streamlit as st

user = pia_internal_processing.pia_for_user()

# st.title("Chat with Pia")

# # Initialize chat history
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # Display chat messages from history on app rerun
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # Accept user input
# if user_input := st.chat_input("How can I help you today?"):
#     # Display user message in chat message container
#     with st.chat_message("user"):
#         st.markdown(user_input)
#     # Add user message to chat history
#     st.session_state.messages.append({"role": "user", "content": user_input})

#     # Display assistant response in chat message container
#     with st.chat_message("assistant"):
#         response = st.write_stream(user.pia_chat(user_input))
#     # Add assistant response to chat history
#     st.session_state.messages.append({"role": "assistant", "content": response})



with gr.Blocks() as demo:

    with gr.Tab("Input user bio"):
        name = gr.Textbox(label="Name")
        age = gr.Textbox(label="Age")
        gender = gr.Textbox(label="Gender")
        height = gr.Textbox(label="Height (in metres)")
        weight = gr.Textbox(label="Weight (in Kgs)")
        allergens_and_restrictions = gr.Textbox(label="Allergens and dietary restrictions")
        religious_beliefs = gr.Textbox(label="Religious beliefs")
        # nationality = gr.Textbox(label="Nationality")
        ethnicity = gr.Textbox(label="Ethnicity")
        current_location = gr.Textbox(label="Current location")
        # medical_history / Current health conditions
        submit_btn = gr.Button("Submit")

        def input_bio(name, age, gender, height, weight, allergens_and_restrictions, 
                     religious_beliefs, ethnicity, current_location):
            bio = {"name": name, "age": age, "gender": gender, 
                   "height": height, "weight": weight, 
                  "allergens_and_restrictions": allergens_and_restrictions, 
                   "religious_beliefs": religious_beliefs,
                   "ethnicity": ethnicity, "current_location": current_location}
            user.set_user_bio(bio)
            
        gr.on(
            triggers=[submit_btn.click],
            fn=input_bio,
            inputs=[name, age, gender, height, weight, allergens_and_restrictions,
                   religious_beliefs, ethnicity, current_location]
        )

    with gr.Tab("Pia interface"):
        gr.ChatInterface(user.pia_chat)
        
        meal_plan_btn = gr.Button("Meal plan, please!")
        cons_nutrition_advice_btn = gr.Button("Consolidated nutrition advice, please!")
        meal_plan = gr.TextArea(label = "Meal plan")
        cons_nutrition_advice = gr.TextArea(label = "Consolidated nutrition advice")

        gr.on(
            triggers=[meal_plan_btn.click, cons_nutrition_advice_btn],
            fn=user.generate_meal_plan,
            outputs = user_info
        )
            
    with gr.Tab("Display user info obtained"):
        user_info = gr.TextArea(label = "User info")
        refresh_btn = gr.Button("Refresh")
    
        def get_user_info():
            return user.output_user_info()
    
        gr.on(
            triggers=[refresh_btn.click],
            fn=get_user_info,
            outputs = user_info
        )

