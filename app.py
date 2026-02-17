from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# Temporary upload folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ComfyUI API endpoint on cloud GPU
COMFYUI_URL = "http://YOUR_CLOUD_GPU_IP:PORT/api/run_workflow"

@app.route("/generate", methods=["POST"])
def generate_video():
    # Get uploaded image and prompt
    image_file = request.files['image']
    prompt_text = request.form['prompt']

    # Save uploaded image temporarily
    image_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
    image_file.save(image_path)

    # Load workflow JSON
    with open("workflow_dynamic.json", "r", encoding="utf-8") as f:
        workflow_json = f.read()

    # Inject user prompt
    workflow_json = workflow_json.replace("<USER_PROMPT>", prompt_text)

    # Send request to ComfyUI API
    with open(image_path, "rb") as img_file:
        files = {"image": img_file}
        response = requests.post(COMFYUI_URL, files=files, data={"workflow": workflow_json})

    if response.status_code == 200:
        result = response.json()
        return jsonify({"video_url": result.get("video_url", "")})
    else:
        return jsonify({"error": "Failed to generate video"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
