# ----------------------------------
#         LOCAL SET UP
# ----------------------------------

reinstall_packages:
	@pip install -r requirements.txt

download_spacy_pipeline:
	python -m spacy download en_core_web_trf


# ----------------------------------
#    LOCAL INSTALL COMMANDS
# ----------------------------------

install:
	@pip install -e . 


# ----------------------------------
#    PACKAGES ACTIONS
# ----------------------------------

load_10k_data_to_bq:
	python ml_logic/data.py load_data_to_bq '10000'

load_300k_data_to_bq:
	python ml_logic/data.py load_data_to_bq '300000'

load_450k_data_to_bq:
	python ml_logic/data.py load_data_to_bq '450000'

load_all_data_to_bq:
	python ml_logic/data.py load_data_to_bq 'all'

run_ner_on_10k:
	python interface/main.py run_ner_model '10k'

run_ner_on_300k:
	python interface/main.py run_ner_model '300k'

run_ner_on_450k:
	python interface/main.py run_ner_model '450k'

run_ner_on_all:
	python interface/main.py run_ner_model 'all'