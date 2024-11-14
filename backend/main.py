from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
from video_transcriber import get_video_transcript
from text_processor import TextProcessor
from graph_builder import GraphBuilder
from summarizer import GroqSummarizer
from schemas import VideoRequest

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialized summarizer
summarizer = GroqSummarizer()


@app.post("/summarize")
async def summarize_video(request: VideoRequest) -> Dict:
    try:
        # Get transcript
        transcript = await get_video_transcript(request.url)

        # Process text
        processor = TextProcessor()
        chunks = processor.split_text(transcript)
        embeddings = processor.create_embeddings(chunks)

        # Build graph and get important chunks
        graph_builder = GraphBuilder()
        graph = graph_builder.build_graph(chunks, embeddings)
        important_chunks = graph_builder.get_important_chunks()

        # Combine important chunks
        combined_text = " ".join(important_chunks)

        # Generate summary using Groq
        summary = await summarizer.generate_summary(
            combined_text,
            max_length=request.max_length
        )

        return {
            "summary": summary,
            "original_length": len(transcript.split()),
            "summary_length": len(summary.split())
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/config/verify")
async def verify_config():
    try:
        test_completion = summarizer.client.chat.completions.create(
            messages=[{"role": "user", "content": "Test"}],
            model="llama3-8b-8192",
            max_tokens=5
        )
        return {"status": "configured", "groq_api": "connected"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
