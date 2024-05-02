import streamlit as st
import os
from PIL import Image
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Title of the Streamlit app
st.set_page_config(page_title="Image AI", page_icon="./logo.jpg")
st.title("Image AI")

# Upload an image
uploaded_file = st.file_uploader("Choose an image", type=["png","jpg"])
# Display the uploaded image
if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img)
    # Ask a question
    # question = st.text_area("Question", placeholder="What do you want to know about the image?")
    question = st.chat_input(placeholder="What do you want to know about the image?")
# Submit button
    if question:
        with st.chat_message(name="user",avatar="./user.png"):
            st.write(question)
        with st.chat_message(name="ai",avatar="./logo.jpg"):
            with st.spinner():
                model = ChatGoogleGenerativeAI(model="gemini-pro-vision")
                message = HumanMessage(content=[
                { 'type': 'text', 'text': question },
                { 'type': 'image_url', 'image_url': img }
            ])
                stream_placeholder = st.empty()
                response = model.stream([message])
                buffer = []
                for chunk in response:
                    buffer.append(chunk.content)
                    stream_placeholder.markdown(''.join(buffer), unsafe_allow_html=True)
