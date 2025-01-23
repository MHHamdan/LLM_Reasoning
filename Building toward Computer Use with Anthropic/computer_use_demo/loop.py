import platform
from datetime import datetime
from collections.abc import Callable
from typing import Any
import openai

# Constants
SYSTEM_PROMPT = f"""<SYSTEM_CAPABILITY>
* You are utilizing an Ubuntu virtual machine using {platform.machine()} architecture with internet access.
* You can feel free to install Ubuntu applications with your bash tool. Use curl instead of wget.
* To open firefox, please just click on the firefox icon. Note, firefox-esr is what is installed on your system.
* Using bash tool you can start GUI applications, but you need to set export DISPLAY=:1 and use a subshell. For example \"(DISPLAY=:1 xterm &)\". GUI apps run with bash tool will appear within your desktop environment, but they may take some time to appear. Take a screenshot to confirm it did.
* The current date is {datetime.today().strftime('%A, %B %-d, %Y')}.
</SYSTEM_CAPABILITY>

<IMPORTANT>
* When using Firefox, if a startup wizard appears, IGNORE IT. Do not even click \"skip this step\". Instead, click on the address bar where it says \"Search or enter address\", and enter the appropriate search term or URL there.
* If the item you are looking at is a pdf, if after taking a single screenshot of the pdf it seems that you want to read the entire document instead of trying to continue to read the pdf from your screenshots + navigation, determine the URL, use curl to download the pdf, install and use pdftotext to convert it to a text file, and then read that text file directly.
</IMPORTANT>"""

async def sampling_loop(
    *,
    api_key: str,
    model: str = "gpt-4",
    system_prompt_suffix: str = "",
    messages: list[dict[str, Any]],
    output_callback: Callable[[str], None],
    max_tokens: int = 4096,
):
    """
    Sampling loop for OpenAI GPT API interaction.
    """
    system_prompt = {
        "role": "system",
        "content": f"{SYSTEM_PROMPT}{' ' + system_prompt_suffix if system_prompt_suffix else ''}",
    }

    # Ensure the system prompt is included
    if not messages or messages[0]["role"] != "system":
        messages.insert(0, system_prompt)

    while True:
        try:
            # Make an API call to OpenAI
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                api_key=api_key,
            )

            # Extract the assistant's response
            assistant_message = response["choices"][0]["message"]
            messages.append(assistant_message)

            # Output the response content
            output_callback(assistant_message["content"])

            # Simulate tool interaction if needed (not implemented in this example)
            user_response = await simulate_tool_interaction(assistant_message["content"])
            if user_response:
                messages.append({"role": "user", "content": user_response})
            else:
                break

        except openai.error.OpenAIError as e:
            print(f"OpenAI API error: {e}")
            break

async def simulate_tool_interaction(assistant_message: str) -> str:
    """
    Simulates interaction with tools based on assistant's response.
    This function is a placeholder for actual tool implementation.
    """
    print(f"Assistant said: {assistant_message}")
    return ""  # Return an empty string to end the loop

# Example usage
if __name__ == "__main__":
    import asyncio

    async def main():
        await sampling_loop(
            api_key="your_openai_api_key",
            messages=[
                {"role": "user", "content": "Explain the difference between GPT and Claude AI."}
            ],
            output_callback=lambda content: print(f"Assistant: {content}"),
        )

    asyncio.run(main())
