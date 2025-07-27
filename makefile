# Makefile for Bybit Streamlit Trading Bot

APP_NAME = Trading-bot
DOCKER_PORT = 8501

.PHONY: run install build docker-run docker-build clean

## Install Python dependencies locally
install:
	pip install -r requirements.txt

## Run Streamlit app locally
run:
	streamlit run bot.py

## Build Docker image
build:
	docker build -t $(APP_NAME) .

## Run Docker container (port 8501)
run:
	docker run --rm -p $(DOCKER_PORT):8501 $(APP_NAME)

## Clean up __pycache__ and temp files
clean:
	find . -type d -name '__pycache__' -exec rm -r {} +
	find . -name '*.pyc' -delete
