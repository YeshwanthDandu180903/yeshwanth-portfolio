const CONFIG = {
    // Development URL (Localhost)
    // API_URL: 'http://127.0.0.1:8000',

    // Production URL (Hugging Face Spaces)
    // Replace 'YOUR_SPACE_NAME' with your actual space name from Hugging Face
    // Example: 'https://huggingface.co/spaces/YeshwanthDandu/portfolio-backend' -> 'https://yeshwanthdandu-portfolio-backend.hf.space'
    API_URL: 'https://yeshu1809-portfolio-backend.hf.space'
};

// Helper to get full endpoint
const getApiUrl = (endpoint) => {
    // Remove trailing slash if present
    const base = CONFIG.API_URL.replace(/\/$/, "");
    // Ensure endpoint starts with slash
    const path = endpoint.startsWith("/") ? endpoint : `/${endpoint}`;
    return `${base}${path}`;
};
