# ----------------------------------
#         LOCAL SET UP
# ----------------------------------

install_packages:
	@pip install -r requirements.txt

run_spacy_process:
	python -m spacy download en_core_web_trf


# ----------------------------------
#    LOCAL INSTALL COMMANDS
# ----------------------------------

install:
	@pip install . -U
