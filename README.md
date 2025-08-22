# Project Setup Guide

Welcome to the project setup guide! Follow these instructions to get your project up and running.

## Prerequisites

- **Python**: Ensure you have Python 3.11 installed on your system. If you don't, you can download it from the [official Python website](https://www.python.org/downloads/).

## Installation Steps

### Step 1: Create a Virtual Environment

A virtual environment is crucial for managing the dependencies of the project separately from your global Python installation.

- **Windows:**

```bash
python -m venv venv
```

- **macOS/Linux:**

```bash
python3 -m venv venv
```

### Step 2: Activate the Virtual Environment

Activating the virtual environment will ensure that all Python and pip commands apply only to this specific environment.

- **Windows:**

```bash
source venv\Scripts\activate
```

- **macOS/Linux:**

```bash
source venv/bin/activate
```

### Step 3: Install Requirements

Install all required packages for the project as specified in the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

Create a `.env` file in the root directory of the project. Add the following variables:

```txt
USERNAME={your_username}
PASSWORD={your_password}

ORIGINS=["http://127.0.0.1"]
```

Replace `your_username` and `your_password` with appropriate values.

### Step 5: Start the Server

Run the server using the following command:

```bash
uvicorn main:app --reload
```

This command will start the FastAPI application with live reloading enabled.

## Usage

After starting the server, you can access the application by navigating to `http://127.0.0.1:8000/docs` in your web browser.

## Notes

- Always ensure that the virtual environment is activated when working on the project.
- Keep the `.env` file secure and avoid committing it to public version control repositories.
- If you make changes to the `.env` file, you will need to restart the server to apply these changes.
