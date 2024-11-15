# Image-Metadata-Reader
Reads full image metadata and attempts to extract the prompt, model, and LoRAs used. Gradio app.
## Install
1. run setup.bat to setup venv
2. run go.bat

## Known Limitations
- When parsing an image with convoluted workflow and several prompts, the prompt can be wrongly attributed to Positive/Negative Prompt
- In custom workflow with unusual nodes the prompt may not be found. You may edit patterns.json to remedy the case or check the 'Full Metadata' tab (workflow saved into the file in metadata format) to find the prompt or additional info about the resources
- This may also happen when a styler extension was used to generate the file and the prompt was not saved as continous text
