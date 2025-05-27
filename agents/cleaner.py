# A Semantic Kernel plugin that provides a function to clean raw input text.
# It removes timestamps, filler words, and normalizes punctuation and whitespace.
# This plugin can be used to preprocess text before further analysis or summarization.

from semantic_kernel.functions import kernel_function

class CleanerPlugin:
    @kernel_function(name="clean_text", description="Clean raw input text")
    def clean_text(self, text: str) -> str:
        import re

        # Remove timestamps like [10:05 AM]
        text = re.sub(r"\[\d{1,2}:\d{2}(?:\s?[APap][Mm])?\]", "", text)

        # Remove filler words
        filler_words = r"\b(?:and|so|uh|um|like|you know|yeah|okay|ok)\b"
        text = re.sub(filler_words, "", text, flags=re.IGNORECASE)

        # Remove extra commas, especially next to removed filler
        text = re.sub(r",\s*,+", ",", text)       # double/triple commas
        text = re.sub(r"\s*,\s*", ", ", text)     # clean spacing
        text = re.sub(r"(?:^|[\s(])[,]+", " ", text)  # stray leading commas
        text = re.sub(r"[,]+(?:$|[\s)])", " ", text)  # stray trailing commas

        # Fix punctuation spacing
        text = re.sub(r"\s+([?.!,])", r"\1", text)
        text = re.sub(r"([?.!,])([^\s])", r"\1 \2", text)  # ensure space after punctuation

        # Normalize whitespace
        text = re.sub(r"\s{2,}", " ", text)

        return text.strip()
