

class CheckImageGen:
    """
    Node Che controlla l'immagine generata e ne verifica l'aderenza al prompt fornito.
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE", {"default": None, "tooltip": "Image to check"}),
                "positive_prompt": ("STRING", {"default": "", "multiline": True, "forceInput": False, "tooltip": "Text to filter"}),
                "negative_prompt": ("STRING", {"default": "", "tooltip": ""}),
            }
        }

    RETURN_TYPES = ("IMAGE", "FLOAT", "STRING")
    RETURN_NAMES = ("image", "adherence_score", "tip")
    FUNCTION = "check"
    CATEGORY = "gmammolo/AI"


    def check(self, image, text="", substring="PROMPT:"):
        """Return a single STRING which is the text after the substring (if found),
        or the original input if the substring is not present."""
        # Placeholder implementation
        efficiency = 1.0  # Dummy efficiency value
        return (None, efficiency, "Continue")

