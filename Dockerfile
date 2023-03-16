FROM python:3.10.6-bullseye

# Copy packages
COPY requirements.txt /requirements.txt

# Install packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy Makefile
COPY Makefile Makefile

# Download Spacy pipeline
RUN make download_spacy_pipeline

# Copy app directories and files
COPY interface /interface
COPY ml_logic /ml_logic
COPY scraping /scraping
COPY setup.py setup.py  
COPY params.py params.py
RUN pip install .

# Run api server
CMD uvicorn interface.api:app --host 0.0.0.0 --port 8000