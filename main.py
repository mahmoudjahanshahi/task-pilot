import os
import logging
import asyncio
from dotenv import load_dotenv

from semantic_kernel import Kernel
from semantic_kernel.utils.logging import setup_logging
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.azure_chat_prompt_execution_settings import AzureChatPromptExecutionSettings
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.functions.kernel_arguments import KernelArguments

# Import custom plugins and functions
from agents.cleaner import CleanerPlugin
from agents.summarizer import create_summarizer
from agents.extractor import create_extractor

async def main():
    load_dotenv()

    kernel = Kernel()

    # Azure OpenAI Chat Completion setup
    chat_completion = AzureChatCompletion(
        deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION")
    )
    kernel.add_service(chat_completion)

    # Logging
    setup_logging()
    logging.getLogger("kernel").setLevel(logging.DEBUG)

    # Add plugin
    kernel.add_plugin(CleanerPlugin(), plugin_name="Cleaner")

    # Settings
    settings = AzureChatPromptExecutionSettings(temperature=0.2)
    settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

    # Example input
    input_text = """
    [10:05 AM] So, like, um, you need to finish the report by Friday, you know? 
    And, uh, maybe I should call John? Yeah, that’s all I remember.
    """
    arguments = KernelArguments(text=input_text)

    # Invoke
    cleaned = await kernel.invoke(
        plugin_name="Cleaner",
        function_name="clean_text",
        arguments=arguments
    )

    print("\n--- Cleaned Output ---\n")
    print(cleaned)

    # Create the summarizer agent
    summarizer = create_summarizer(chat_completion)

    # Call the agent with cleaned text
    summary = await summarizer.get_response(
        messages=str(cleaned),
        execution_settings=settings
        )

    print("\n--- Summary ---\n")
    print(summary)

    # Create the extractor agent
    extractor = create_extractor(chat_completion)

    # Call the agent with summarized text
    tasks = await extractor.get_response(
        messages=str(summary),
        execution_settings=settings
        )

    print("\n--- Extracted Tasks ---\n")
    print(tasks)


# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
