from conductor.ai.agents import Agent, AgentRuntime, ToolDef
from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.authentication_settings import AuthenticationSettings
  
config = Configuration(
    server_api_url="<url>",
    authentication_settings=AuthenticationSettings(
        key_id="<key>",
        key_secret="<secret>",
    ),
)

weather_lookup = ToolDef(
      name="weather_lookup",   
      description="Look up current weather for a city.",
      input_schema={
          "type": "object",
          "properties": {"city": {"type": "string"}},
          "required": ["city"],
      },
      output_schema={"type": "object"},
      tool_type="worker",
  ) 

agent = Agent(
    name="weather_agent",
    model="OpenAI/gpt-4o-mini",
    instructions=(
        "You are a weather assistant. Use the weather_lookup tool to look up "
        "current weather for each city the user asks about. Report results "
        "in a clean, readable format. If the user doesn't specify cities, "
        "ask them which cities they'd like weather for."
    ),
    tools=[weather_lookup],
    max_turns=10,
    timeout_seconds=120,
)

if __name__ == "__main__":
    with AgentRuntime(config) as runtime:
        runtime.deploy(agent)
