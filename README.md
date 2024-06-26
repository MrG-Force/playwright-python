# Juitertoys Playwright for Python Automation Framework
## Quickstart
### First add a `.env` file 
Create a `.env` file in the root of the project directory and add the following environment variables:
```bash
SUT_URL=<your app url>
SUT_API_URL=<your app api url>
OKTA_CLIENT_ID=<secret>
OKTA_CLIENT_SECRET=<secret>
OKTA_AUTH_URL=<your okta auth url>
HEADLESS=false
BROWSER=chrome
```
**IMPORTANT:** Never commit your `.env` file to a public repository (nor even a private one really), Make sure to add it to your `.gitignore` file. It's already there but double check.

### requirements.txt
The `requirements.txt` file should include the following dependencies:
```
pytest-playwright
python-dotenv
```
### Install dependencies
```bash
pip install -r requirements.txt
```
### Running the tests
To run the tests, you can use the following command:
```bash
pytest
```

## Quick Start Guide for Running Playwright Tests in Docker
### Pre-requisites
- Docker installed on your machine

### Dockerfile
The Dockerfile included in this repository is a good starting point for running Playwright tests in Docker. It uses the `python:3.8-slim` image as the base image and installs the necessary dependencies to run Playwright tests.

### Build and Run the Docker Image
1. Navigate to the project directory in your terminal
2. Build the Docker image using the following command (you can name the image whatever you like, e.g., `python-playwright`):
```bash
docker build -t python-playwright-jammy-1.44 .
```
3. Run the Docker Container and Execute all the Tests running the following command:
```bash
docker run --rm -v ${PWD}:/app python-playwright-jammy-1.44 pytest /app/tests 
```
### Running Specific Tests
If you want to run specific tests, you can specify the test file or test name as an argument to the `pytest` command. For example, to run the `test_example.py` file, you can use the following command:
```bash
docker run --rm -v ${PWD}:/app python-playwright pytest test_example.py
```

## Allure Reports
### Pre-requisites
- Java installed on your machine. Refer to the [Java Installation Guide](https://www.java.com/en/download/help/download_options.html) for more information.
- Allure installed on your machine, see [Allure Installation](https://allurereport.org/docs/install/) for more information.

### Running Tests with Allure Reports
To run the tests and generate Allure reports, you can use the following command:
```bash
 pytest --alluredir allure-results
```
To view the Allure report, you can use the following command:
```bash
allure serve allure-results
```
