from langchain.chains import LLMChain
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from langchain_community.tools.convert_to_openai import format_tool_to_openai_function
from aitools.mortgage_rate_tool import get_current_mortgage_rate
from models.schemas import PostMessageRequest
from airoles.prompts import AI_ASSISTANT_ROLE
from memory.conversation import conversation_memory
from openaimodels.llm_models import chat
from langchain.agents import AgentExecutor

tools = [get_current_mortgage_rate]


class UserAIChatService:
    def post_ai_user_chat_qna(self, content: PostMessageRequest):
        useraichat = ChatPromptTemplate(
            input_variables=["content", "messages"],
            messages=[
                MessagesPlaceholder(variable_name="messages"),
                SystemMessagePromptTemplate.from_template(AI_ASSISTANT_ROLE),
                HumanMessagePromptTemplate.from_template(content.chat),
            ],
        )

        openai_tools = chat.bind(
            functions=[format_tool_to_openai_function(t) for t in tools]
        )
