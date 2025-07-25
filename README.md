# Configurable LangGraph Agents

A flexible, template-driven system for creating configurable AI agents using LangGraph's prebuilt ReAct pattern, with integrated memory management via LangMem and dynamic prompt optimization.

## Features

- **YAML Configuration**: Complete agent configuration through YAML files
- **LLM Flexibility**: Support for OpenAI, Anthropic, and other providers
- **ReAct Agent Pattern**: Uses LangGraph's optimized ReAct (Reasoning + Acting) agents
- **Memory Integration**: LangMem integration for semantic, episodic, and procedural memory
- **Prompt Optimization**: Dynamic prompt improvement with A/B testing
- **Tool Registry**: Built-in and custom tool management
- **Template System**: Reusable agent templates for different use cases

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Environment Setup

1. Copy the example environment file and add your API keys:
```bash
cp .env.example .env
```

2. Edit the `.env` file and add your API keys:
```bash
# OpenAI API Key
OPENAI_API_KEY=your-openai-api-key-here

# Anthropic API Key  
ANTHROPIC_API_KEY=your-anthropic-api-key-here

# Google Gemini API Key
GOOGLE_API_KEY=your-google-api-key-here

# Groq API Key
GROQ_API_KEY=your-groq-api-key-here
```

**Note**: The `.env` file is automatically loaded by the application. Make sure to add `.env` to your `.gitignore` file to keep your API keys secure.

### Basic Usage

```python
from src.core.configurable_agent import ConfigurableAgent

# Create agent from configuration
agent = ConfigurableAgent("configs/examples/research_agent.yml")

# Run a query
response = agent.run("What are the latest developments in quantum computing?")
print(response["response"])
```

### Async Usage

```python
import asyncio

async def main():
    agent = ConfigurableAgent("configs/examples/research_agent.yml")
    response = await agent.arun("Tell me about machine learning")
    print(response["response"])

asyncio.run(main())
```

## Configuration Structure

### Basic Configuration

```yaml
# Agent Information
agent:
  name: "My Agent"
  description: "Agent description"
  version: "1.0.0"

# LLM Configuration
llm:
  provider: "openai"  # or "anthropic", "gemini", "groq"
  model: "gpt-4o-mini"
  temperature: 0.7
  max_tokens: 2000
  api_key_env: "OPENAI_API_KEY"

# Prompts with Variables
prompts:
  system_prompt:
    template: "You are a helpful assistant. Context: {context}"
    variables: ["context"]
  user_prompt:
    template: "User query: {query}"
    variables: ["query"]

# ReAct Configuration
react:
  max_iterations: 10
  recursion_limit: 50
```

### Memory Configuration

```yaml
memory:
  enabled: true
  provider: "langmem"
  types:
    semantic: true    # Facts and knowledge
    episodic: true    # Conversation history
    procedural: true  # Learned patterns
  storage:
    backend: "memory"  # or "postgres", "redis"
  settings:
    max_memory_size: 5000
    retention_days: 30
    background_processing: true
```

### Tools Configuration

```yaml
tools:
  built_in:
    - "web_search"
    - "calculator"
    - "file_reader"
    - "file_writer"
    - "code_executor"
  custom:
    - name: "custom_tool"
      module_path: "my.custom.tools"
      class_name: "MyTool"
      description: "My custom tool"
      parameters:
        param1: "value1"
```

### Optimization Configuration

```yaml
optimization:
  enabled: true
  prompt_optimization:
    enabled: true
    feedback_collection: true
    ab_testing: true
    optimization_frequency: "weekly"
  performance_tracking:
    enabled: true
    metrics:
      - "response_time"
      - "accuracy"
      - "user_satisfaction"
```

## Example Configurations

### Research Agent
```bash
python examples/usage_examples.py
```

Specialized for research tasks with web search, information synthesis, and memory.

### Coding Assistant
```bash
agent = ConfigurableAgent("configs/examples/coding_assistant.yml")
response = agent.run("Write a Python function to calculate fibonacci numbers")
```

Optimized for software development with code execution and file operations.

### Customer Support
```bash
agent = ConfigurableAgent("configs/examples/customer_support.yml")
response = agent.run("I need help with my order")
```

Designed for customer service with escalation and satisfaction tracking.

### Gemini Research Agent
```bash
agent = ConfigurableAgent("configs/examples/gemini_agent.yml")
response = agent.run("What are the latest developments in quantum computing?")
```

Powered by Google's latest Gemini 2.5 Flash model for research and analysis tasks.

### Groq Coding Assistant
```bash
agent = ConfigurableAgent("configs/examples/groq_agent.yml")
response = agent.run("Write a Python function to calculate fibonacci numbers")
```

Powered by Groq's fast LLMs (including Meta's Llama-4-Scout) for rapid code generation and development.

## Advanced Features

### Custom Tools

```python
from langchain_core.tools import tool

@tool
def my_custom_tool(query: str) -> str:
    \"\"\"Custom tool description.\"\"\"
    return f"Processed: {query}"

# Register with agent
agent.tool_registry.register_function_as_tool(
    name="my_tool",
    func=my_custom_tool,
    description="My custom tool"
)
```

### Dynamic Prompt Updates

```python
# Update prompts at runtime
agent.update_prompts({
    "system_prompt": "New system prompt template"
})
```

### Memory Management

```python
# Get memory statistics
stats = agent.get_memory_stats()
print(f"Stored facts: {stats['semantic_facts']}")

# Export conversation history
history = agent.export_conversation()

# Clear memory
agent.clear_memory()
```

### Optimization and Feedback

```python
from src.optimization.prompt_optimizer import OptimizationMetric

# Record feedback for optimization
agent.prompt_optimizer.record_feedback(
    prompt_type="system_prompt",
    variant_id="variant_1",
    metrics={
        OptimizationMetric.USER_SATISFACTION: 0.9,
        OptimizationMetric.ACCURACY: 0.85
    }
)

# Run optimization
optimized_prompts = agent.prompt_optimizer.optimize_prompts()
```

## ReAct Agent Pattern

The ReAct (Reasoning + Acting) pattern provides:

- **Reasoning**: Step-by-step problem analysis
- **Acting**: Tool usage when information is needed
- **Observation**: Processing tool results
- **Final Response**: Comprehensive answer synthesis

This eliminates complex graph configuration while providing robust reasoning capabilities.

## Testing

```bash
# Run all tests
python run_tests.py

# Run specific test categories
python run_tests.py --unit      # Unit tests only
python run_tests.py --integration  # Integration tests only
python run_tests.py --lint      # Code quality checks
python run_tests.py --quick     # Quick smoke test

# With coverage report
python run_tests.py --unit --coverage

# For detailed output
python run_tests.py --all --verbose
```

See `TEST_RUNNER.md` for complete documentation.

## Architecture

```
src/
├── core/
│   ├── configurable_agent.py    # Main agent class
│   └── config_loader.py         # Configuration management
├── memory/
│   └── memory_manager.py        # LangMem integration
├── optimization/
│   ├── prompt_optimizer.py      # Prompt optimization
│   └── feedback_collector.py    # Feedback collection
└── tools/
    └── tool_registry.py         # Tool management
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:
- Check the [examples](examples/) directory
- Review the [test files](tests/) for usage patterns
- Create an issue on GitHub

## Roadmap

- [ ] Additional LLM provider support (Ollama, Cohere)
- [ ] Web UI for agent configuration
- [ ] Multi-agent coordination
- [ ] Advanced memory backends (vector databases)
- [ ] Monitoring and analytics dashboard
- [ ] Plugin system for custom components