from pathlib import Path

HEADER_NINJA_TASK_ID = "x-ninja-task-id"
HEADER_NINJA_CONVERSATION_ID = "x-ninja-conversation-id"
HEADER_NINJA_EVENT_ID = "x-ninja-event-id"
HEADER_NINJA_SANDBOX_ID = "x-ninja-sandbox-id"
HEADER_NINJA_FEATURE = "x-ninja-feature"

LABEL_GENERATE_TASK_TITLE = "Generate Task Title"
DEFAULT_TASK_TITLE = "User prompt"

# Runtime metadata file paths — single source of truth used across the codebase
AGENT_SETTINGS_PATH = Path.home() / ".agent_settings.json"
COST_LIMIT_PATH = Path.home() / ".cost_limit.json"
SANDBOX_METADATA_PATH = Path("/dev/shm/sandbox_metadata.json")
MCP_TOKEN_PATH = Path("/dev/shm/mcp-token")
PH_METADATA_PATH = Path("/dev/shm/ph_metadata.json")
ORCHESTRATOR_CONFIG_PATH = Path.home() / ".orchestrator_config.json"

DEFAULT_ORCHESTRATOR_CONFIG = {
    "enabled": True,
    "updated_at": None,
}

SYSTEM_PROMPT_PATH = Path(__file__).parent / "system_prompt.txt"
SYSTEM_PROMPT_PATH_SINGLE = Path(__file__).parent / "system_prompt_single.txt"
SYSTEM_PROMPT_PATH_ORCHESTRATOR = (
    Path(__file__).parent / "system_prompt_orchestrator.txt"
)
SYSTEM_PROMPT_CODEX_PATH = Path(__file__).parent / "system_prompt_codex.txt"
SYSTEM_PROMPT_SINGLE_CODEX_PATH = (
    Path(__file__).parent / "system_prompt_single_codex.txt"
)
SYSTEM_PROMPT_ORCHESTRATOR_CODEX_PATH = (
    Path(__file__).parent / "system_prompt_orchestrator_codex.txt"
)
AGENTS_MD_CODEX_PATH = Path(__file__).parent / "agent-docs" / "AGENTS.md"
# Stop-hook chained orchestrator cycles (see orchestrator_stop_hook.py)
STOP_HOOKS_FEATURE_FLAG = "orchestrator-stop-hooks"

MONITOR_SERVICE_NAME = "monitor"
ORCHESTRATOR_SERVICE_NAME = "orchestrator"
UPGRADE_SERVICE_NAME = "upgrade"

# Timeout passed to the claude binary
CLAUDE_RUN_MONITOR_TIMEOUT_SECONDS = 7200  # 2 hours
CLAUDE_RUN_ORCHESTRATOR_TIMEOUT_SECONDS = 10800  # 3 hours

CODEX_RUN_ORCHESTRATOR_TIMEOUT_SECONDS = 7200  # 2 hours
CODEX_RUN_MONITOR_TIMEOUT_SECONDS = 7200

DEFAULT_MODEL = "claude-opus-4-8"

CODEX_HARNESS_MODEL = ["gpt-5.6-sol"]
MONITOR_TURNS_THRESHOLD = 60
MONITOR_MINUTES_THRESHOLD = 5
HANDOFF_CONTEXT = (
    "This task has used up the budget for a single monitor turn — either too "
    "many steps or too much wall-clock time. Stop working on it now. "
    "Summarize the progress you have made, create a github issue describing "
    "the remaining work, and tell the user in the channel, quoting the issue "
    "number. The background agent owns this task from here: do NOT keep "
    "working on it, and do NOT pick it back up if the user asks about it "
    "later — report the issue's status instead and let the background agent "
    "finish it."
)
CODEX_CONFIG_DIR = Path.home() / ".codex"
CODEX_LOG_DIR = CODEX_CONFIG_DIR / "sessions"
CODEX_CONFIG_FILE = CODEX_CONFIG_DIR / "config.toml"
CODEX_SETTINGS_FILE = CODEX_CONFIG_DIR / "codex_settings.json"

COMMON_LOGGER_NAME = "common"

# These env vars are used by the Codex harness to set the headers for the request
ENV_VAR_TASK_ID = "NINJA_TASK_ID"
ENV_VAR_FEATURE = "NINJA_FEATURE"
ENV_VAR_CONVERSATION_ID = "NINJA_CONVERSATION_ID"


# Prompts
CONTINUE_WORKFLOW_PROMPT = "Continue working on the task"
