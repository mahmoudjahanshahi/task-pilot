# TaskPilot – Multi-Agent Action Extraction Assistant with Azure OpenAI

TaskPilot is a multi-agent assistant that takes messy notes or transcripts and turns them into:
- Cleaned text
- Summaries
- Extracted action items with ownership and due dates

It uses Azure OpenAI, Semantic Kernel agents, and FastAPI to demonstrate a modular, LLM-powered architecture.

---

## Objective

Build an AI-powered assistant that can:
- Clean and process unstructured input (e.g., meeting notes)
- Summarize the core content into bullet points
- Extract actionable tasks with owner and deadlines
- Demonstrate multi-agent reasoning with clear roles

---

## What It Uses

- **Azure OpenAI** – For summarization and task extraction using LLMs
- **Semantic Kernel (Python SDK)** – For defining and orchestrating agents
- **FastAPI** – For serving the web app interface
- **Tailwind CSS** – For clean and responsive UI styling
- **Azure App Service** – For hosting the deployed app

---

## Deployment

### Required Environment Variables

In the Azure portal, go to **Settings > Environment variables**, and add the following environment variables:

- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_API_VERSION`
- `AZURE_OPENAI_DEPLOYMENT_NAME`

### Startup Command

In **App Service > Settings > Configuration**, set the following startup command:

```bash
gunicorn -w 1 -k uvicorn.workers.UvicornWorker app.main:app
```

### GitHub Deployment (Recommended)

- Connect your repo in Deployment Center via GitHub Actions
- Azure will auto-deploy on pushes to main
- All secrets should be configured via the App Service settings panel
