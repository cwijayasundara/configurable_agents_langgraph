"""
Usage examples for the configurable agent system.
"""
import os
import sys
import asyncio
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Load environment variables from .env file
load_dotenv()

from src.core.configurable_agent import ConfigurableAgent
from src.optimization.prompt_optimizer import OptimizationMetric


def basic_usage_example():
    """Basic usage of a configurable agent."""
    print("=== Basic Usage Example ===")
    
    # Create agent from configuration
    agent = ConfigurableAgent("configs/examples/research_agent.yml")
    
    # Run a simple query
    response = agent.run("What are the latest developments in quantum computing?")
    
    print("Agent Response:")
    print(response["response"])
    print(f"Iterations: {response['iteration_count']}")
    print(f"Tools Used: {list(response['tool_results'].keys())}")


def memory_example():
    """Example showing memory functionality."""
    print("\\n=== Memory Example ===")
    
    agent = ConfigurableAgent("configs/examples/coding_assistant.yml")
    
    # First interaction
    response1 = agent.run("I'm working on a Python web scraper using requests")
    print("First interaction:")
    print(response1["response"][:200] + "...")
    
    # Second interaction - agent should remember context
    response2 = agent.run("How can I add error handling to handle timeouts?")
    print("\\nSecond interaction (with memory):")
    print(response2["response"][:200] + "...")
    
    # Check memory stats
    memory_stats = agent.get_memory_stats()
    print(f"\\nMemory stats: {memory_stats}")


def optimization_example():
    """Example showing prompt optimization."""
    print("\\n=== Optimization Example ===")
    
    agent = ConfigurableAgent("configs/examples/customer_support.yml")
    
    # Simulate multiple interactions with feedback
    test_queries = [
        "My order hasn't arrived yet",
        "I need to return a product",
        "How do I reset my password?",
        "I was charged twice for the same order"
    ]
    
    for i, query in enumerate(test_queries):
        response = agent.run(query, interaction_id=f"test_{i}")
        
        # Simulate user satisfaction feedback
        satisfaction_score = 0.8 if i % 2 == 0 else 0.6
        
        print(f"Query {i+1}: {query[:30]}...")
        print(f"Response length: {len(response['response'])} chars")
        print(f"Simulated satisfaction: {satisfaction_score}")
        print()


async def async_usage_example():
    """Example of async usage."""
    print("\\n=== Async Usage Example ===")
    
    agent = ConfigurableAgent("configs/examples/research_agent.yml")
    
    # Run multiple queries concurrently
    queries = [
        "What is machine learning?",
        "Explain blockchain technology",
        "What are the benefits of renewable energy?"
    ]
    
    tasks = [agent.arun(query) for query in queries]
    responses = await asyncio.gather(*tasks)
    
    for i, (query, response) in enumerate(zip(queries, responses)):
        print(f"Query {i+1}: {query}")
        print(f"Response: {response['response'][:100]}...")
        print()


def custom_tools_example():
    """Example showing how to add custom tools."""
    print("\\n=== Custom Tools Example ===")
    
    # Create a simple custom tool function
    def database_query(query: str) -> str:
        """Mock database query tool."""
        return f"Database result for: {query}"
    
    agent = ConfigurableAgent("configs/examples/coding_assistant.yml")
    
    # Register custom tool
    agent.tool_registry.register_function_as_tool(
        name="database_query",
        func=database_query,
        description="Query the database for information"
    )
    
    print("Available tools:")
    tools = agent.get_available_tools()
    for tool_name, description in tools.items():
        print(f"- {tool_name}: {description}")


def configuration_management_example():
    """Example showing configuration management."""
    print("\\n=== Configuration Management Example ===")
    
    agent = ConfigurableAgent("configs/examples/research_agent.yml")
    
    # Get current configuration
    config = agent.get_config()
    print(f"Agent: {config.agent.name}")
    print(f"LLM: {config.llm.provider} - {config.llm.model}")
    print(f"Memory enabled: {config.memory.enabled}")
    
    # Update prompts dynamically
    new_prompts = {
        "system_prompt": "You are a specialized scientific research assistant focused on peer-reviewed sources."
    }
    agent.update_prompts(new_prompts)
    print("\\nPrompts updated successfully")
    
    # Get formatted prompt
    formatted_prompt = agent.get_prompt_template(
        "user_prompt", 
        user_input="Latest cancer research findings"
    )
    print(f"\\nFormatted prompt sample: {formatted_prompt[:100]}...")


def error_handling_example():
    """Example showing error handling."""
    print("\\n=== Error Handling Example ===")
    
    try:
        # Try to create agent with non-existent config
        agent = ConfigurableAgent("configs/nonexistent.yml")
    except FileNotFoundError as e:
        print(f"Expected error: {e}")
    
    # Create agent with valid config
    agent = ConfigurableAgent("configs/examples/research_agent.yml")
    
    # Test with invalid input
    response = agent.run("")  # Empty input
    print(f"Empty input response: {response['response'][:100]}...")
    
    if "error" in response:
        print(f"Error handled: {response['error']}")


def gemini_example():
    """Example using Gemini LLM."""
    print("\\n=== Gemini Agent Example ===")
    
    try:
        agent = ConfigurableAgent("configs/examples/gemini_agent.yml")
        
        config = agent.get_config()
        print(f"Agent: {config.agent.name}")
        print(f"LLM: {config.llm.provider} - {config.llm.model}")
        
        response = agent.run("What are the latest developments in quantum computing?")
        print(f"Response: {response['response'][:200]}...")
        
    except Exception as e:
        print(f"Gemini example failed: {e}")


def groq_example():
    """Example using Groq LLM."""
    print("\\n=== Groq Agent Example ===")
    
    try:
        agent = ConfigurableAgent("configs/examples/groq_agent.yml")
        
        config = agent.get_config()
        print(f"Agent: {config.agent.name}")
        print(f"LLM: {config.llm.provider} - {config.llm.model}")
        
        response = agent.run("Write a Python function to calculate fibonacci numbers")
        print(f"Response: {response['response'][:200]}...")
        
    except Exception as e:
        print(f"Groq example failed: {e}")


def main():
    """Run all examples."""
    # Check for environment variables
    if not os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY") == "your-openai-api-key-here":
        print("Warning: OPENAI_API_KEY not set in .env file. Some examples may fail.")
        print("Please update your .env file with your actual OpenAI API key.")
    if not os.getenv("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_API_KEY") == "your-anthropic-api-key-here":
        print("Warning: ANTHROPIC_API_KEY not set in .env file. Some examples may fail.")
        print("Please update your .env file with your actual Anthropic API key.")
    if not os.getenv("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY") == "your-google-api-key-here":
        print("Warning: GOOGLE_API_KEY not set in .env file. Gemini examples may fail.")
        print("Please update your .env file with your actual Google API key.")
    if not os.getenv("GROQ_API_KEY") or os.getenv("GROQ_API_KEY") == "your-groq-api-key-here":
        print("Warning: GROQ_API_KEY not set in .env file. Groq examples may fail.")
        print("Please update your .env file with your actual Groq API key.")
    
    try:
        basic_usage_example()
        memory_example()
        optimization_example()
        custom_tools_example()
        configuration_management_example()
        error_handling_example()
        gemini_example()
        groq_example()
        
        # Run async example
        print("\\n=== Running Async Example ===")
        asyncio.run(async_usage_example())
        
    except Exception as e:
        print(f"Example failed (likely due to missing API keys): {e}")
        print("\\nTo run examples successfully:")
        print("1. Copy .env.example to .env: cp .env.example .env")
        print("2. Edit .env file and add your actual API keys")
        print("3. Install required dependencies: pip install -r requirements.txt")
        print("\\nSupported LLM providers:")
        print("- OpenAI (gpt-4o-mini, gpt-4o, gpt-3.5-turbo)")
        print("- Anthropic (Claude-3, Claude-2)")
        print("- Google Gemini (gemini-2.5-flash-preview-05-20, gemini-1.5-pro, gemini-1.0-pro)")
        print("- Groq (meta-llama/llama-4-scout-17b-16e-instruct, llama3-8b-8192, llama3-70b-8192)")


if __name__ == "__main__":
    main()