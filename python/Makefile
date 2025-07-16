# Default values 
PROFILE_NAME ?= default_profile
TRAINED_PROFILE_NAME ?= trained_profile
RECORD_TITLE ?= default_record
RECORD_DESCRIPTION ?= optional_description
MARKER_VALUE ?= test_value
MARKER_LABEL ?= test_label
EXPORT_FOLDER ?= ./export

all: help

help:
	@echo "Available commands:"
	@echo "  make cortex                      - Run cortex.py"
	@echo "  make facial_expression_train     - Run facial_expression_train.py (with PROFILE_NAME)"
	@echo "  make mental_command_train        - Run mental_command_train.py (with PROFILE_NAME)"
	@echo "  make live_advance                - Run live_advance.py (with TRAINED_PROFILE_NAME)"
	@echo "  make marker                      - Run marker.py with marker and record arguments"
	@echo "  make record                      - Run record.py with record and export arguments"
	@echo "  make sub_data                    - Run sub_data.py"
	@echo ""
	@echo "You can override values like this:"
	@echo "  make facial_expression_train PROFILE_NAME=my_profile"
	@echo "  make record RECORD_TITLE=my_title EXPORT_FOLDER=~/Desktop"

cortex:
	python3 cortex.py

facial_expression_train:
	python3 facial_expression_train.py --profile_name $(PROFILE_NAME)

mental_command_train:
	python3 mental_command_train.py --profile_name $(PROFILE_NAME)

live_advance:
	python3 live_advance.py --trained_profile_name $(TRAINED_PROFILE_NAME)

marker:
	python3 marker.py \
		--record_title "$(RECORD_TITLE)" \
		--record_description "$(RECORD_DESCRIPTION)" \
		--marker_value "$(MARKER_VALUE)" \
		--marker_label "$(MARKER_LABEL)" \
		--record_export_folder "$(EXPORT_FOLDER)"

record:
	python3 record.py \
		--record_title "$(RECORD_TITLE)" \
		--record_description "$(RECORD_DESCRIPTION)" \
		--record_export_folder "$(EXPORT_FOLDER)"

sub_data:
	python3 sub_data.py
