import os

# ================= PROJECT ROOT =================
# This dynamically finds the RAG_BOT root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ================= IMAGE DIRECTORY =================
IMAGE_DIR = os.path.join(BASE_DIR, "images", "extracted")

# ================= KEYWORD → IMAGE MAP =================
IMAGE_KEYWORDS = {
    # IIoT / Industrial Automation
    "industrial internet of things": "iiot.png",
    "iiot": "iiot.png",
    "horizontal iot": "horizontal_iot.png",
    "vertical iot": "vertical_iot.png",
    "iot architecture": "iiot.png",
    "smart factory": "iiot.png",

    # RAG / AI
    "retrieval augmented generation": "rag_pipeline.png",
    "rag pipeline": "rag_pipeline.png",
    "rag": "rag_pipeline.png",
    "naive rag":"naive_rag.png",
    "modular rag":"modular_rag.png",
    "retrieval augmented generation": "rag_pipeline.png",
    "retrieval augmented generation": "rag_pipeline.png",
    "retrieval augmented generation": "rag_pipeline.png",
    "advanced rag":"advanced_rag.png",
    "rag as a service": "rag_as_a_service.png",
    "rag as a service": "rag_as_a_service.png",
    "rag as a service": "rag_as_a_service.png",


    # CNN
    "cnn": "cnn.png",
    "convolutional neural network": "cnn.png",
    #RNN
    "rnn": "rnn.png",
    "Recurrent Neural Networks":"rnn.png",
    "recurrent neural networks":"rnn.png",
    "recurrent neural network":"rnn.png",
    # LSTM
    "lstm": "lstm.png",
    "Long Short-Term Memory":"lstm.png"

}

# ================= IMAGE RETRIEVAL FUNCTION =================
def get_supporting_images(text):
    """
    Returns a list of absolute image paths
    based on keywords found in the text.
    """

    if not text:
        return []

    text = text.lower()
    matched_images = []

    for keyword, image_name in IMAGE_KEYWORDS.items():
        if keyword in text:
            image_path = os.path.join(IMAGE_DIR, image_name)

            # Debug-safe existence check
            if os.path.isfile(image_path):
                matched_images.append(image_path)

    return matched_images
