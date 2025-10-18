

class CheckImageGen:
    """
    Node Che controlla l'immagine generata e ne verifica l'aderenza al prompt fornito.
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE", {"default": None, "tooltip": "Image to check"}),
                "positive_prompt": ("STRING", {"default": "", "multiline": True, "forceInput": False, "tooltip": "Positive prompt to guide generation image"}),
                "negative_prompt": ("STRING", {"default": "", "multiline": True, "forceInput": False, "tooltip": "Negative prompt to guide generation image"}),
                "openai_base_url": ("STRING", {"default": "https://utopia.hpc4ai.unito.it/api", "tooltip": "Base URL for OpenAI-compatible API"}),
                "model": ("STRING", {"default": "gemma3:27b-it-fp16", "tooltip": "Model to use for evaluation"}),
                "openai_api_key": ("STRING", {"default": "", "tooltip": "API key for the OpenAI-compatible service (optional if set in env)"}),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "prompt": "PROMPT", 
                "extra_pnginfo": "EXTRA_PNGINFO",
            }
        }

    RETURN_TYPES = ("IMAGE", "FLOAT", "STRING")
    RETURN_NAMES = ("image", "adherence_score", "tip")
    FUNCTION = "check"
    CATEGORY = "gmammolo/AI"


    def check(self, image, positive_prompt="", negative_prompt="", openai_base_url="https://api.openai.com", model="gpt-4o-mini", openai_api_key=""):
        """Send the image and prompts to an OpenAI-compatible responses endpoint and return:
        (image, adherence_score: float between 0 and 1, tip: string)

        Contract:
        - Inputs: pillow-like IMAGE object (or None), positive_prompt, negative_prompt, openai_base_url, model, openai_api_key
        - Output: tuple (image, float, str)
        - Error modes: on network/error return adherence_score=0.0 and tip with error message
        """
        try:
            import base64
            import io
            import json
            import requests
        except Exception as e:
            return (image, 0.0, f"Missing dependency: {e}")

        # Build the combined instruction for the model
        instruction = (
            f"You are given an image and two text prompts.\n"
            f"Positive prompt: {positive_prompt}\n"
            f"Negative prompt: {negative_prompt}\n"
            "Please evaluate how well the image adheres to the positive prompt and does NOT match the negative prompt. "
            "Return a JSON object with keys: 'score' (0.0-1.0) and 'tip' (short advice)."
        )

        # Encode image to PNG base64 if provided
        image_b64 = None
        if image is not None:
            try:
                # assume image is a PIL Image-like object with save()
                buf = io.BytesIO()
                image.save(buf, format="PNG")
                buf.seek(0)
                image_b64 = base64.b64encode(buf.read()).decode("utf-8")
            except Exception as e:
                return (image, 0.0, f"Failed to encode image: {e}")

        # Prepare request
        url = openai_base_url.rstrip("/") + "/v1/responses"
        headers = {"Content-Type": "application/json"}
        if openai_api_key:
            headers["Authorization"] = f"Bearer {openai_api_key}"

        # Build the inputs; include the image as a data URL in the input content
        inputs = []
        if image_b64:
            inputs.append({"type": "image_base64", "image_base64": image_b64, "name": "image"})

        # Use text input with the instruction and prompts
        inputs.append({"type": "text", "text": instruction})

        body = {
            "model": model,
            "input": inputs,
            # give the model a short system instruction to produce JSON
            "temperature": 0.0,
        }

        try:
            resp = requests.post(url, headers=headers, data=json.dumps(body), timeout=30)
        except Exception as e:
            return (image, 0.0, f"Request error: {e}")

        if resp.status_code != 200:
            # try to return server message
            msg = resp.text
            return (image, 0.0, f"API error {resp.status_code}: {msg}")

        try:
            data = resp.json()
        except Exception as e:
            return (image, 0.0, f"Invalid JSON response: {e}")

        # Attempt to extract model-generated text. Support both OpenAI-style and generic.
        text_out = None
        # OpenAI Responses API may include 'output' or 'choices'
        if isinstance(data, dict):
            if "output" in data and isinstance(data["output"], list) and len(data["output"])>0:
                # output can be list of multimodal items; find first text
                for item in data["output"]:
                    if isinstance(item, dict) and item.get("type") == "output_text":
                        text_out = item.get("content") or item.get("text")
                        break
                if text_out is None:
                    # fallback: join text fields
                    parts = []
                    for item in data["output"]:
                        if isinstance(item, dict) and "content" in item:
                            parts.append(item.get("content"))
                    text_out = "\n".join([p for p in parts if p]) if parts else None
            elif "choices" in data and isinstance(data["choices"], list) and len(data["choices"])>0:
                # legacy completions/chat
                first = data["choices"][0]
                if isinstance(first, dict):
                    text_out = first.get("text") or (first.get("message") and first["message"].get("content"))

        if not text_out:
            # As a last resort, stringify the whole response
            text_out = json.dumps(data)

        # Try to parse JSON from the model output
        score = 0.0
        tip = ""
        try:
            # model may have returned a JSON object; find first JSON substring
            import re

            m = re.search(r"\{.*\}", text_out, flags=re.S)
            parsed = None
            if m:
                parsed = json.loads(m.group(0))
            else:
                # try to load directly
                parsed = json.loads(text_out)

            if isinstance(parsed, dict):
                if "score" in parsed:
                    score = float(parsed.get("score") or 0.0)
                # also accept 'adherence' or similar
                elif "adherence" in parsed:
                    score = float(parsed.get("adherence") or 0.0)
                tip = str(parsed.get("tip") or parsed.get("advice") or "")
        except Exception:
            # fallback heuristics: find a float between 0 and 1 in the text
            try:
                import re
                m = re.search(r"([01](?:\.\d+)?|0?\.\d+)", text_out)
                if m:
                    score = float(m.group(1))
                    if score > 1.0:
                        score = max(0.0, min(1.0, score / 100.0))
                tip = text_out.strip()[:512]
            except Exception:
                score = 0.0
                tip = text_out.strip()[:512]

        # clamp score
        try:
            score = float(score)
        except Exception:
            score = 0.0
        score = max(0.0, min(1.0, score))

        return (image, score, tip)

