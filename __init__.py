
from .nodes.SimpleTextbox import SimpleTextbox
from .nodes.FilterTextPrompt import FilterTextPrompt

from .deprecated_nodes import NODE_CLASS_MAPPINGS as DEPRECATED_NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as DEPRECATED_NODE_DISPLAY_NAME_MAPPINGS

#merge deprecated mappings
NODE_CLASS_MAPPINGS = {
    "SimpleTextbox": SimpleTextbox,
    "FilterTextPrompt": FilterTextPrompt,
    **DEPRECATED_NODE_CLASS_MAPPINGS
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "SimpleTextbox": "Simple Textbox",
    "FilterTextPrompt": "Filter Text Prompt",
    **DEPRECATED_NODE_DISPLAY_NAME_MAPPINGS
}

WEB_DIRECTORY = "./web"
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']
