import re


class FilterTextPrompt:
    """
    Node that filters a plain STRING by removing everything before (and
    including) a given substring and returns the filtered STRING.
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"default": "", "multiline": True, "forceInput": False, "tooltip": "Text to filter"}),
                "substring": ("STRING", {"default": "<think>", "tooltip": "Remove everything before this substring (inclusive)"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "filter_prompt"
    CATEGORY = "gmammolo/Text"

    def _filter_string(self, original_text, substring):
        # Only operate on strings
        if not isinstance(original_text, str):
            return original_text

        # Normalize: replace line breaks with spaces, collapse multiple whitespace
        normalized = original_text.replace('\r', ' ').replace('\n', ' ')
        normalized = re.sub(r"\s+", ' ', normalized).strip()

        # If no substring provided, return the normalized input
        if not substring:
            return normalized

        idx = normalized.find(substring)
        if idx != -1:
            return normalized[idx + len(substring):]
        return normalized

    def filter_prompt(self, text="", substring="PROMPT:"):
        """Return a single STRING which is the text after the substring (if found),
        or the original input if the substring is not present."""
        filtered = self._filter_string(text, substring)
        return (filtered,)

