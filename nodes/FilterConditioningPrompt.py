class FilterConditioningPrompt:
    """
    Custom node for ComfyUI that filters a CONDITIONING prompt by removing content 
    before a specified substring (including the substring itself).
    """
    
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                    "conditioning": ("CONDITIONING", {"tooltip": "The conditioning prompt to filter"}),
                    "substring": ("STRING", {"default": "<think>", "tooltip": "Remove everything before this substring (inclusive)"})
                }}

    RETURN_TYPES = ("CONDITIONING",)
    RETURN_NAMES = ("filtered_conditioning",)
    FUNCTION = "filter_prompt"
    CATEGORY = "conditioning"

    def filter_prompt(self, conditioning, substring):
        """
        Filter the conditioning prompt by removing content before the specified substring.
        
        Args:
            conditioning: The input CONDITIONING object
            substring: The substring to search for (content before this will be removed)
            
        Returns:
            Filtered CONDITIONING object
        """
        # ComfyUI CONDITIONING format is a list of [conditioning_data, extra_info]
        filtered_conditioning = []
        
        for cond_item in conditioning:
            if len(cond_item) >= 2:
                # Get the conditioning data and extra info
                cond_data, extra_info = cond_item[0], cond_item[1]
                
                # Check if there's a 'pooled_output' or text content to filter
                if 'pooled_output' in extra_info:
                    # For SDXL and similar models that use pooled output
                    filtered_conditioning.append([cond_data, extra_info])
                else:
                    # For standard text conditioning, we need to filter the prompt
                    # The actual text prompt is usually stored in the extra_info
                    filtered_extra_info = extra_info.copy()
                    
                    # Look for text content in various possible keys
                    text_keys = ['prompt', 'text', 'conditioning_text']
                    for key in text_keys:
                        if key in filtered_extra_info and isinstance(filtered_extra_info[key], str):
                            original_text = filtered_extra_info[key]
                            
                            # Find the substring and remove everything before it (inclusive)
                            if substring in original_text:
                                substring_index = original_text.find(substring)
                                filtered_text = original_text[substring_index + len(substring):]
                                filtered_extra_info[key] = filtered_text
                            # If substring not found, keep original text
                    
                    filtered_conditioning.append([cond_data, filtered_extra_info])
            else:
                # Keep the item as-is if it doesn't have the expected structure
                filtered_conditioning.append(cond_item)
        
        return (filtered_conditioning,)
