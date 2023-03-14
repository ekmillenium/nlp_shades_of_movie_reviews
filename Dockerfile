FROM python:3.10.6-bullseye

# Copy packages
COPY requirements.txt /requirements.txt

# Install packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy app directories and files
COPY interface /interface
COPY ml_logic /ml_logic
#COPY scraper /scraper
COPY setup.py setup.py
COPY params.py params.py
RUN pip install .

# Copy Makefile and shortcut commands
COPY Makefile Makefile

# Download Spacy pipeline
RUN make download_spacy_pipeline

# Run api server
CMD uvicorn interface.api:app --host 0.0.0.0 