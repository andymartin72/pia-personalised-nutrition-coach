import os
import torch
import pdb
import datetime
import time
import random

# Gradio
import gradio as gr

from pia import pia

pia = pia()


with gr.Blocks() as demo:
    with gr.Tab("About you"):
        with gr.Tab("New user"):
            def input_bio(name, age, gender, height, weight, allergens_and_restrictions, 
                        religious_beliefs, ethnicity, current_location):
                bio = {"name": name, "age": age, "gender": gender, 
                    "height": height, "weight": weight, 
                    "allergens_and_restrictions": allergens_and_restrictions, 
                    "religious_beliefs": religious_beliefs,
                    "ethnicity": ethnicity, "current_location": current_location}
                output = pia.new_user(bio)
                return output

            # Input elements
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
            user_id = gr.Textbox(label="Your user ID", show_copy_button=True)
                
            gr.on(
                triggers=[submit_btn.click],
                fn=input_bio,
                inputs=[name, age, gender, height, weight, allergens_and_restrictions,
                    religious_beliefs, ethnicity, current_location],
                outputs = user_id
            )

        with gr.Tab("Existing user"):
            user_id = gr.Textbox(label="User ID")
            submit_btn = gr.Button("Submit")
            output_message = gr.Textbox(label="Identification status")

            gr.on(
                triggers=[submit_btn.click],
                fn=pia.existing_user,
                inputs=user_id,
                outputs = output_message
            )

    with gr.Tab("Pia chat interface"):
        gr.ChatInterface(pia.pia_chat)

        with gr.Row():
            meal_plan_btn = gr.Button("Meal plan, please!")
            cons_nutrition_advice_btn = gr.Button("Consolidated nutrition advice, please!")

        with gr.Row():
            meal_plan = gr.TextArea(label = "Meal plan")
            cons_nutrition_advice = gr.TextArea(label = "Consolidated nutrition advice")

        meal_plan_btn.click(pia.generate_meal_plan, outputs = meal_plan)
        cons_nutrition_advice_btn.click(pia.generate_consolidated_nutrition_advice, outputs = cons_nutrition_advice)
        
            
    with gr.Tab("Display user info obtained"):
        user_info = gr.TextArea(label = "User info")
        refresh_btn = gr.Button("Refresh")
    
        def get_user_info():
            return pia.output_user_info()
    
        gr.on(
            triggers=[refresh_btn.click],
            fn=get_user_info,
            outputs = user_info
        )

demo.launch()