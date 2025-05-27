# A function to extract tasks from text.
# This plugin can be used to identify action items, owners, and due dates from informal text.

from semantic_kernel.agents import ChatCompletionAgent

def create_extractor(shared_service):

    return ChatCompletionAgent(
        service=shared_service,
        name="Extractor",
        instructions=(
            "You extract action items from input text. "
            "Interpret 'you' as audience, and 'I' as the speaker. "
            "For each task, return a bullet point with the format:\n"
            "- Task - Owner - Due Date\n"
            "Mark Unspecified if owner is not clear. "
            "Mark ASAP if due date is not clear. "
            "Example:\n"
            "\"You need to send the email\" → '- Send the email - Audience - ASAP)'\n"
            "\"I will review it by Tuesday\" → '- Review it - Speeker - Tuesday)'\n"
            "\"We should start the search\" → '- Start the search - Unspecified - ASAP)'\n"
        ),
    )
