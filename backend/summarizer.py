import os
from groq import Groq
from fastapi import HTTPException
import dotenv

dotenv.load_dotenv(dotenv_path='.env')


class GroqSummarizer:
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    async def generate_summary(self, text: str, max_length: int) -> str:
        try:
            prompt = f"""
            Analyze the following Marathi text and provide a concise summary in Marathi. 
            The summary should capture the main points and key ideas.
            Text to summarize: {text}
            Please provide a summary in under {max_length} words.
            """

            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant skilled in summarizing Marathi text while preserving "
                                   "key information."
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

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate summary: {str(e)}"
            )
