from langchain_core.messages import AIMessage, HumanMessage
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from langchain_community.tools.convert_to_openai import format_tool_to_openai_function
from aitools.mortgage_rate_tool import get_current_mortgage_rate
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from models.schemas import PostMessageRequest
from openaimodels.llm_models import chat
from langchain.agents import AgentExecutor

tools = [get_current_mortgage_rate]

chat_history = []


class UserAIChatService:
    def post_ai_user_chat_qna(self, content: PostMessageRequest):
        MEMORY_KEY = "chat_history"
        useraichatprompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are very powerful assistant and has general knowledge, but don't know how to compute mortgage",
                ),
                MessagesPlaceholder(variable_name=MEMORY_KEY),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="mortgage_scratchpad"),
            ]
        )

        openai_tools = chat.bind(
            functions=[format_tool_to_openai_function(t) for t in tools]
        )

        agent = (
            {
                "input": lambda x: x["input"],
                "mortgage_scratchpad": lambda x: format_to_openai_function_messages(
                    x["intermediate_steps"]
                ),
                "chat_history": lambda x: x["chat_history"],
            }
            | useraichatprompt
            | openai_tools
            | OpenAIFunctionsAgentOutputParser()
        )

        agent_executor = AgentExecutor(agent=agent, tools=tools)

        result = agent_executor.invoke(
            {"input": content.chat, "chat_history": chat_history}
        )
        chat_history.extend(
            [
                HumanMessage(content=content.chat),
                AIMessage(content=result["output"]),
            ]
        )

        return result
