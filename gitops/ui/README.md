## Setup and Installation

    *   Python 3.11+
    *   Streamlit

    
    ```
    brew install streamlit
    ```

## Configurations

        ```bash
        export GOOGLE_CLOUD_PROJECT=<your-project-id>
        ```

## Running UI Locally

```
uv run streamlit run main.py --server.port=8080 --server.enableCORS=false
```

## Deployment to Cloud Run

### Create an Artifact Registry repository.

This is where we'll store the agent container image.

```bash
gcloud artifacts repositories create adk-agents-ui \
  --repository-format=docker \
  --location=us-central1 \
  --description="Repository for ADK agents" \
  --project=$GOOGLE_CLOUD_PROJECT
```

### Containerize the ADK Python agent. 

Build the container image and push it to Artifact Registry with Cloud Build.

```bash
gcloud builds submit --region=us-central1 --tag us-central1-docker.pkg.dev/$GOOGLE_CLOUD_PROJECT/adk-agents-ui/gitops-ui:latest
```

### Deploy the agent to Cloud Run 

```bash
gcloud run deploy gitops \
  --image=us-central1-docker.pkg.dev/$GOOGLE_CLOUD_PROJECT/adk-agents-ui/gitops-ui:latest \
  --region=us-central1 \
  --allow-unauthenticated
```