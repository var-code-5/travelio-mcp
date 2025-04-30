import asyncio
import os
from dotenv import load_dotenv
import google.generativeai as genai  # Use Google Generative AI library
import subprocess

async def main():
    # Load environment variables
    load_dotenv()

    # Start the Travelio MCP server
    server_process = subprocess.Popen(
        ["python", "-m", "app.mcp.server"],
        env=os.environ.copy(),
    )

    try:
        # Configure the Gemini LLM
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Missing GEMINI_API_KEY environment variable")
        genai.configure(api_key=api_key)
        llm = genai.GenerativeModel(model_name="gemini-1.5-pro")

        # Run the query directly using the LLM
        query = "Find the best travel destinations for adventure seekers"
        result = llm.generate(prompt=query)
        print(f"\nResult: {result.text}")

    finally:
        # Ensure the server process is terminated
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    asyncio.run(main())
