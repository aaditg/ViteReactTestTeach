const BASE_URL = "http://127.0.0.1:5000"; // Flask backend URL

export const processImage = async (file, color) => {
    const formData = new FormData();
    formData.append("image", file);
    formData.append("color", color);

    const response = await fetch(`${BASE_URL}/process`, {
        method: "POST",
        body: formData,
    });

    if (!response.ok) {
        throw new Error("Error processing image");
    }

    return response.json();
};

export const downloadProcessedImage = async () => {
    const response = await fetch(`${BASE_URL}/download`, { method: "GET" });
    if (!response.ok) {
        throw new Error("Error downloading image");
    }

    return response.blob();
};

export const cleanupTemporaryFiles = async () => {
    const response = await fetch(`${BASE_URL}/cleanup`, { method: "POST" });
    if (!response.ok) {
        throw new Error("Error cleaning up files");
    }

    return response.json();
};