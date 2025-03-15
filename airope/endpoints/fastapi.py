from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import logging
from contextlib import asynccontextmanager

# Configure logging
logger = logging.getLogger(__name__)


# Define request and response models using Pydantic
class HelloResponse(BaseModel):
    message: str


class DataRequest(BaseModel):
    content: str
    description: str | None


class DataResponse(BaseModel):
    id: int
    content: str
    description: str | None
    processed: bool = False


# Lifespan event handler for startup and shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic: initialize resources, connections, etc.
    logger.info("Starting up FastAPI application")
    yield
    # Shutdown logic: clean up resources, close connections, etc.
    logger.info("Shutting down FastAPI application")


# Create FastAPI instance with metadata and lifespan
app = FastAPI(
    title="AiRope API",
    description="API for AiRope - Local AI application for document and code management",
    version="0.1.0",
    lifespan=lifespan,
)


# Simple dependency for demonstration
async def get_api_key(api_key: str = Depends(lambda: None)):
    # In a real app, validate API key here
    if api_key.strip() == "":
        # For demo purposes, we'll allow None, but log it
        logger.warning("No API key provided")
    return api_key


@app.get("/", response_model=HelloResponse, tags=["General"])
async def root():
    """
    Root endpoint that returns a simple hello message.
    """
    return HelloResponse(message="Hello from AiRope API")


@app.get("/hello", response_model=HelloResponse, tags=["General"])
async def hello():
    """
    Simple hello endpoint that returns a greeting message.
    """
    return HelloResponse(message="Hello, World!")


@app.post(
    "/data",
    response_model=DataResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Data"],
)
async def create_data(data: DataRequest, api_key: Annotated[str, Depends(get_api_key)]):
    """
    Create new data entry.

    This is a placeholder POST endpoint that simulates creating a data entry.

    - **content**: The main content to be processed
    - **description**: Optional description of the content
    """
    try:
        # This is a placeholder - in a real app, you would save to a database
        logger.info(f"Received data: {data.content}")

        # Mock response
        return DataResponse(
            id=1,  # Placeholder ID
            content=data.content,
            description=data.description,
            processed=True,
        )
    except Exception as e:
        logger.error(f"Error processing data: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process data",
        )


# Add a health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return {"status": "healthy"}


# If running this file directly
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
