# Configurable LangGraph Agents

A flexible, template-driven system for creating configurable AI agents using LangGraph's prebuilt ReAct pattern, with integrated memory management via LangMem, dynamic prompt optimization, and **hierarchical agent teams** with sophisticated coordination and routing algorithms.

## 🚀 Features

### Core Agent Features
- **YAML Configuration**: Complete agent configuration through YAML files
- **LLM Flexibility**: Support for OpenAI, Anthropic, Google Gemini, Groq, and other providers
- **ReAct Agent Pattern**: Uses LangGraph's optimized ReAct (Reasoning + Acting) agents
- **Memory Integration**: LangMem integration for semantic, episodic, and procedural memory
- **Prompt Optimization**: Dynamic prompt improvement with A/B testing
- **Tool Registry**: Built-in and custom tool management
- **Template System**: Reusable agent templates for different use cases

### 🏢 Hierarchical Agent Teams
- **Three-tier Architecture**: Coordinator → Supervisors → Workers
- **Intelligent Routing**: Advanced algorithms for optimal task delegation
- **Dynamic Team Management**: Add/remove agents and teams at runtime
- **Cross-team Communication**: Enable collaboration between teams
- **Performance Monitoring**: Real-time metrics and analytics
- **Configuration-driven**: All behavior defined through YAML configs

### 🧠 Advanced Routing Strategies
- **Keyword-based**: Route by matching task keywords to agent capabilities
- **LLM-based**: Use language models for intelligent routing decisions
- **Rule-based**: Route using predefined business rules
- **Capability-based**: Match tasks to agent specializations
- **Workload-based**: Balance load across available agents
- **Performance-based**: Route to highest-performing agents
- **Hybrid**: Combine multiple strategies for optimal results

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

```bash
python3 setup.py
```

This will:
- Create a virtual environment
- Install all dependencies
- Set up the `.env` file
- Test the installation

### Option 2: Manual Setup

1. **Create virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp env.example .env
   ```

4. **Edit the `.env` file and add your API keys**:
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

## 🎯 Basic Usage

### Single Agent

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

### Hierarchical Agent Teams

```python
from src.hierarchical.hierarchical_agent import HierarchicalAgentTeam

# Create hierarchical team
team = HierarchicalAgentTeam(
    name="research_team",
    coordinator_config='configs/examples/hierarchical/research_pipeline_team.yml'
)

# Run a complex task
result = team.run("Research the latest developments in AI agents and write a summary")
print(result['response'])

# Get team statistics
stats = team.get_hierarchy_info()
print(f"Total teams: {stats['total_teams']}")
print(f"Total workers: {stats['total_workers']}")
```

## 🖥️ Web Interfaces

### Basic Agent Web UI

```bash
# Launch the basic web interface
python run_web_ui.py
# Or directly with streamlit
streamlit run web_ui.py
```

### Hierarchical Agent Web UI

```bash
# Launch the hierarchical web interface
python run_hierarchical_ui.py
# Or directly with streamlit
streamlit run hierarchical_web_ui.py
```

Both web interfaces will be available at: http://localhost:8501

### Web UI Features

- **🎯 Multi-Tab Interface**: Organized tabs for agent info, LLM config, prompts, tools, memory, etc.
- **📝 Visual Configuration**: Form-based configuration with validation and help text
- **💾 File Operations**: Load example configs, upload/download YAML files
- **🔍 Live Preview**: Real-time YAML preview with validation
- **🧪 Agent Testing**: Test your configured agent directly in the interface
- **🚀 Quick Templates**: One-click loading of pre-configured agent templates
- **🏗️ Team Builder**: Visual hierarchical team builder with drag-and-drop
- **📊 Performance Dashboard**: Real-time metrics and analytics
- **🗂️ Agent Library**: Searchable catalog of available agent configurations

## 📁 Configuration Structure

### Basic Agent Configuration

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

### Hierarchical Team Configuration

```yaml
# Team Information
team:
  name: "Your Team Name"
  description: "Team description"
  version: "1.0.0"
  type: "hierarchical"

# Top-level Coordinator
coordinator:
  name: "Team Coordinator"
  description: "Coordinates between teams"
  llm:
    provider: "openai"
    model: "gpt-4o-mini"
    temperature: 0.3
    max_tokens: 2000
    api_key_env: "OPENAI_API_KEY"
  
  routing:
    strategy: "hybrid"  # keyword_based, llm_based, rule_based, hybrid
    fallback_team: "default_team"
    confidence_threshold: 0.8

# Teams Configuration
teams:
  - name: "specialist_team"
    description: "Team description"
    
    supervisor:
      name: "Team Supervisor"
      llm:
        provider: "openai"
        model: "gpt-4o-mini"
        temperature: 0.2
      routing:
        strategy: "capability_based"
        fallback_worker: "default_worker"
    
    workers:
      - name: "specialist_worker"
        role: "specialist"
        config_file: "configs/examples/specialist_agent.yml"
        description: "Specialized worker agent"
        capabilities: 
          - "specialized_task"
          - "domain_expertise"
        priority: 1

# Memory Configuration (Hierarchical)
memory:
  enabled: true
  provider: "langmem"
  levels:
    coordinator:
      enabled: true
      types: {semantic: true, episodic: true, procedural: true}
    team:
      enabled: true
      shared_across_workers: true
    worker:
      enabled: true
      individual: false

# Coordination Settings
coordination:
  cross_team_communication: true
  team_dependencies: 
    - "team_b depends on team_a"
  task_flow:
    type: "pipeline"  # sequential, parallel, conditional, pipeline
    max_parallel_tasks: 3
    timeout_per_task: 300

# Performance Monitoring
performance:
  monitoring:
    enabled: true
    metrics:
      - "response_time"
      - "task_success_rate"
      - "worker_utilization"
      - "decision_accuracy"
```

## 📚 Example Configurations

### Single Agents

#### Research Agent
```bash
python examples/usage_examples.py
```
Specialized for research tasks with web search, information synthesis, and memory.

#### Coding Assistant
```bash
agent = ConfigurableAgent("configs/examples/coding_assistant.yml")
response = agent.run("Write a Python function to calculate fibonacci numbers")
```
Optimized for software development with code execution and file operations.

#### Customer Support
```bash
agent = ConfigurableAgent("configs/examples/customer_support.yml")
response = agent.run("I need help with my order")
```
Designed for customer service with escalation and satisfaction tracking.

#### Gemini Research Agent
```bash
agent = ConfigurableAgent("configs/examples/gemini_agent.yml")
response = agent.run("What are the latest developments in quantum computing?")
```
Powered by Google's latest Gemini 2.5 Flash model for research and analysis tasks.

#### Groq Coding Assistant
```bash
agent = ConfigurableAgent("configs/examples/groq_agent.yml")
response = agent.run("Write a Python function to calculate fibonacci numbers")
```
Powered by Groq's fast LLMs (including Meta's Llama-4-Scout) for rapid code generation and development.

### Hierarchical Teams

#### 🔬 Research Pipeline Team
- **Flow**: Browser Agent → Research Analyst → Writer Agent
- **Use case**: Comprehensive research with web search, analysis, and content creation
- **Configuration**: `configs/examples/hierarchical/research_pipeline_team.yml`

#### 💻 Development Team
- **Flow**: Requirements → Development → QA
- **Use case**: Software development with analysis, coding, and testing
- **Configuration**: `configs/examples/hierarchical/development_team.yml`

#### 🎧 Customer Service Team
- **Flow**: Triage → Specialist → Escalation
- **Use case**: Customer support with routing and escalation handling
- **Configuration**: `configs/examples/hierarchical/customer_service_team.yml`

#### ✍️ Content Creation Team
- **Flow**: Research → Writing → Editorial
- **Use case**: Content creation with research, writing, and editing
- **Configuration**: `configs/examples/hierarchical/content_creation_team.yml`

## 🛠️ Advanced Features

### Custom Tools

```python
from langchain_core.tools import tool

@tool
def my_custom_tool(query: str) -> str:
    """Custom tool description."""
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

### Enhanced Routing for Hierarchical Teams

```python
from src.hierarchical.enhanced_routing import EnhancedRoutingEngine, RoutingStrategy, AgentCapability

# Create routing engine
routing_engine = EnhancedRoutingEngine(
    llm=your_llm,
    default_strategy=RoutingStrategy.HYBRID
)

# Register agents
web_agent = AgentCapability(
    agent_id="web_searcher",
    capabilities=["web_search", "information_gathering"],
    specialization_keywords=["search", "web", "internet"],
    priority=1
)
routing_engine.register_agent(web_agent)

# Route a task
decision = routing_engine.route_task(
    task_description="Find information about AI developments",
    available_agents=["web_searcher", "analyst", "writer"],
    strategy=RoutingStrategy.HYBRID
)

print(f"Selected agent: {decision.target}")
print(f"Confidence: {decision.confidence}")
print(f"Reasoning: {decision.reasoning}")
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

## 🔄 Task Flow Types

### Sequential Flow
Tasks are processed one after another through the team hierarchy.

```yaml
coordination:
  task_flow:
    type: "sequential"
    timeout_per_task: 300
```

### Parallel Flow
Multiple tasks can be processed simultaneously across teams.

```yaml
coordination:
  task_flow:
    type: "parallel"
    max_parallel_tasks: 5
```

### Pipeline Flow
Tasks flow through teams in a predefined pipeline sequence.

```yaml
coordination:
  task_flow:
    type: "pipeline"
    max_parallel_tasks: 3
```

### Conditional Flow
Task routing depends on specific conditions and results.

```yaml
coordination:
  task_flow:
    type: "conditional"
    timeout_per_task: 300
```

## 🎯 Use Cases

### Research & Analysis
- **Academic Research**: Multi-step research with web search, analysis, and report generation
- **Market Research**: Comprehensive market analysis with data gathering and insights
- **Competitive Intelligence**: Automated competitor analysis and reporting

### Software Development
- **Full-stack Development**: Requirements analysis, development, and testing
- **Code Review**: Automated code analysis, review, and improvement suggestions
- **DevOps**: Deployment, monitoring, and maintenance workflows

### Content Creation
- **Content Marketing**: Research, writing, editing, and SEO optimization
- **Technical Documentation**: API documentation, user guides, and tutorials
- **Social Media**: Content creation, scheduling, and engagement analysis

### Customer Support
- **Multi-tier Support**: Triage, specialized support, and escalation handling
- **Help Desk**: Automated ticket routing and resolution
- **Customer Success**: Proactive customer engagement and support

## 📊 Performance Monitoring

### Key Metrics Tracked
- **Response Time**: Average time for task completion
- **Success Rate**: Percentage of successfully completed tasks
- **Agent Utilization**: Workload distribution across agents
- **Routing Accuracy**: Effectiveness of routing decisions
- **Team Coordination**: Cross-team collaboration efficiency

### Dashboard Features
- Real-time charts and visualizations
- Agent performance comparison
- Team analytics with workload distribution
- Alert system with configurable thresholds
- Historical trend analysis
- Detailed performance reports

## 🧪 Testing

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

## 🏗️ Architecture

```
src/
├── core/
│   ├── configurable_agent.py    # Main agent class
│   ├── config_loader.py         # Configuration management
│   └── hierarchical_config_loader.py  # Hierarchical config management
├── hierarchical/
│   ├── hierarchical_agent.py    # Hierarchical team management
│   ├── enhanced_routing.py      # Advanced routing algorithms
│   ├── enhanced_supervisor.py   # Supervisor agent implementation
│   ├── supervisor.py            # Basic supervisor functionality
│   ├── team_coordinator.py      # Team coordination logic
│   └── worker_agent.py          # Worker agent implementation
├── memory/
│   └── memory_manager.py        # LangMem integration
├── optimization/
│   ├── prompt_optimizer.py      # Prompt optimization
│   └── feedback_collector.py    # Feedback collection
├── tools/
│   └── tool_registry.py         # Tool management
└── monitoring/
    └── performance_dashboard.py # Performance monitoring
```

## 🚨 Troubleshooting

### Common Issues

#### Configuration Validation Errors
```bash
# Check YAML syntax
python -c "import yaml; yaml.safe_load(open('your_config.yml'))"

# Validate with schema
python -c "
from src.core.config_loader import ConfigLoader
loader = ConfigLoader()
config = loader.load_config('your_config.yml')
print('Configuration is valid!')
"
```

#### API Key Issues
```bash
# Check environment variables
echo $OPENAI_API_KEY
echo $ANTHROPIC_API_KEY

# Verify in Python
python -c "import os; print('OPENAI_API_KEY:', bool(os.getenv('OPENAI_API_KEY')))"
```

#### Import Errors
```bash
# Install missing dependencies
pip install -r requirements.txt

# Check specific imports
python -c "from src.hierarchical.hierarchical_agent import HierarchicalAgentTeam"
```

### Performance Issues

#### Slow Routing Decisions
- Reduce `confidence_threshold` for faster decisions
- Use `keyword_based` routing for simple tasks
- Optimize LLM temperature settings

#### High Memory Usage
- Reduce `max_memory_size` in memory configuration
- Disable unused memory types
- Implement memory cleanup policies

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

We welcome contributions to both the basic agent system and hierarchical agent teams! Please feel free to:

- Submit bug reports and feature requests
- Contribute new agent templates
- Improve routing algorithms
- Enhance the web UI
- Add new monitoring capabilities

## 📄 License

MIT License - see LICENSE file for details.

## 📞 Support

For issues and questions:
- Check the [examples](examples/) directory
- Review the [test files](tests/) for usage patterns
- Create an issue on GitHub
- Check the inline code documentation

## 🔮 Roadmap

### Completed ✅
- [x] Web UI for agent configuration
- [x] Multi-agent coordination (Hierarchical Agent Teams)
- [x] Advanced routing algorithms
- [x] Performance monitoring dashboard
- [x] Memory management integration

### Planned 🚧
- [ ] Additional LLM provider support (Ollama, Cohere)
- [ ] Advanced memory backends (vector databases)
- [ ] Visual drag-and-drop team builder
- [ ] Auto-scaling and load balancing
- [ ] Integration hub and template marketplace
- [ ] Advanced analytics and ML-powered insights
- [ ] Plugin system for custom components

---

**Built with ❤️ for the AI agent community**

Transform your single-agent workflows into powerful hierarchical teams with intelligent coordination, advanced routing, and comprehensive monitoring. Start building your configurable and hierarchical agent systems today!