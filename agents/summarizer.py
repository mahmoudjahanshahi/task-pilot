# A Semantic Kernel plugin that provides a function to summarize messy or informal text.
# It produces 3-5 clear bullet points summarizing actions, decisions, or important information.
# This plugin can be used to generate concise summaries from cleaned text.

from semantic_kernel.agents import ChatCompletionAgent

def create_summarizer(shared_service):
    return ChatCompletionAgent(
        service=shared_service,
        name="Summarizer",
        instructions=(
            "You are an expert in summarizing messy or informal text. "
            "Your job is to produce 3-5 clear bullet points summarizing actions, decisions, or important information. "
            "Focus on clarity and usefulness."
        )
    )
