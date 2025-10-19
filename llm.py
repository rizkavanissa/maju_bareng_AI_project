import getpass
import os

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.text_splitter import CharacterTextSplitter
# from langchain_core.documents import Document
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# embedding_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")


# Asks for user's Google API key
GOOGLE_API_KEY = input("Enter your API key: ").strip()
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# Initialize the LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.5, top_p=0.9)

# Creates prompt system message and initializes chat history
chat_history = []
chat_history.append(
    SystemMessage(content="You are a knowledgeable and bubbly assistant who is passionate about fashion. You are knowledgeable about the latest fashion trends, styles, and designers. You love to help people find their personal style and give fashion advice. You are also knowledgeable about fashion history, the current fashion industry, and can provide interesting facts and trivia about fashion."),
)

while True:
    # Asks for user input
    prompt = input("User: ")
    chat_history.append(HumanMessage(content=prompt))

    # Gives prompt to LLM and gets response
    response = llm.invoke(chat_history)
    print()
    print("AI:", response.content)
    print()
    chat_history.append(response)
