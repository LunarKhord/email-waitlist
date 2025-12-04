
# 🚀 Email-Waitlist API

A lightweight, high-performance backend built with **FastAPI** to securely capture and immediately forward early access emails for the landing page.

## 🌟 Overview

This API handles the single critical task of collecting email addresses from the landing page's waitlist form and **immediately forwarding the data** to a designated external service (e.g., Mailchimp, ConvertKit, SendGrid, or a logging service). **No internal persistent database or complex schema management is required.**

**Built With:**

  * **Python 3.10+**
  * **Package Manager: `uv`** (for fast dependency management and environment creation)
  * **FastAPI:** High-performance, easy-to-use web framework.
  * **Pydantic:** Data validation and settings management.
  * **Requests/HTTPX:** Library for making outbound API calls (to the EMP/service).
  * **Uvicorn:** ASGI server for running the application.

## 🛠️ Local Setup

Follow these steps to get your development environment running using the `uv` package manager.

### 1\. Prerequisites

Ensure you have Python 3.10+ installed and the `uv` tool installed globally.

```bash
# Example command to install uv
pip install uv
```

### 2\. Clone the Repository

```bash
git clone https://github.com/LunarKhord/email-waitlist.git
cd email-waitlist
```

### 3\. Setup Virtual Environment and Install Dependencies (using `uv`)

The `uv` tool handles both environment creation and dependency installation in one swift step.

```bash
# Create and activate environment, and install dependencies from requirements.txt
uv sync
```

*(Ensure `requests` or `httpx` is included in your `requirements.txt` for outbound API calls.)*

### 4\. Run the Application

Start the development server using Uvicorn. Since `uv` manages the environment, use `uv run`:

```bash
uv run uvicorn main:app --reload
```

The server will now be running at: `http://127.0.0.1:8000`

## 📂 API Endpoints and Data Forwarding

The root endpoint for waitlist submission is `/api/v1/waitlist`.

| Endpoint | Method | Description | Request Body Example | Response Codes |
| :--- | :--- | :--- | :--- | :--- |
| `/api/v1/waitlist` | **POST** | **Validates and immediately forwards** the email and industry data to the configured external service. | `{"email": "user@example.com", "industry": "HVAC"}` | 201 Created (Success), 400 Bad Request (Validation), 500 Internal Error (Forwarding Failure) |
| `/api/v1/health` | GET | Basic health check to confirm the service is running. | N/A | 200 OK |

### **Important: Data Forwarding**

This API is configured to make an outbound POST request to a third-party service defined by the `FORWARDING_API_URL` environment variable.

  - **Success:** If the forwarding API returns a 2xx status code, the client receives a **201 Created**.
  - **Failure:** If the forwarding API fails (e.g., a 4xx or 5xx status from Mailchimp), the server logs the error and returns a **500 Internal Server Error** to the client.

## ⚙️ Configuration (Environment Variables)

The application relies heavily on environment variables for external service integration.

| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `FORWARDING_API_URL` | `None` | **CRITICAL:** The URL of the third-party service (e.g., Mailchimp list endpoint). |
| `FORWARDING_API_KEY` | `None` | **CRITICAL:** The secret API key/token required to authenticate the outbound POST request. |
| `CORS_ORIGINS` | `http://localhost:3000` | Comma-separated list of front-end origins allowed to call this API (your landing page domain). |

To set environment variables, create a `.env` file in the root directory.

## 🔑 CORS Policy

This API implements CORS (Cross-Origin Resource Sharing) to restrict which domains can submit data. The allowed origins are configured via the `CORS_ORIGINS` environment variable. **Ensure your production landing page URL is added to this list before deployment.**
