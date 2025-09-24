import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from prompts import recipe_prompt, SYSTEM_PROMPT

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("❌ API key not found. Please set GEMINI_API_KEY in your .env file.")
else:
    genai.configure(api_key=API_KEY)

    st.set_page_config(page_title="AI Recipe Generator", page_icon="🍲", layout="wide")
    st.title("🍲 AI Recipe Generator")

    # Initialize session state
    if "chat" not in st.session_state:
        model = genai.GenerativeModel("gemini-2.5-flash")
        st.session_state.chat = model.start_chat()
    if "recipe" not in st.session_state:
        st.session_state.recipe = None
    if "qna_chat" not in st.session_state:
        qna_model = genai.GenerativeModel("gemini-2.5-flash")
        st.session_state.qna_chat = qna_model.start_chat()
    if "qna_messages" not in st.session_state:
        st.session_state.qna_messages = []

    # 🔄 Reset chat button
    if st.button("🔄 Reset All"):
        st.session_state.chat = None
        st.session_state.recipe = None
        st.session_state.qna_chat = None
        st.session_state.qna_messages = []
        st.rerun()

    # Initialize chat session if not present
    if "chat" not in st.session_state or st.session_state.chat is None:
        model = genai.GenerativeModel("gemini-2.5-flash")
        st.session_state.chat = model.start_chat()
    if "qna_chat" not in st.session_state or st.session_state.qna_chat is None:
        qna_model = genai.GenerativeModel("gemini-2.5-flash")
        st.session_state.qna_chat = qna_model.start_chat()
    if "recipe" not in st.session_state:
        st.session_state.recipe = None

    # Create two columns layout
    col1, col2 = st.columns([1, 1])
    
    # Left column - Recipe Generator
    with col1:
        st.header("🍳 Recipe Generator")
        
        # Ingredient input
        ingredients = st.text_area(
            "Enter ingredients (comma separated):",
            placeholder="e.g. chicken, garlic, onion, tomato",
            key="ingredients_input"
        )

        # Generate recipe
        if st.button("Generate Recipe"):
            if ingredients.strip():
                recipe_instructions = f"{SYSTEM_PROMPT}\n{recipe_prompt(ingredients)}"
                response = st.session_state.chat.send_message(recipe_instructions)
                st.session_state.recipe = response.text
                st.success("✅ Recipe generated!")
                st.rerun()
            else:
                st.warning("⚠️ Please enter at least one ingredient.")

        # Show generated recipe
        if st.session_state.recipe:
            st.subheader("Generated Recipe")
            with st.container():
                st.markdown(st.session_state.recipe)
    
    # Right column - QnA Bot
    with col2:
        st.header("🤖 Recipe Q&A Assistant")
        
        if not st.session_state.recipe:
            st.info("💡 Generate a recipe first to start asking questions about it!")
        else:
            # Display chat messages
            chat_container = st.container()
            with chat_container:
                for message in st.session_state.qna_messages:
                    if message["role"] == "user":
                        st.markdown(f"**You:** {message['content']}")
                    else:
                        st.markdown(f"**Assistant:** {message['content']}")
            
            # Chat input
            question = st.text_input(
                "Ask a question about the recipe:",
                placeholder="e.g. Can I substitute chicken with tofu?",
                key="qna_input"
            )
            
            if st.button("Ask Question") or (question and st.session_state.get("last_question") != question):
                if question.strip():
                    # Add user message to chat history
                    st.session_state.qna_messages.append({"role": "user", "content": question})
                    
                    # Create context-aware prompt for QnA
                    qna_context = f"""
                    You are a helpful cooking assistant. A user has generated the following recipe:
                    
                    {st.session_state.recipe}
                    
                    Please answer the user's question about this recipe. Be helpful, specific, and provide practical cooking advice.
                    If the question is not related to cooking or the recipe, politely redirect the user to ask recipe-related questions.
                    
                    User's question: {question}
                    """
                    
                    try:
                        response = st.session_state.qna_chat.send_message(qna_context)
                        # Add assistant response to chat history
                        st.session_state.qna_messages.append({"role": "assistant", "content": response.text})
                        st.session_state.last_question = question
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                else:
                    st.warning("⚠️ Please enter a question.")
            
            # Clear chat button
            if st.button("🗑️ Clear Chat"):
                st.session_state.qna_messages = []
                st.session_state.qna_chat = None
                st.rerun()