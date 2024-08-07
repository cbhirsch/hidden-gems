import streamlit as st
from groq import Groq

from apicall import search

st.title("Colorado's Hidden Gems")

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What kind of adventure are you looking for?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    search_result = search(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        groq_client = Groq()
        all_but_last_message = st.session_state.messages[:-1]
        last_message = st.session_state.messages[-1]
        next_to_last_system_message = {
            "role": "system",
            "content": f"You are a helpful adventure guide. Answer the user's question using the search result. Use markdown. Include the colorado.gov link. Be brief.\n\n{search_result.for_model()}",
        }
        all_messages = (
            all_but_last_message + [next_to_last_system_message] + [last_message]
        )
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": m["role"], "content": m["content"]} for m in all_messages
            ],
            model="llama3-8b-8192",
        )
        response = chat_completion.choices[0].message.content

        st.markdown(response)

        st.video(search_result.youtube_link, start_time=search_result.start_time)

    st.session_state.messages.append({"role": "assistant", "content": response})
