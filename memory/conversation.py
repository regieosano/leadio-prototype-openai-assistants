from langchain.memory import ConversationSummaryMemory
from openaimodels.llm_models import chat
from memory.filechatmessage import file_chat_messages


conversation_memory = ConversationSummaryMemory(
    chat_memory=file_chat_messages,
    memory_key="messages",
    return_messages=True,
    llm=chat,
)
