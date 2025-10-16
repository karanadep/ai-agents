import datetime
import os
import requests

from google.adk.tools.mcp_tool import MCPToolset, StreamableHTTPConnectionParams
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# argocd_tools = MCPToolset(
#     connection_params=StreamableHTTPConnectionParams(
#         url="http://localhost:3000/mcp/",
#         headers={
#             "x-argocd-base-url": os.getenv("ARGOCD_BASE_URL"),
#             "x-argocd-api-token": os.getenv("ARGOCD_API_TOKEN"),
#         },
#     ),
#     # Read only tools
#     tool_filter=[
#         "list_applications",
#         "get_application",
#         "create_application",
#         "update_application",
#         "delete_application",
#         "sync_application",
#         "get_application_resource_tree",
#         "get_application_managed_resources",
#         "get_application_workload_logs",
#         "get_resource_events",
#         "get_resource_actions",
#         "run_resource_action",
#     ],
# )

argocd_tools = MCPToolset(
    errlog=None,
    connection_params=StdioConnectionParams(
        server_params = StdioServerParameters(
            command='npx',
            args=[
                "-y",
                "argocd-mcp@latest",
            ],
            # Pass the API key as an environment variable to the npx process
            # This is how the MCP server for Google Maps expects the key.
            env={
                "ARGOCD_BASE_URL": os.getenv("ARGOCD_BASE_URL"),
                "ARGOCD_API_TOKEN": os.getenv("ARGOCD_API_TOKEN"),
            }
        ),
    ),
    # You can filter for specific Maps tools if needed:
    tool_filter=[
        "list_applications",
        "get_application",
        "create_application",
        "update_application",
        "delete_application",
        "sync_application",
        "get_application_resource_tree",
        "get_application_managed_resources",
        "get_application_workload_logs",
        "get_resource_events",
        "get_resource_actions",
        "run_resource_action",
    ],
)

github_tools = MCPToolset(
    errlog=None,    
    connection_params=StreamableHTTPConnectionParams(
        url="https://api.githubcopilot.com/mcp/",
        headers={
            "Authorization": "Bearer " + os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN"),
        },
    ),
    # Read only tools
    tool_filter=[
        "search_repositories",
        "search_issues",
        "list_issues",
        "get_issue",
        "list_pull_requests",
        "get_pull_request",
        "create_pull_request",
        "merge_pull_request",
        "pull_request_review_write",
        "create_branch",
        "create_or_update_file",
        "get_file",
        "list_files",
        "get_directory_contents",
        "add_comment_to_pending_review",
        "request_copilot_review",
        "update_pull_request",
        "update_pull_request_branch",
        "create_pull_request_with_copilot",
        "get_file_contents",
        "search_code"
    ],
)