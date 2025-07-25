# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Installation & Setup
```bash
pip install -r requirements.txt
```

Required environment variables:
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env file and add your API keys
OPENAI_API_KEY=your-openai-api-key-here
ANTHROPIC_API_KEY=your-anthropic-api-key-here
GOOGLE_API_KEY=your-google-api-key-here
GROQ_API_KEY=your-groq-api-key-here
```

### Testing
```bash
# Run all tests
pytest tests/

# Run specific test file with verbose output
pytest tests/test_config_loader.py -v

# Run with coverage reporting
pytest tests/ --cov=src --cov-report=html

# Run single test method
pytest tests/test_config_loader.py::TestConfigLoader::test_load_valid_config -v
```

### Running Examples
```bash
# Run comprehensive test suite
python run_tests.py --all

# Run specific test categories
python run_tests.py --unit      # Unit tests
python run_tests.py --integration  # Integration tests
python run_tests.py --lint      # Code quality checks
python run_tests.py --quick     # Quick smoke test

# Run usage examples (requires API keys)
python examples/usage_examples.py

# Test specific agent configuration
python -c "
from src.core.configurable_agent import ConfigurableAgent
agent = ConfigurableAgent('configs/examples/research_agent.yml')
print(agent.run('test query'))
"
```

## Architecture Overview

This is a **template-driven configurable agent system** built on LangGraph's prebuilt ReAct agents. The core philosophy is that agents are entirely configured through YAML files without code changes.

### Key Architectural Concepts

**Configuration-First Design**: All agent behavior (LLM, prompts, tools, memory) is defined in YAML configuration files. The system uses LangGraph's optimized `create_react_agent()` for the core reasoning loop.

**Component Initialization Flow**:
1. `ConfigurableAgent` loads YAML → validates with Pydantic models
2. `_setup_llm()` → creates LLM instance based on provider (OpenAI/Anthropic)
3. `_setup_tools()` → registers built-in and custom tools via `ToolRegistry`
4. `_setup_memory()` → initializes `MemoryManager` if enabled
5. `_setup_graph()` → uses `create_react_agent()` with LLM and tools

**ReAct Pattern**: Uses LangGraph's prebuilt ReAct (Reasoning + Acting) agent which follows the pattern of reasoning about the problem and taking actions with tools. This is more efficient than custom graph construction.

**State Management**: The ReAct agent manages its own internal state with messages flowing through the reasoning loop. Memory integration happens at the input/output level.

### Core Components

**src/core/configurable_agent.py** - Main orchestrator class that ties everything together. Entry point for creating agents from config files.

**src/core/config_loader.py** - Pydantic models for YAML validation and configuration parsing. Handles environment variable resolution for API keys.

**src/memory/memory_manager.py** - LangMem integration supporting three memory types: semantic (facts), episodic (conversations), procedural (successful patterns). Includes cleanup based on retention policies.

**src/optimization/prompt_optimizer.py** - A/B testing framework for prompts with automatic evolution based on performance metrics. Generates variants and tracks performance.

**src/optimization/feedback_collector.py** - Collects automatic and user feedback for prompt optimization, including response time, token efficiency, and success rates.

**src/tools/tool_registry.py** - Manages built-in tools (web_search, calculator, file_reader, file_writer, code_executor) and custom tool registration.

### Configuration Structure

Agent configurations have simplified sections for ReAct pattern:

- **agent**: Metadata (name, description, version)
- **llm**: Provider, model, parameters, API key env var
- **prompts**: Templates with variable substitution (primarily system_prompt)
- **tools**: Lists of built-in tools and custom tool definitions
- **memory**: LangMem configuration for semantic/episodic/procedural memory
- **react**: Simple ReAct configuration (max_iterations, recursion_limit)
- **optimization**: Prompt optimization and performance tracking settings
- **runtime**: Execution limits and debug settings

### ReAct Agent Pattern

The ReAct (Reasoning + Acting) pattern simplifies agent behavior:

- **Reasoning**: The agent thinks about the problem step by step
- **Acting**: The agent uses tools when needed to gather information or perform actions
- **Observation**: The agent processes tool results and continues reasoning
- **Final Answer**: The agent provides a comprehensive response

This eliminates the need for complex graph configurations while providing robust reasoning capabilities.

### Memory Architecture

Three-tier memory system:
- **Semantic**: Key facts extracted from interactions (simple NLP patterns)
- **Episodic**: Full conversation history with cleanup policies
- **Procedural**: Successful interaction patterns with usage counters

Memory operations are integrated into graph nodes and can be configured per-agent.

### Testing Patterns

Tests are organized by component with fixtures for configurations. Key testing patterns:
- Mock API keys via environment variables in tests
- Use temporary files for YAML config testing
- Pydantic validation testing for config edge cases
- Tool registry testing with custom tool registration
- Memory manager testing with different memory types enabled/disabled

### Common Debugging

When agents fail to initialize, check:
1. API key environment variables are set
2. YAML configuration validates against Pydantic models
3. Custom tools can be imported from specified module paths
4. Graph configuration has valid entry point and connected nodes

The `debug_mode: true` runtime setting provides additional logging during graph execution.

**ReAct Agent Integration**: The system uses LangGraph's prebuilt `create_react_agent()` which handles state management internally. The ReAct pattern provides a more reliable and optimized approach than custom graph construction.

**System Prompt Integration**: System prompts are prepended to the message list when invoking the ReAct agent, ensuring proper context setting without complex state management.