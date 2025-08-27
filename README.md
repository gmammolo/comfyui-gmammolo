# ComfyUI GMAMMOLO

This repository provides a small set of custom nodes for ComfyUI. The primary node removes any text before a specified substring (inclusive) from a CONDITIONING object. This is useful when prompt-generation scripts or logging insert internal markers that shouldn't be forwarded to a model.

## Installation

# ComfyUI - Filter Conditioning Prompt Node

This repository provides a single custom node for ComfyUI that filters CONDITIONING prompts by removing any text before a specified substring (inclusive). It's useful when prompt generation or logging inserts markers or internal reasoning text that shouldn't be forwarded to a model.

Provided node

- `FilterConditioningPrompt` — accepts a `CONDITIONING` input and a `substring` (default: `<think>`). Returns a `CONDITIONING`-formatted output with text before the first occurrence of `substring` removed (including the substring).

Why use it

- Removes prompt prefixes or markers while preserving ComfyUI's CONDITIONING structure.

Installation

1. Place this repository inside your ComfyUI `custom_nodes/` folder (for example `custom_nodes/comfyui-gmammolo`).
2. Restart ComfyUI.

No external Python dependencies are required by this node. If you add dependencies later, list them in `requirements.txt` and install them with `pip install -r requirements.txt`.

Usage

1. In ComfyUI, find the node under the `conditioning` category (display name: "Filter Conditioning Prompt").
2. Connect a `CONDITIONING` output to the `conditioning` input.
3. Optionally change the `substring` input to the marker you want to strip (default `<think>`).
4. Use the node's `filtered_conditioning` output in place of the original conditioning.

Project layout

- `CompfyuiGmammolo.py` — node implementation with `FilterConditioningPrompt`.
- `example_workflows/` — example templates (if present).
- `saved_context/` — legacy folder possibly used by older code.
- `web/js/` — web UI helper scripts (if present).

License

See `LICENSE` for license details.

Contributing

If you want additional features, tests, or support for other conditioning formats, open an issue or submit a pull request.

— End of README
- `example_workflows/` — example templates (if present).

- `saved_context/` — legacy folder possibly used by older code.

- `web/js/` — web UI helper scripts (if present).
