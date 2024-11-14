# Marathi-News-RAG

This repository contains the backend for a Marathi News Summarization system, designed to transcribe, process, and summarize video content in Marathi. The project leverages various modern technologies such as FastAPI, Whisper, Langchain, Groq, and ChromaDB for natural language processing, summarization, and vector storage. The system aims to analyze YouTube videos, transcribe them, process the transcripts, and generate concise summaries.

## Project Overview

The project is currently under research, and several core functionalities are still in the process of being refined. The system performs the following key steps:

1. **Video Transcription**:
    - It fetches transcripts for YouTube videos using the YouTube Transcript API. In cases where transcripts are unavailable, it falls back to transcribing the audio using Whisper (a speech-to-text model).

2. **Text Processing**:
    - After obtaining the transcript, the text is processed by splitting it into smaller chunks using `RecursiveCharacterTextSplitter` and generating embeddings with the `HuggingFaceEmbeddings` model.

3. **Graph Building**:
    - A similarity graph is constructed using the Chroma vector store to represent relationships between different chunks of the transcript. This graph helps identify the most important chunks based on their centrality (calculated using PageRank).

4. **Summarization**:
    - Using Groq’s API, a concise summary of the most important chunks is generated. The summary is expected to capture the key points of the video content in Marathi.

## Current Issues

- **Transcript Issues**: There are known issues with generating accurate transcripts, especially when the YouTube video does not have an available transcript. The fallback transcription process using Whisper is still being refined.

- **Text Processing**: The system’s ability to handle large or complex transcripts might need optimization as it can sometimes miss context due to the chunking and embedding processes.

- **Summarization**: Groq's summarization API is being used for text summarization, but its performance is still under research, particularly in ensuring that the summaries are both accurate and concise.

## Technologies Used

- **FastAPI**: The backend is built using FastAPI, providing a high-performance framework for building APIs.
- **Whisper**: Used for transcribing audio content when YouTube transcripts are unavailable.
- **YouTube Transcript API**: Extracts available transcripts from YouTube videos.
- **Langchain**: Used for text splitting and embedding generation.
- **ChromaDB**: Stores and retrieves text embeddings for similarity search.
- **Groq API**: Utilized for generating concise summaries of the text content.

## Requirements

- Python 3.9+
- You can install all the necessary dependencies with:

```bash
pip install -r requirements.txt
```

### Environment Variables

- **GROQ_API_KEY**: Set this environment variable to access the Groq API for summarization.

## Endpoints

### `POST /summarize`

This endpoint accepts a YouTube video URL and generates a summary of the video content in Marathi.

#### Request Body (JSON)
```json
{
  "url": "https://www.youtube.com/watch?v=xxxxxxx",
  "min_length": 100,
  "max_length": 300
}
```

#### Response (JSON)
```json
{
  "summary": "This is the summarized content of the video.",
  "original_length": 1500,
  "summary_length": 100
}
```

### `GET /health`

This endpoint checks the health of the backend service.

#### Response (JSON)
```json
{
  "status": "healthy"
}
```

### `GET /config/verify`

This endpoint verifies the Groq API configuration.

#### Response (JSON)
```json
{
  "status": "configured",
  "groq_api": "connected"
}
```

## Frontend

The frontend for this application is developed in **React**, where users can enter a YouTube video URL, request a summary, and view the results. The frontend communicates with this backend via API requests.

## Future Work

- **Transcript Accuracy**: Improve the fallback transcription using Whisper and handle edge cases where the video may have heavy accents or low-quality audio.
- **Text Summarization**: Optimize the summarization for better conciseness and relevance.
- **Scalability**: Enhance the backend for scalability, particularly in handling large video transcripts.
- **Multi-Language Support**: Expand the capabilities to handle languages other than Marathi, based on the success of the initial implementation.

## Contributing

If you would like to contribute to this project, please fork the repository and create a pull request. We welcome contributions related to improving the transcription, summarization, and overall efficiency of the system.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.