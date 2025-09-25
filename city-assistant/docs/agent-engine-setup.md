0. review notes

- https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/set-up

1. Service account

- Default Service Agent: By default, agents use the `AI Platform Reasoning Engine Service Agent`. This Google-managed service account has the `Vertex AI Reasoning Engine Service Agent` role (roles/aiplatform.reasoningEngineServiceAgent), which includes the default permissions required for deployed agents.
- AI Platform Reasoning Engine Service Agent (service-PROJECT_NUMBER@gcp-sa-aiplatform-re.iam.gserviceaccount.com)

2. Create a bucket

- Bucket name: 

3. Troubleshooting

- https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/troubleshooting/deploy