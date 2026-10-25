import streamlit as st
from openai import OpenAI

# 1. App Page Configuration
st.set_page_config(page_title="Free OpenRouter Chatbot", page_icon="🤖")
st.title("🤖 Free OpenRouter Assistant")

# 2. Sidebar for Secure Key Entry
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Enter OpenRouter API Key", type="password", help="Get a free key from openrouter.ai")
    st.markdown("[Get a Free OpenRouter API Key](https://openrouter.ai)")
    
    # Let the user know which free model is being used
    st.info("Using Free Model: google/gemini-2.5-flash:free")

# 3. Initialize chat history session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Display historical chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Handle User Input
if prompt := st.chat_input("What is on your mind?"):
    if not api_key:
        st.info("Please add your OpenRouter API key in the sidebar to continue.")
        st.stop()
        
    # Append and display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 6. Call OpenRouter API & Stream Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Point the client to OpenRouter's system endpoints
            client = OpenAI(
                base_url="https://openrouter.aiapi/v1",
                api_key=api_key,
            )
            
            # Using OpenRouter streaming syntax
            response = client.chat.completions.create(
                model="google/gemini-2.5-flash:free",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True
            )
            
            for chunk in response:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
