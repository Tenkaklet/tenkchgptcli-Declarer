import os
import typer
import openai
from dotenv import load_dotenv
from typing import Optional
from tqdm import tqdm
import time

load_dotenv()

openai.api_key = os.getenv("OPENAI_KEY")

app = typer.Typer()


@app.command()
def interactive_chat(
    text: Optional[str] = typer.Option(None, "--text", "-t", help="Start with text"),
    temperature: float = typer.Option(0.7, help="Control Randomness. Defaults to 0.7"),
    max_tokens: int = typer.Option(
        150, help="Control length of response. Defaults to 150"
    ),
    model: str = typer.Option(
        "gpt-3.5-turbo", help="Control the model to use. Defaults to gpt-3.5-turbo"
    ),
):
    """Interactive CLI tool to chat with ChatGPT."""
    typer.echo(
        "Welcome, you are now starting an interactive chat with Declarer AI. Type 'exit' to end the session."
    )

    messages = []

    while True:
        if text:
            prompt = text
            text = None
        else:
            prompt = typer.prompt("You")

        messages.append({"role": "user", "content": prompt})
        if prompt == "exit":
            typer.echo("Declarer AI: Goodbye!")
            break

        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        
        # here I can add an animation to show that the AI is typing
        for i in tqdm(range(101), desc="Declarer AI is typing...", ascii=False, ncols=75, leave=True, position=0):
            time.sleep(0.01)


        typer.echo(f'Declarer AI: {response["choices"][0]["message"]["content"]}')
        messages.append(response["choices"][0]["message"])


if __name__ == "__main__":
    app()