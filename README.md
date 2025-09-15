# Rent-Me Backend API

This is the backend API for the Rent-Me application, built with FastAPI and MongoDB.

## Installation

1.  **Clone the repository** (if you haven't already):
    ```bash
    git clone <repository-url>
    cd rent-me-backend
    ```

2.  **Create and activate a virtual environment:**
    From the root `rent-me-backend` directory:
    ```bash
    # Create the virtual environment
    python -m venv venv

    # Activate on Windows (PowerShell)
    .\venv\Scripts\Activate.ps1
    
    # Or on Windows (Command Prompt)
    # venv\Scripts\activate
    
    # Activate on macOS/Linux
    # source venv/bin/activate
    ```

3.  **Install dependencies:**
    With your virtual environment active, run:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up Environment Variables:**
    Create a file named `.env` in the root directory. Add the following variables with your own values:
    ```
    MONGO_DATABASE_URI="your_mongodb_connection_string"
    JWT_SECRET_KEY="a_very_strong_and_random_secret_key"
    ```

## Running the Project

1.  **Start the development server:**
    From the root directory (`rent-me-backend`), run the following command:
    ```bash
    uvicorn app.main:app --reload
    ```
    This command tells the `uvicorn` server to run the FastAPI instance named `app` located in the `app/main.py` file and to automatically reload on any code changes.

2.  **Access the API:**
    -   The API will be running at `http://127.0.0.1:8000`.
    -   Interactive API documentation is available at `http://127.0.0.1:8000/docs`.

---
For more details, see the code and configuration files in the `app/` directory.