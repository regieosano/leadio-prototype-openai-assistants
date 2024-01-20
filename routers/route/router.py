from fastapi import APIRouter

post_router = APIRouter(
	prefix="/api",
	tags=["Posts"]
)