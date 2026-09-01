from conductor.ai.agents import Agent, AgentRuntime, ToolDef
from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.authentication_settings import AuthenticationSettings
from conductor.ai.agents.guardrail import RegexGuardrail

config = Configuration(
    server_api_url="<url>",
    authentication_settings=AuthenticationSettings(
        key_id="<key>",
        key_secret="<secret>",
    ),
)

no_emails = RegexGuardrail(
    patterns=[r"[\w.+-]+@[\w-]+\.[\w.-]+"],
    name="no_pii",
    message="Response must not contain email addresses.",
    on_fail="retry",
)

agent = Agent(
    name="support_reply_agent",
    model="OpenAI/gpt-4o-mini",
    instructions=(
        "Draft a short customer support reply confirming an order."
    ),
    guardrails=[no_emails],
    max_turns=10,
    timeout_seconds=120,
)

if __name__ == "__main__":
    with AgentRuntime(config) as runtime:
        runtime.deploy(agent)
