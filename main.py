import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

# Initialize session state
if "generated_recipe" not in st.session_state:
    st.session_state.generated_recipe = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("AI Recipe Generator")
st.write("Enter ingredients you have, and I'll suggest a recipe!")

ingredients = st.text_input("Ingredients (comma-separated):")
st.checkbox("No cooking with fire/gas", key="no_flame")
if st.button("Generate Recipe"):
    if ingredients:
        prompt = f"Create a recipe using the following ingredients: {ingredients}. Include a title, ingredients list, and step-by-step instructions. If any non food items are mentioned, just tell them to give food ingredients only, and don't generate any hypothetical recipes."
        if st.session_state.no_flame: 
            prompt += " Also, ensure the recipe does not involve cooking with fire or gas."
        with st.spinner("Generating your recipe..."):
            response = model.generate_content(prompt)
        
        # Store the generated recipe in session state
        st.session_state.generated_recipe = response.text
    else:
        st.error("Please enter some ingredients.")

# Display the generated recipe persistently if it exists
if st.session_state.generated_recipe:
    st.subheader("Generated Recipe")
    st.write(st.session_state.generated_recipe)

# Recipe Chatbot Section
if st.session_state.generated_recipe:
    st.markdown("---")
    st.subheader("🤖 Recipe Assistant")
    st.write("Ask me questions about the recipe above!")
    
    # Display chat history
    for i, (question, answer) in enumerate(st.session_state.chat_history):
        st.write(f"**You:** {question}")
        st.write(f"**Assistant:** {answer}")
        st.write("")
    
    # Chat input
    user_question = st.text_input("Ask a question about the recipe:", key="chat_input")
    
    if st.button("Ask") and user_question:
        with st.spinner("Thinking..."):
            # Create a context-aware prompt
            chat_prompt = f"""
            Based on this recipe:
            {st.session_state.generated_recipe}
            
            Please answer this question: {user_question}
            
            Keep your answer helpful, concise, and related to the recipe. If the question is not related to cooking or the recipe, politely redirect to recipe-related topics.
            """
            
            chat_response = model.generate_content(chat_prompt)
            
            # Add to chat history
            st.session_state.chat_history.append((user_question, chat_response.text))
            
            # Clear the input field by resetting the session state key
            if "chat_input" in st.session_state:
                del st.session_state["chat_input"]
            
            # Rerun to show the new chat
            st.rerun()
    
    # Clear chat button
    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()
