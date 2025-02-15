
import gradio as gr
from smolagents import load_tool

# Load the tool
journey_tool = load_tool("MHamdan/journey-metrics-tool", trust_remote_code=True)

def create_interface():
    with gr.Blocks(title="Journey Metrics Calculator") as iface:
        gr.Markdown("# Journey Metrics Calculator")
        gr.Markdown("Calculate travel distance and time between two locations.")
        
        with gr.Row():
            with gr.Column():
                start = gr.Textbox(
                    label="Start Location",
                    placeholder="e.g., Montreal"
                )
                dest = gr.Textbox(
                    label="Destination Location",
                    placeholder="e.g., Toronto"
                )
                mode = gr.Dropdown(
                    choices=["driving", "walking", "bicycling", "transit", "plane"],
                    label="Transportation Mode",
                    value="driving"
                )
                submit_btn = gr.Button("Calculate Journey")
                
            with gr.Column():
                output = gr.Textbox(
                    label="Journey Details",
                    lines=5
                )
        
        # Example data
        gr.Examples(
            examples=[
            ["Montreal", "Toronto", "plane"],
            ["Vancouver", "Whistler", "driving"],
            ["Ottawa", "Kingston", "bicycling"],
            ["New York", "Los Angeles", "plane"],
            ["Sanaa", "Jeddah", "plane"],
            ["Sanaa", "Jeddah", "driving"],
            ["Sanaa", "Jeddah", "bicycling"],
            ["London", "Paris", "train"]
        ],
            inputs=[start, dest, mode],
            outputs=output,
            fn=journey_tool,
            cache_examples=True
        )
        
        submit_btn.click(
            fn=journey_tool,
            inputs=[start, dest, mode],
            outputs=output
        )
    
    return iface

# Create and launch the interface
demo = create_interface()
demo.launch()
