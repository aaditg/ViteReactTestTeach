import React, { useState } from "react";
import axios from "axios";

const App = () => {
    const [file, setFile] = useState(null);
    const [color, setColor] = useState("");
    const [averageColor, setAverageColor] = useState("");
    const [error, setError] = useState("");

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
        setAverageColor("");
        setError("");
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");
        if (!file || !color) {
            setError("Please select a file and a color");
            return;
        }

        const formData = new FormData();
        formData.append("file", file);
        formData.append("color", color);

        try {
            const response = await axios.post("http://localhost:5000/process", formData, {
                headers: { "Content-Type": "multipart/form-data" },
            });
            const { average_color } = response.data;
            setAverageColor(average_color);
            alert(`Average Color: ${average_color}`);
        } catch (err) {
            console.error("Error:", err);
            setError("Error processing image. Please try again.");
        }
    };

    const handleDownload = async () => {
        try {
            const response = await axios.get("http://localhost:5000/download", {
                responseType: "blob", // Ensures the file is received as a blob
            });

            const blob = new Blob([response.data]);
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = "processed_image.png";
            a.click();
            window.URL.revokeObjectURL(url);
        } catch (err) {
            setError("Error downloading file. Please try again.");
            console.error(err);
        }
    };

    const handleCleanup = async () => {
        try {
            await axios.post("http://localhost:5000/cleanup");
            alert("Temporary files cleaned up!");
        } catch (err) {
            setError("Error cleaning up temporary files.");
            console.error(err);
        }
    };

    return (
        <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
            <h1>Image Processing App</h1>
            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="file">Upload an image:</label>
                    <input
                        type="file"
                        id="file"
                        onChange={handleFileChange}
                        accept="image/*"
                        required
                    />
                </div>
                <div>
                    <label htmlFor="color">Select a color:</label>
                    <select
                        id="color"
                        value={color}
                        onChange={(e) => setColor(e.target.value)}
                        required
                    >
                        <option value="">Select Color</option>
                        <option value="red">Red</option>
                        <option value="blue">Blue</option>
                        <option value="yellow">Yellow</option>
                        <option value="green">Green</option>
                        <option value="orange">Orange</option>
                        <option value="purple">Purple</option>
                    </select>
                </div>
                <button type="submit" style={{ marginTop: "10px" }}>
                    Process Image
                </button>
            </form>

            {error && <p style={{ color: "red" }}>{error}</p>}
            {averageColor && <p>Average Color: {averageColor}</p>}

            <div style={{ marginTop: "20px" }}>
                <button onClick={handleDownload} disabled={!averageColor}>
                    Download Processed Image
                </button>
                <button onClick={handleCleanup} style={{ marginLeft: "10px" }}>
                    Cleanup Temporary Files
                </button>
            </div>
        </div>
    );
};

export default App;
