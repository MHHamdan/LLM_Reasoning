import gradio as gr
from transformers import pipeline
import requests
from bs4 import BeautifulSoup
import PyPDF2
import docx
import time
from langchain_community.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file
openai_api_key = os.getenv("OPENAI_API_KEY")
llm = OpenAI(openai_api_key=openai_api_key)

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
sentiment_analyzer = pipeline("sentiment-analysis")
topic_classifier = pipeline("zero-shot-classification")

def fetch_text_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        soup = BeautifulSoup(response.text, "html.parser")
        return " ".join(p.get_text() for p in soup.find_all("p"))
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Error fetching text from URL: {str(e)}")

def extract_text_from_pdf(file):
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except PyPDF2.errors.PdfReadError as e:
        raise ValueError(f"Error extracting text from PDF: {str(e)}")

def extract_text_from_docx(file):
    try:
        doc = docx.Document(file)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    except docx.opc.exceptions.PackageNotFoundError as e:
        raise ValueError(f"Error extracting text from DOCX: {str(e)}")

def analyze_text(input_text, input_type, tasks, progress=gr.Progress()):
    if input_type == "URL":
        progress(0, desc="Fetching text from URL")
        try:
            input_text = fetch_text_from_url(input_text)
        except ValueError as e:
            return str(e), "", "", ""
    elif input_type == "File":
        progress(0, desc="Extracting text from file")
        if input_text is None:
            return "No file uploaded", "", "", ""
        file_name = input_text.name.lower()
        if file_name.endswith(".pdf"):
            try:
                input_text = extract_text_from_pdf(input_text)
            except ValueError as e:
                return str(e), "", "", ""
        elif file_name.endswith(".docx"):
            try:
                input_text = extract_text_from_docx(input_text)
            except ValueError as e:
                return str(e), "", "", ""
        else:
            input_text = input_text.read().decode("utf-8")
    
    original_text = input_text[:1000] + ("..." if len(input_text) > 1000 else "")
    
    summary, sentiment, topics = "", "", ""
    
    if "Summarization" in tasks:
        progress(0.3, desc="Generating summary")
        summary = summarizer(input_text, max_length=100, min_length=30, do_sample=False)[0]["summary_text"]
        time.sleep(1)  # Add a minimal delay for demonstration purposes
    
    if "Sentiment Analysis" in tasks:
        progress(0.6, desc="Analyzing sentiment")
        sentiment = sentiment_analyzer(input_text[:512])[0]["label"]  # Truncate input for sentiment analysis
        time.sleep(1)
    
    if "Topic Detection" in tasks:
        progress(0.9, desc="Detecting topics")
        topic_labels = ["technology", "politics", "sports", "entertainment", "business"]
        topics = topic_classifier(input_text[:512], topic_labels, multi_label=True)["labels"]  # Truncate input for topic detection 
        time.sleep(1)
    
    progress(1, desc="Analysis completed")
    
    return original_text, summary, sentiment, ", ".join(topics)

def chat(input_text, conversation_history):
    prompt_template = """
    Assistant is an AI language model that helps with text analysis tasks.

    Conversation history:
    {conversation_history}

    Human: {input_text}
    Assistant:"""

    prompt = PromptTemplate(
        input_variables=["conversation_history", "input_text"], 
        template=prompt_template
    )
    
    chain = ConversationChain(llm=llm, prompt=prompt, memory=ConversationBufferMemory(memory_key="conversation_history"))
    response = chain.predict(input_text=input_text)
    
    return response

def create_interface():
    with gr.Blocks(title="Text Analysis App") as interface:
        gr.Markdown("## Choose data format to analyze")
        input_type = gr.Dropdown(["Text", "URL", "File"], label="Input Type")
        text_input = gr.Textbox(label="Text Input", visible=False)
        url_input = gr.Textbox(label="URL Input", visible=False)
        file_input = gr.File(label="File Upload", visible=False)

        tasks_checkboxes = gr.CheckboxGroup(["Summarization", "Sentiment Analysis", "Topic Detection"], label="Analysis Tasks")

        submit_button = gr.Button("Analyze")
        progress_bar = gr.Progress()

        with gr.Tab("Original Text"):
            original_text_output = gr.Textbox(label="Original Text")
        with gr.Tab("Summary"):
            summary_output = gr.Textbox(label="Summary")
        with gr.Tab("Sentiment"):
            sentiment_output = gr.Textbox(label="Sentiment")
        with gr.Tab("Topics"):
            topics_output = gr.Textbox(label="Topics")
        with gr.Tab("Conversation"):
            conversation_history = gr.State([])
            conversation_input = gr.Textbox(label="Human")
            conversation_output = gr.Textbox(label="Assistant")
            conversation_button = gr.Button("Send")

        def update_input_visibility(input_type):
            return {
                text_input: gr.update(visible=input_type == "Text"),
                url_input: gr.update(visible=input_type == "URL"),
                file_input: gr.update(visible=input_type == "File")
            }

        input_type.change(update_input_visibility, inputs=[input_type], outputs=[text_input, url_input, file_input])

        def process_input(input_type, text, url, file, tasks):
            if input_type == "Text":
                input_value = text
            elif input_type == "URL":
                input_value = url
            else:
                input_value = file
            
            original_text, summary, sentiment, topics = analyze_text(input_value, input_type, tasks, progress_bar)
            return original_text, summary, sentiment, topics

        submit_button.click(
            fn=process_input,
            inputs=[input_type, text_input, url_input, file_input, tasks_checkboxes],
            outputs=[original_text_output, summary_output, sentiment_output, topics_output]
        )

        def process_conversation(conversation_history, conversation_input):
            conversation_history.append(f"Human: {conversation_input}")
            response = chat(conversation_input, "\n".join(conversation_history))
            conversation_history.append(f"Assistant: {response}")
            return "\n".join(conversation_history), "", response

        conversation_button.click(
            fn=process_conversation,
            inputs=[conversation_history, conversation_input],
            outputs=[conversation_history, conversation_input, conversation_output]
        )

    return interface

if __name__ == "__main__":
    create_interface().launch()