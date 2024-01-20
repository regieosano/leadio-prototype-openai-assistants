from fastapi import HTTPException, status
from routers.route.router import post_router
from models.schemas import PostMessageRequest, PostMessageResponse
from services.api.useraichat import UserAIChatService

user_ai_chat_service = UserAIChatService()


@post_router.post(
    "/useraichat",
    status_code=status.HTTP_200_OK,
    response_model=PostMessageResponse,
)
def user_ai_chats(content: PostMessageRequest):
    try:
        reply = user_ai_chat_service.post_ai_user_chat_qna(content)
        return reply
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
