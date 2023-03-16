import os

##################  VARIABLES  ##################
# GCP Project
GCP_PROJECT = os.environ.get("GCP_PROJECT")
GCP_REGION = os.environ.get("GCP_REGION")

# Cloud Storage
BUCKET_NAME = os.environ.get("BUCKET_NAME")

# BigQuery
BQ_REGION = os.environ.get("BQ_REGION")
BQ_DATASET = os.environ.get("BQ_DATASET")
DATA_SIZE= os.environ.get("DATA_SIZE")

# Compute Engine
INSTANCE = os.environ.get("INSTANCE")

# Docker
GCR_IMAGE = os.environ.get("GCR_IMAGE")
GCR_REGION = os.environ.get("GC_REGION")

# Goggle Cloud Run
MEMORY = os.environ.get("MEMORY")
SERVICE_URL = os.environ.get("SERVICE_URL")

# Model Lifecycle
PREFECT_FLOW_NAME = os.environ.get("PREFECT_FLOW_NAME")
PREFECT_LOG_LEVEL = os.environ.get("PREFECT_LOG_LEVEL")

##################  CONSTANTS  #####################
LOCAL_DATA_PATH = os.path.join(os.path.expanduser('~'), os.environ.get("LOCAL_DATA_PATH"))