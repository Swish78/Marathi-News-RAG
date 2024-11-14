import os
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
import whisper
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
import networkx as nx
from groq import Groq
import dotenv
dotenv.load_dotenv(dotenv_path='.env')

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


class TextProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", "।", ".", " ", ""]
        )
        self.embeddings = HuggingFaceEmbeddings(
            model_name="ai4bharat/indic-bert",
            model_kwargs={'device': 'cuda'},
            encode_kwargs={'normalize_embeddings': True}
        )

    def split_text(self, text):
        return self.text_splitter.split_text(text)

    def create_embeddings(self, chunks):
        return Chroma.from_texts(
            texts=chunks,
            embedding=self.embeddings,
            persist_directory="./chroma_db"
        )


# Class for building the graph
class GraphBuilder:
    def __init__(self):
        self.graph = nx.Graph()

    def build_graph(self, chunks, embeddings):
        for i, chunk in enumerate(chunks):
            self.graph.add_node(i, text=chunk)

        for i in range(len(chunks)):
            results = embeddings.similarity_search_with_score(chunks[i], k=3)
            for doc, score in results:
                if score > 0.7:
                    j = chunks.index(doc.page_content)
                    if i != j:
                        self.graph.add_edge(i, j, weight=score)

        return self.graph

    def get_important_chunks(self, top_k=3):
        pagerank = nx.pagerank(self.graph)
        important_nodes = sorted(
            [(node, score) for node, score in pagerank.items()],
            key=lambda x: x[1],
            reverse=True
        )[:top_k]
        return [self.graph.nodes[node]['text'] for node, _ in important_nodes]


# Function to get transcript
def get_video_transcript(url, language="mr"):
    try:
        video_id = url.split("watch?v=")[1]
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
        return " ".join([entry['text'] for entry in transcript])
    except Exception:
        print("Falling back to Whisper model...")
        model = whisper.load_model("base")
        yt = YouTube(url)
        audio_path = yt.streams.filter(only_audio=True).first().download()
        result = model.transcribe(audio_path)
        os.remove(audio_path)
        return result["text"]


# Function to generate a summary using Groq
def generate_summary_with_groq(text, max_length=300):
    prompt = f"""
    Analyze the following Marathi text and provide a concise summary in Marathi. 
    The summary should capture the main points and key ideas.
    Text to summarize: {text}
    Please provide a summary in under {max_length} words.
    """

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant skilled in summarizing Marathi text while preserving key information."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="llama3-8b-8192",
        temperature=0.3,
        max_tokens=max_length * 4,
        top_p=0.9
    )

    return chat_completion.choices[0].message.content


if __name__ == "__main__":
    url = input("Enter the YouTube video URL: ")
    min_length = int(input("Enter minimum summary length (in words): "))
    max_length = int(input("Enter maximum summary length (in words): "))

    transcript = get_video_transcript(url)
    print(f"\nOriginal Transcript Length: {len(transcript.split())} words")

    processor = TextProcessor()
    chunks = processor.split_text(transcript)
    embeddings = processor.create_embeddings(chunks)

    graph_builder = GraphBuilder()
    graph = graph_builder.build_graph(chunks, embeddings)
    important_chunks = graph_builder.get_important_chunks()

    combined_text = " ".join(important_chunks)
    summary = generate_summary_with_groq(combined_text, max_length)

    print("\nGenerated Summary:")
    print(summary)
