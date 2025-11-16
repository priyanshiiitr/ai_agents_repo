# AI Summary Evaluator

This is a full-stack application that uses a Large Language Model (LLM) to evaluate a student's summary of a lecture transcript based on selected criteria.

## Project Structure

- `backend/`: FastAPI application that handles the core logic.
- `frontend/`: React single-page application for the user interface.
- `Dockerfile.backend`: Containerizes the FastAPI service.
- `Dockerfile.frontend`: Containerizes the React service (using a multi-stage build).
- `docker-compose.yml`: Orchestrates the services for local development.

## How to Run

1.  **Prerequisites**:
    - Docker
    - Docker Compose

2.  **Configuration**:
    - Copy `.env.example` to a new file named `.env`.
    - Open `.env` and replace `your_openai_api_key_here` with your actual OpenAI API key.
    - If you don't have an API key, the backend will use a mocked response for demonstration purposes.

3.  **Build and Run**:
    - Open your terminal in the project's root directory.
    - Run the command:
      ```bash
      docker-compose up --build
      ```

4.  **Access the Application**:
    - Frontend (React App): [http://localhost:3000](http://localhost:3000)
    - Backend (API Docs): [http://localhost:8000/docs](http://localhost:8000/docs)
