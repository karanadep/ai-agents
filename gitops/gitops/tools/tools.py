import os

from google.adk.tools.mcp_tool import MCPToolset, StreamableHTTPConnectionParams
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

from dotenv import load_dotenv

load_dotenv()

argocd_tools = MCPToolset(
    # errlog=None,
    connection_params=StdioConnectionParams(
        server_params = StdioServerParameters(
            command='npx',
            args=[
                "-y",
                "argocd-mcp@latest",
                "stdio"
            ],
            env={
                "ARGOCD_BASE_URL": os.getenv("ARGOCD_BASE_URL"),
                "ARGOCD_API_TOKEN": os.getenv("ARGOCD_API_TOKEN"),
                # Add this if you are using self-signed certificates
                # "NODE_TLS_REJECT_UNAUTHORIZED": "0",                
            }
        ),
    ),
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

jira_tools = MCPToolset(
    connection_params=StreamableHTTPConnectionParams(
        url="http://localhost:3000/mcp/",
        headers={
                "JIRA_URL": os.getenv("JIRA_URL"),
                "JIRA_USERNAME": os.getenv("JIRA_USERNAME"),
                "JIRA_API_TOKEN": os.getenv("JIRA_API_TOKEN"),
        },
    ),
    tool_filter=[
        "jira_get_issue",
        "jira_search",
        "jira_create_issue",
        "jira_update_issue",
        "jira_transition_issue",
        "jira_add_comment",
    ],
)

# kubernetes_tools = MCPToolset(
#     errlog=None,
#     connection_params=StdioConnectionParams(
#         server_params = StdioServerParameters(
#             command='npx',
#             args=[
#                 "-y",
#                 "kubernetes-mcp-server@latest",
#             ],
#             env={
#                 "KUBECONFIG": "/path/to/your/kubeconfig"
#             }
#         ),
#     ),
#     # You can filter for specific Maps tools if needed:
#     tool_filter=[
#         "configuration_contexts_list",
#         "configuration_view",
#         "events_list",
#         "namespaces_list",
#         "projects_list",
#         "pods_list",
#         "pods_list_in_namespace",
#         "pods_get",
#         "pods_delete",
#         "pods_top",
#         "pods_exec",
#         "pods_log",
#         "pods_run",
#         "resources_list",
#         "resources_get",
#         "resources_create_or_update",
#         "resources_delete",
#         "helm_install",
#         "helm_list",
#         "helm_uninstall"
#     ],
# )

# The agent uses GitHub MCP tools directly for all operations
# No additional helper functions needed - the agent leverages the MCP tools
