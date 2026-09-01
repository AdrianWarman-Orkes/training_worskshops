from conductor.ai.agents import Agent, AgentRuntime, ToolDef
from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.authentication_settings import AuthenticationSettings
from conductor.ai.agents.guardrail import LLMGuardrail

config = Configuration(
    server_api_url="<url>",
    authentication_settings=AuthenticationSettings(
        key_id="<key>",
        key_secret="<secret>",
    ),
)

no_financial_advice = LLMGuardrail(
    model="OpenAI/gpt-4o-mini",
    policy="Reject any response that gives specific financial or investment advice, such as recommending a particular stock, fund, or asset.",
    name="no_financial_advice",
    on_fail="retry",
)

agent = Agent(
    name="support_agent_llm_guard",
    model="OpenAI/gpt-4o-mini",
    instructions=(
        "You are a customer support agent for a budgeting app. Answer the user's question helpfully."
    ),
    guardrails=[no_financial_advice],
    max_turns=10,
    timeout_seconds=120,
)

if __name__ == "__main__":
    with AgentRuntime(config) as runtime:
        runtime.deploy(agent)
