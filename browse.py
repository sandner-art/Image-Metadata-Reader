import gradio as gr
from PIL import Image
import re
import json

# Load patterns from external file
with open('patterns.json', 'r') as f:
    patterns = json.load(f)

prompt_patterns = patterns.get("prompt_patterns", [])
model_patterns = patterns.get("model_patterns", [])
lora_patterns = patterns.get("lora_patterns", [])

def get_all_metadata(image):
    # Extract resolution
    width, height = image.size
    resolution = f"{width}x{height}"
    
    # Extract text prompts (ensure unique and ordered)
    prompts = []
    metadata = image.info
    for pattern in prompt_patterns:
        for key, value in metadata.items():
            if isinstance(value, str):
                matches = re.findall(pattern, value)
                for match in matches:
                    prompts.append(match.strip())
    
    # Extract positive and negative prompts
    positive_prompt = prompts[0] if prompts else None
    negative_prompt = prompts[1] if len(prompts) > 1 else None
    
    # Extract model (ensure unique)
    model_set = set()
    for pattern in model_patterns:
        for key, value in metadata.items():
            if isinstance(value, str):
                matches = re.findall(pattern, value)
                for match in matches:
                    model_set.add(match.strip())
    model = next(iter(model_set), None)
    
    # Extract LoRAs (ensure unique)
    lora_set = set()
    for pattern in lora_patterns:
        for key, value in metadata.items():
            if isinstance(value, str):
                matches = re.findall(pattern, value)
                for match in matches:
                    lora_set.add(match.strip())
    loras = list(lora_set)
    
    # Collect all metadata excluding the resolution and prompt
    all_metadata = {
        key: value for key, value in metadata.items() if key not in ["Resolution", "Prompt"]
    }
    
    # Add model and LoRAs to metadata
    if model:
        all_metadata["Model"] = model
    if loras:
        all_metadata["LoRAs"] = ", ".join(loras)
    
    # Format metadata as a string
    metadata_str = "\n".join([f"{key}: {value}" for key, value in all_metadata.items()])
    
    # Update resolution to include model and LoRAs if available
    if model:
        resolution += f", Model: {model}"
    if loras:
        resolution += f", LoRA: {', '.join(loras)}"
    
    # Format positive and negative prompts
    if positive_prompt:
        all_metadata["Positive Prompt"] = positive_prompt
    if negative_prompt:
        all_metadata["Negative Prompt"] = negative_prompt
    
    # Prepare the prompt output for the first page
    prompt_output = ""
    if positive_prompt:
        prompt_output += f"Positive Prompt: {positive_prompt}\n"
    if negative_prompt:
        prompt_output += f"Negative Prompt: {negative_prompt}\n"
    
    return resolution, prompt_output, metadata_str

def display_metadata(image):
    if image is None:
        return "No image uploaded", "", ""
    resolution, prompt_output, metadata_str = get_all_metadata(image)
    return resolution, prompt_output, metadata_str

# Create the Gradio interface
with gr.Blocks() as iface:
    gr.Markdown("## Image Metadata Reader")
    
    with gr.Tab("Upload Image"):
        with gr.Row():
            with gr.Column():
                image_input = gr.Image(type="pil", label="Upload Image")
            with gr.Column():
                prompt_output = gr.Textbox(label="Prompt", lines=20, interactive=False)
                resolution_output = gr.Textbox(label="Resolution, Model, LoRA", lines=1, interactive=False)
        submit_button = gr.Button("Get Metadata")
        gr.Markdown("sandner.art | [Creative AI/ML Research](https://github.com/sandner-art)")
    with gr.Tab("Full Metadata"):
        full_metadata_output = gr.Textbox(label="Full Metadata", lines=20, interactive=False)
    
    # Define the function to run when the button is clicked
    submit_button.click(
        fn=display_metadata,
        inputs=image_input,
        outputs=[resolution_output, prompt_output, full_metadata_output]
    )

# Launch the interface
iface.launch(inbrowser=True)