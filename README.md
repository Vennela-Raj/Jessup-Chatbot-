This project involves a chatbot for Jessup Cellars, designed to answer customer queries about their wines and memberships. The chatbot uses pre-trained models for natural language processing and semantic similarity to provide accurate responses.

Prerequisites:
Ensure you have the following software installed:
Python 3.8+
pip (Python package installer)

Installation:
Clone the repository to your local machine using: git clone https://github.com/Vennela-Raj/Jessup-Chatbot-.git

Navigate to the Project Directory: cd Jessup-Chatbot-

Create a Virtual Environment (optional but recommended): python -m venv venv

Activate the Virtual Environment:
  On Windows: venv\Scripts\activate
  On macOS/Linux: source venv/bin/activate

Install the necessary Python packages using:
pip install streamlit spacy sentence-transformers numpy scikit-learn

Ensure you also download the SpaCy model: python -m spacy download en_core_web_sm

Run the chatbot application using Streamlit:
  streamlit run bot.py
  Replace bot.py with the name of your main script if different.

Access the Application:
 Open a web browser and go to http://localhost:8501 to interact with the chatbot.
