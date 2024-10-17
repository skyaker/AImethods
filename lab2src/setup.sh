python3 -m venv .venv

source .venv/bin/activate

pip install tensorflow-macos
# pip install tensorflow-metal  

pip install -r requirements.txt

source .venv/bin/activate

streamlit run app.py