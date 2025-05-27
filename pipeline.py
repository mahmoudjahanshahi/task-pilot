import os
from dotenv import load_dotenv

from semantic_kernel import Kernel
from semantic_kernel.utils.logging import setup_logging
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.azure_chat_prompt_execution_settings import AzureChatPromptExecutionSettings
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.functions.kernel_arguments import KernelArguments

from agents.cleaner import CleanerPlugin
from agents.summarizer import create_summarizer
from agents.extractor import create_extractor

load_dotenv()

# Shared Azure OpenAI chat service
chat_completion = AzureChatCompletion(
    deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION")
)

# LLM config
settings = AzureChatPromptExecutionSettings(temperature=0.2)
settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

# Function to run the Task Pilot pipeline
async def run_task_pilot_pipeline(input_text: str) -> dict:
    # Set up Semantic Kernel and logging
    kernel = Kernel()
    kernel.add_plugin(CleanerPlugin(), plugin_name="Cleaner")
    setup_logging()

    # Cleaner Agent
    arguments = KernelArguments(text=input_text)
    cleaned = await kernel.invoke(
        plugin_name="Cleaner",
        function_name="clean_text",
        arguments=arguments
    )

    # Summarizer Agent
    summarizer = create_summarizer(chat_completion)
    summary = await summarizer.get_response(
        messages=str(cleaned),
        execution_settings=settings
    )

    # Extractor Agent
    extractor = create_extractor(chat_completion)
    tasks = await extractor.get_response(
        messages=str(summary), 
        execution_settings=settings
    )

    return {
        "cleaned": str(cleaned),
        "summary": str(summary),
        "tasks": str(tasks),
    }
