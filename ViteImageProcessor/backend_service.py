from flask import Flask, request, jsonify, send_file
import os
from flask_cors import CORS
from image_processing import (
    delete_existing_txt_files,
    load_image,
    get_color_input,
    save_image_and_color,
    delete_existing_output,
    isolate_color,
    calculate_average_hex,
    save_average_color,
)

app = Flask(__name__)
CORS(app)

# Ensure directories exist
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return "Image Processing Backend Service is running!"

@app.route("/process", methods=["POST"])
def process_image():
    """
    Handles the image upload, processes the image based on color, and returns the processed results.
    """
    try:
        # Delete existing files
        delete_existing_txt_files()
        delete_existing_output()

        # Get the uploaded image file and target color
        image_file = request.files.get("image")
        color = request.form.get("color").strip().lower()

        if not image_file or not color:
            return jsonify({"error": "Missing image file or color input"}), 400

        # Save the uploaded file to UPLOAD_FOLDER
        image_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
        image_file.save(image_path)

        # Load the image and process it
        image = load_image(image_path)
        isolated_image = isolate_color(image, color)

        # Save the isolated image to OUTPUT_FOLDER
        output_path = os.path.join(OUTPUT_FOLDER, "isolated_subject.png")
        isolated_image.save(output_path)

        # Calculate the average hex color
        avg_hex = calculate_average_hex(output_path)
        save_average_color(avg_hex)

        return jsonify({
            "message": "Image processed successfully",
            "average_color": avg_hex,
            "processed_image_path": output_path
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/download", methods=["GET"])
def download_processed_image():
    """
    Endpoint to download the processed image.
    """
    try:
        output_path = os.path.join(OUTPUT_FOLDER, "isolated_subject.png")
        if os.path.exists(output_path):
            return send_file(output_path, mimetype="image/png", as_attachment=True, download_name="processed_image.png")
        else:
            return jsonify({"error": "Processed image not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/cleanup", methods=["POST"])
def cleanup():
    """
    Deletes all temporary files in UPLOAD_FOLDER and OUTPUT_FOLDER.
    """
    try:
        for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER]:
            for file in os.listdir(folder):
                os.remove(os.path.join(folder, file))
        return jsonify({"message": "Temporary files cleaned up successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
