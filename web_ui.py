"""
Streamlit Web UI for Configurable LangGraph Agents
"""
import streamlit as st
import yaml
import os
import tempfile
import json
from pathlib import Path
from typing import Dict, Any, List
import asyncio
from datetime import datetime
import sys

# Import project modules
from src.core.configurable_agent import ConfigurableAgent
from src.core.config_loader import ConfigLoader, AgentConfiguration
from src.tools.tool_registry import ToolRegistry

# Page configuration
st.set_page_config(
    page_title="Configurable LangGraph Agents",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to optimize sidebar width (20% of screen) and ensure content is visible
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        width: 20% !important;
        min-width: 280px !important;
    }
    [data-testid="stSidebar"] > div:first-child {
        width: 20% !important;
        min-width: 280px !important;
    }
    [data-testid="stSidebar"] > div:first-child > div:first-child {
        width: 20% !important;
        min-width: 280px !important;
    }
    .main .block-container {
        margin-left: 22% !important;
        max-width: 78% !important;
    }
    /* Ensure sidebar content is visible and ultra-compact */
    [data-testid="stSidebar"] .stButton > button {
        width: 100% !important;
        margin: 1px 0 !important;
        padding: 0.2rem 0.5rem !important;
        font-size: 0.8rem !important;
    }
    [data-testid="stSidebar"] .stMarkdown {
        margin: 2px 0 !important;
    }
    [data-testid="stSidebar"] .stSubheader {
        margin-top: 12px !important;
        margin-bottom: 6px !important;
        font-size: 1rem !important;
    }
    [data-testid="stSidebar"] .stSelectbox > div > div {
        font-size: 0.8rem !important;
    }
    [data-testid="stSidebar"] .stExpander {
        margin: 2px 0 !important;
    }
    [data-testid="stSidebar"] .stCaption {
        font-size: 0.75rem !important;
    }
    [data-testid="stSidebar"] .stInfo {
        padding: 0.5rem !important;
        font-size: 0.8rem !important;
    }
    
    /* Fix text area text color - ensure text is black and readable */
    .stTextArea textarea {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    /* Fix text input text color */
    .stTextInput input {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    /* Fix selectbox text color */
    .stSelectbox select {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    /* Fix number input text color */
    .stNumberInput input {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    /* Ensure all form elements have readable text */
    .stTextArea, .stTextInput, .stSelectbox, .stNumberInput {
        color: #000000 !important;
    }
    
    /* Fix any white text on white background issues */
    .stTextArea > div > div > textarea,
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stNumberInput > div > div > input {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    /* Additional comprehensive text color fixes for all form elements */
    .stTextArea textarea,
    .stTextInput input,
    .stSelectbox select,
    .stNumberInput input,
    .stMultiselect select,
    .stSlider input {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    /* Target form elements specifically */
    .stForm .stTextArea textarea,
    .stForm .stTextInput input,
    .stForm .stSelectbox select,
    .stForm .stNumberInput input,
    .stForm .stMultiselect select {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    /* Target all input elements with more specific selectors */
    input[type="text"],
    input[type="number"],
    textarea,
    select {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    /* Force text color for all Streamlit form widgets */
    [data-testid="stTextInput"] input,
    [data-testid="stTextArea"] textarea,
    [data-testid="stSelectbox"] select,
    [data-testid="stNumberInput"] input,
    [data-testid="stMultiselect"] select {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    /* Additional targeting for nested elements */
    .stTextArea > div > div > div > textarea,
    .stTextInput > div > div > div > input,
    .stSelectbox > div > div > div > select,
    .stNumberInput > div > div > div > input {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    /* Fix ONLY form inputs that are white on white */
    .stTextArea textarea,
    .stTextInput input,
    .stSelectbox select,
    .stNumberInput input,
    .stMultiselect select {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    /* Don't affect any other text elements */
    .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6,
    .stMarkdown strong, .stMarkdown em, .stMarkdown small, .stMarkdown span, .stMarkdown div {
        /* Let these keep their natural colors */
    }
</style>

<script>
function fixTextColors() {
    // Fix all textarea elements
    document.querySelectorAll('textarea').forEach(function(el) {
        el.style.color = '#000000';
        el.style.backgroundColor = '#ffffff';
    });
    
    // Fix all input elements
    document.querySelectorAll('input[type="text"], input[type="number"]').forEach(function(el) {
        el.style.color = '#000000';
        el.style.backgroundColor = '#ffffff';
    });
    
    // Fix all select elements
    document.querySelectorAll('select').forEach(function(el) {
        el.style.color = '#000000';
        el.style.backgroundColor = '#ffffff';
    });
    
    // Fix only form inputs that are white on white
    document.querySelectorAll('.stTextArea textarea, .stTextInput input, .stSelectbox select, .stNumberInput input, .stMultiselect select').forEach(function(el) {
        el.style.color = '#000000';
        el.style.backgroundColor = '#ffffff';
    });
}

// Run on page load
document.addEventListener('DOMContentLoaded', fixTextColors);

// Run periodically to catch dynamically added elements
setInterval(fixTextColors, 1000);
</script>
""", unsafe_allow_html=True)

# Initialize session state
if 'config_data' not in st.session_state:
    st.session_state.config_data = {}
if 'current_config_file' not in st.session_state:
    st.session_state.current_config_file = None
if 'agent_instance' not in st.session_state:
    st.session_state.agent_instance = None

def get_available_models():
    """Get available models for each provider."""
    return {
        "openai": [
            "gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo",
            "gpt-3.5-turbo-16k"
        ],
        "anthropic": [
            "claude-3.5-sonnet-20241022", "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307", "claude-3-opus-20240229"
        ],
        "gemini": [
            "gemini-2.5-flash-preview-05-20", "gemini-1.5-pro", "gemini-1.5-flash",
            "gemini-pro", "gemini-pro-vision"
        ],
        "groq": [
            "meta-llama/llama-4-scout-17b-16e-instruct", "llama3-groq-70b-8192-tool-use-preview",
            "llama3-groq-8b-8192-tool-use-preview", "mixtral-8x7b-32768"
        ]
    }

def get_built_in_tools():
    """Get list of available built-in tools."""
    tool_registry = ToolRegistry()
    return tool_registry.get_built_in_tools()

def validate_config(config_data: Dict[str, Any]) -> tuple[bool, str]:
    """Validate configuration data."""
    try:
        config_loader = ConfigLoader()
        if config_loader.validate_config(config_data):
            return True, "Configuration is valid!"
        else:
            return False, "Invalid configuration format"
    except Exception as e:
        return False, f"Validation error: {str(e)}"

def save_config_to_file(config_data: Dict[str, Any], file_path: str) -> bool:
    """Save configuration to YAML file."""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(config_data, f, default_flow_style=False, sort_keys=False, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving configuration: {str(e)}")
        return False

def load_config_from_file(file_path: str) -> Dict[str, Any]:
    """Load configuration from YAML file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        st.error(f"Error loading configuration: {str(e)}")
        return {}

def render_agent_info_form():
    """Render agent information form."""
    st.subheader("Agent Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Agent Name", 
                           value=st.session_state.config_data.get('agent', {}).get('name', ''),
                           help="A descriptive name for your agent")
        
        version = st.text_input("Version", 
                              value=st.session_state.config_data.get('agent', {}).get('version', '1.0.0'),
                              help="Version number for your agent")
    
    with col2:
        description = st.text_area("Description", 
                                 value=st.session_state.config_data.get('agent', {}).get('description', ''),
                                 help="Detailed description of what your agent does",
                                 height=100)
    
    # Update session state
    if 'agent' not in st.session_state.config_data:
        st.session_state.config_data['agent'] = {}
    
    st.session_state.config_data['agent']['name'] = name
    st.session_state.config_data['agent']['description'] = description
    st.session_state.config_data['agent']['version'] = version

def render_llm_config_form():
    """Render LLM configuration form."""
    st.subheader("LLM Configuration")
    
    models = get_available_models()
    
    col1, col2 = st.columns(2)
    
    with col1:
        provider = st.selectbox("LLM Provider", 
                              options=list(models.keys()),
                              index=list(models.keys()).index(st.session_state.config_data.get('llm', {}).get('provider', 'openai')) if st.session_state.config_data.get('llm', {}).get('provider') in models else 0,
                              help="Choose your LLM provider")
        
        model = st.selectbox("Model", 
                           options=models[provider],
                           index=models[provider].index(st.session_state.config_data.get('llm', {}).get('model', models[provider][0])) if st.session_state.config_data.get('llm', {}).get('model') in models[provider] else 0,
                           help="Select the specific model to use")
        
        api_key_env = st.text_input("API Key Environment Variable", 
                                  value=st.session_state.config_data.get('llm', {}).get('api_key_env', f"{provider.upper()}_API_KEY"),
                                  help="Name of environment variable containing your API key")
    
    with col2:
        temperature = st.slider("Temperature", 
                              min_value=0.0, max_value=2.0, 
                              value=st.session_state.config_data.get('llm', {}).get('temperature', 0.7),
                              step=0.1,
                              help="Controls randomness in responses")
        
        max_tokens = st.number_input("Max Tokens", 
                                   min_value=1, max_value=128000,
                                   value=st.session_state.config_data.get('llm', {}).get('max_tokens', 4000),
                                   help="Maximum number of tokens in response")
        
        base_url = st.text_input("Base URL (Optional)", 
                               value=st.session_state.config_data.get('llm', {}).get('base_url', ''),
                               help="Custom base URL for API endpoint")
    
    # Update session state
    if 'llm' not in st.session_state.config_data:
        st.session_state.config_data['llm'] = {}
    
    st.session_state.config_data['llm']['provider'] = provider
    st.session_state.config_data['llm']['model'] = model
    st.session_state.config_data['llm']['temperature'] = temperature
    st.session_state.config_data['llm']['max_tokens'] = max_tokens
    st.session_state.config_data['llm']['api_key_env'] = api_key_env
    if base_url:
        st.session_state.config_data['llm']['base_url'] = base_url

def render_prompts_config_form():
    """Render prompts configuration form."""
    st.subheader("Prompts Configuration")
    
    # System Prompt
    st.write("**System Prompt**")
    system_template = st.text_area("System Prompt Template", 
                                 value=st.session_state.config_data.get('prompts', {}).get('system_prompt', {}).get('template', ''),
                                 height=150,
                                 help="The system prompt that defines the agent's role and behavior")
    
    system_variables = st.text_input("System Prompt Variables (comma-separated)", 
                                   value=', '.join(st.session_state.config_data.get('prompts', {}).get('system_prompt', {}).get('variables', [])),
                                   help="Variables that can be substituted in the system prompt")
    
    # User Prompt
    st.write("**User Prompt**")
    user_template = st.text_area("User Prompt Template", 
                                value=st.session_state.config_data.get('prompts', {}).get('user_prompt', {}).get('template', ''),
                                height=100,
                                help="Template for formatting user inputs")
    
    user_variables = st.text_input("User Prompt Variables (comma-separated)", 
                                 value=', '.join(st.session_state.config_data.get('prompts', {}).get('user_prompt', {}).get('variables', [])),
                                 help="Variables that can be substituted in the user prompt")
    
    # Tool Prompt (Optional)
    st.write("**Tool Prompt (Optional)**")
    tool_template = st.text_area("Tool Prompt Template", 
                                value=st.session_state.config_data.get('prompts', {}).get('tool_prompt', {}).get('template', ''),
                                height=100,
                                help="Template for tool usage instructions")
    
    tool_variables = st.text_input("Tool Prompt Variables (comma-separated)", 
                                 value=', '.join(st.session_state.config_data.get('prompts', {}).get('tool_prompt', {}).get('variables', [])) if st.session_state.config_data.get('prompts', {}).get('tool_prompt') else '',
                                 help="Variables that can be substituted in the tool prompt")
    
    # Update session state
    if 'prompts' not in st.session_state.config_data:
        st.session_state.config_data['prompts'] = {}
    
    st.session_state.config_data['prompts']['system_prompt'] = {
        'template': system_template,
        'variables': [v.strip() for v in system_variables.split(',') if v.strip()]
    }
    
    st.session_state.config_data['prompts']['user_prompt'] = {
        'template': user_template,
        'variables': [v.strip() for v in user_variables.split(',') if v.strip()]
    }
    
    if tool_template:
        st.session_state.config_data['prompts']['tool_prompt'] = {
            'template': tool_template,
            'variables': [v.strip() for v in tool_variables.split(',') if v.strip()]
        }

def render_tools_config_form():
    """Render tools configuration form."""
    st.subheader("Tools Configuration")
    
    # Built-in Tools
    st.write("**Built-in Tools**")
    available_tools = get_built_in_tools()
    current_built_in = st.session_state.config_data.get('tools', {}).get('built_in', [])
    
    selected_tools = st.multiselect("Select Built-in Tools", 
                                  options=available_tools,
                                  default=[tool for tool in current_built_in if tool in available_tools],
                                  help="Choose from available built-in tools")
    
    # Custom Tools
    st.write("**Custom Tools**")
    
    # Initialize custom tools in session state
    if 'tools' not in st.session_state.config_data:
        st.session_state.config_data['tools'] = {}
    if 'custom' not in st.session_state.config_data['tools']:
        st.session_state.config_data['tools']['custom'] = []
    
    custom_tools = st.session_state.config_data['tools']['custom']
    
    # Add new custom tool
    with st.expander("Add Custom Tool"):
        new_tool_name = st.text_input("Tool Name", key="new_tool_name")
        new_tool_module = st.text_input("Module Path", key="new_tool_module")
        new_tool_class = st.text_input("Class Name", key="new_tool_class")
        new_tool_description = st.text_area("Description", key="new_tool_description")
        new_tool_params = st.text_area("Parameters (JSON format)", 
                                     value="{}",
                                     key="new_tool_params",
                                     help="JSON object with tool parameters")
        
        if st.button("Add Custom Tool"):
            try:
                params = json.loads(new_tool_params) if new_tool_params.strip() else {}
                new_tool = {
                    'name': new_tool_name,
                    'module_path': new_tool_module,
                    'class_name': new_tool_class,
                    'description': new_tool_description,
                    'parameters': params
                }
                custom_tools.append(new_tool)
                st.success(f"Added custom tool: {new_tool_name}")
                st.rerun()
            except json.JSONDecodeError:
                st.error("Invalid JSON format in parameters")
    
    # Display existing custom tools
    if custom_tools:
        st.write("**Existing Custom Tools**")
        for i, tool in enumerate(custom_tools):
            with st.expander(f"Custom Tool: {tool['name']}"):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"**Module:** {tool['module_path']}")
                    st.write(f"**Class:** {tool['class_name']}")
                    st.write(f"**Description:** {tool['description']}")
                    if tool.get('parameters'):
                        st.write(f"**Parameters:** {json.dumps(tool['parameters'], indent=2)}")
                with col2:
                    if st.button("Remove", key=f"remove_tool_{i}"):
                        custom_tools.pop(i)
                        st.rerun()
    
    # Update session state
    st.session_state.config_data['tools']['built_in'] = selected_tools
    st.session_state.config_data['tools']['custom'] = custom_tools

def render_memory_config_form():
    """Render memory configuration form."""
    st.subheader("Memory Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        memory_enabled = st.checkbox("Enable Memory", 
                                   value=st.session_state.config_data.get('memory', {}).get('enabled', False),
                                   help="Enable memory functionality for the agent")
        
        if memory_enabled:
            provider = st.selectbox("Memory Provider", 
                                  options=["langmem", "custom"],
                                  index=0 if st.session_state.config_data.get('memory', {}).get('provider', 'langmem') == 'langmem' else 1,
                                  help="Choose memory provider")
            
            st.write("**Memory Types**")
            semantic = st.checkbox("Semantic Memory", 
                                 value=st.session_state.config_data.get('memory', {}).get('types', {}).get('semantic', True),
                                 help="Store facts and knowledge")
            
            episodic = st.checkbox("Episodic Memory", 
                                 value=st.session_state.config_data.get('memory', {}).get('types', {}).get('episodic', True),
                                 help="Store conversation history")
            
            procedural = st.checkbox("Procedural Memory", 
                                   value=st.session_state.config_data.get('memory', {}).get('types', {}).get('procedural', True),
                                   help="Store learned patterns")
    
    with col2:
        if memory_enabled:
            st.write("**Storage Configuration**")
            backend = st.selectbox("Storage Backend", 
                                 options=["memory", "postgres", "redis"],
                                 index=["memory", "postgres", "redis"].index(st.session_state.config_data.get('memory', {}).get('storage', {}).get('backend', 'memory')),
                                 help="Choose storage backend")
            
            connection_string = st.text_input("Connection String (Optional)", 
                                            value=st.session_state.config_data.get('memory', {}).get('storage', {}).get('connection_string', ''),
                                            help="Database connection string if using external storage")
            
            st.write("**Memory Settings**")
            max_memory_size = st.number_input("Max Memory Size", 
                                            min_value=1000, max_value=100000,
                                            value=st.session_state.config_data.get('memory', {}).get('settings', {}).get('max_memory_size', 10000),
                                            help="Maximum number of memory items")
            
            retention_days = st.number_input("Retention Days", 
                                           min_value=1, max_value=365,
                                           value=st.session_state.config_data.get('memory', {}).get('settings', {}).get('retention_days', 30),
                                           help="How long to keep memories")
            
            background_processing = st.checkbox("Background Processing", 
                                              value=st.session_state.config_data.get('memory', {}).get('settings', {}).get('background_processing', True),
                                              help="Enable background memory processing")
    
    # Update session state
    if 'memory' not in st.session_state.config_data:
        st.session_state.config_data['memory'] = {}
    
    st.session_state.config_data['memory']['enabled'] = memory_enabled
    
    if memory_enabled:
        st.session_state.config_data['memory']['provider'] = provider
        st.session_state.config_data['memory']['types'] = {
            'semantic': semantic,
            'episodic': episodic,
            'procedural': procedural
        }
        st.session_state.config_data['memory']['storage'] = {
            'backend': backend
        }
        if connection_string:
            st.session_state.config_data['memory']['storage']['connection_string'] = connection_string
        
        st.session_state.config_data['memory']['settings'] = {
            'max_memory_size': max_memory_size,
            'retention_days': retention_days,
            'background_processing': background_processing
        }

def render_react_config_form():
    """Render ReAct configuration form."""
    st.subheader("ReAct Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        max_iterations = st.number_input("Max Iterations", 
                                       min_value=1, max_value=100,
                                       value=st.session_state.config_data.get('react', {}).get('max_iterations', 10),
                                       help="Maximum reasoning/acting cycles")
    
    with col2:
        recursion_limit = st.number_input("Recursion Limit", 
                                        min_value=10, max_value=200,
                                        value=st.session_state.config_data.get('react', {}).get('recursion_limit', 50),
                                        help="Maximum recursion depth")
    
    # Update session state
    if 'react' not in st.session_state.config_data:
        st.session_state.config_data['react'] = {}
    
    st.session_state.config_data['react']['max_iterations'] = max_iterations
    st.session_state.config_data['react']['recursion_limit'] = recursion_limit

def render_optimization_config_form():
    """Render optimization configuration form."""
    st.subheader("Optimization Configuration")
    
    optimization_enabled = st.checkbox("Enable Optimization", 
                                     value=st.session_state.config_data.get('optimization', {}).get('enabled', False),
                                     help="Enable optimization features")
    
    if optimization_enabled:
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Prompt Optimization**")
            prompt_opt_enabled = st.checkbox("Enable Prompt Optimization", 
                                           value=st.session_state.config_data.get('optimization', {}).get('prompt_optimization', {}).get('enabled', False))
            
            feedback_collection = st.checkbox("Feedback Collection", 
                                            value=st.session_state.config_data.get('optimization', {}).get('prompt_optimization', {}).get('feedback_collection', False))
            
            ab_testing = st.checkbox("A/B Testing", 
                                   value=st.session_state.config_data.get('optimization', {}).get('prompt_optimization', {}).get('ab_testing', False))
            
            optimization_frequency = st.selectbox("Optimization Frequency", 
                                                options=["daily", "weekly", "monthly"],
                                                index=["daily", "weekly", "monthly"].index(st.session_state.config_data.get('optimization', {}).get('prompt_optimization', {}).get('optimization_frequency', 'weekly')))
        
        with col2:
            st.write("**Performance Tracking**")
            perf_tracking_enabled = st.checkbox("Enable Performance Tracking", 
                                              value=st.session_state.config_data.get('optimization', {}).get('performance_tracking', {}).get('enabled', False))
            
            if perf_tracking_enabled:
                available_metrics = ["response_time", "accuracy", "user_satisfaction", "source_quality", "resolution_rate", "customer_satisfaction", "escalation_rate", "code_quality", "execution_success"]
                current_metrics = st.session_state.config_data.get('optimization', {}).get('performance_tracking', {}).get('metrics', ["response_time", "accuracy", "user_satisfaction"])
                
                selected_metrics = st.multiselect("Performance Metrics", 
                                                options=available_metrics,
                                                default=[metric for metric in current_metrics if metric in available_metrics])
    
    # Update session state
    if 'optimization' not in st.session_state.config_data:
        st.session_state.config_data['optimization'] = {}
    
    st.session_state.config_data['optimization']['enabled'] = optimization_enabled
    
    if optimization_enabled:
        st.session_state.config_data['optimization']['prompt_optimization'] = {
            'enabled': prompt_opt_enabled,
            'feedback_collection': feedback_collection,
            'ab_testing': ab_testing,
            'optimization_frequency': optimization_frequency
        }
        
        st.session_state.config_data['optimization']['performance_tracking'] = {
            'enabled': perf_tracking_enabled
        }
        
        if perf_tracking_enabled:
            st.session_state.config_data['optimization']['performance_tracking']['metrics'] = selected_metrics

def render_runtime_config_form():
    """Render runtime configuration form."""
    st.subheader("Runtime Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        max_iterations = st.number_input("Max Iterations", 
                                       min_value=1, max_value=200,
                                       value=st.session_state.config_data.get('runtime', {}).get('max_iterations', 50),
                                       help="Maximum iterations for agent execution")
        
        timeout_seconds = st.number_input("Timeout (seconds)", 
                                        min_value=10, max_value=3600,
                                        value=st.session_state.config_data.get('runtime', {}).get('timeout_seconds', 300),
                                        help="Maximum execution time in seconds")
    
    with col2:
        retry_attempts = st.number_input("Retry Attempts", 
                                       min_value=0, max_value=10,
                                       value=st.session_state.config_data.get('runtime', {}).get('retry_attempts', 3),
                                       help="Number of retry attempts on failure")
        
        debug_mode = st.checkbox("Debug Mode", 
                               value=st.session_state.config_data.get('runtime', {}).get('debug_mode', False),
                               help="Enable debug mode for detailed logging")
    
    # Update session state
    if 'runtime' not in st.session_state.config_data:
        st.session_state.config_data['runtime'] = {}
    
    st.session_state.config_data['runtime']['max_iterations'] = max_iterations
    st.session_state.config_data['runtime']['timeout_seconds'] = timeout_seconds
    st.session_state.config_data['runtime']['retry_attempts'] = retry_attempts
    st.session_state.config_data['runtime']['debug_mode'] = debug_mode

def render_yaml_preview():
    """Render YAML preview and validation."""
    st.subheader("Configuration Preview")
    
    # Generate YAML
    try:
        yaml_content = yaml.dump(st.session_state.config_data, default_flow_style=False, sort_keys=False, indent=2)
        
        # Validate configuration
        is_valid, validation_message = validate_config(st.session_state.config_data)
        
        if is_valid:
            st.success(validation_message)
        else:
            st.error(validation_message)
        
        # Display YAML
        st.code(yaml_content, language='yaml')
        
        # Download button
        st.download_button(
            label="Download Configuration",
            data=yaml_content,
            file_name=f"agent_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.yml",
            mime="text/yaml"
        )
        
        return yaml_content
        
    except Exception as e:
        st.error(f"Error generating YAML: {str(e)}")
        return None

def render_file_operations():
    """Render file load/save operations."""
    st.subheader("File Operations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Load Configuration**")
        
        st.info("💡 Agent templates are available in the sidebar under 'Quick Templates'")
        
        # Upload custom config
        
        # Upload custom config
        uploaded_file = st.file_uploader("Upload Configuration File", type=['yml', 'yaml'])
        if uploaded_file is not None:
            try:
                config_data = yaml.safe_load(uploaded_file.read())
                st.session_state.config_data = config_data
                st.session_state.current_config_file = uploaded_file.name
                st.success(f"Loaded configuration from {uploaded_file.name}")
                st.rerun()
            except Exception as e:
                st.error(f"Error loading file: {str(e)}")
    
    with col2:
        st.write("**Save Configuration**")
        
        save_filename = st.text_input("Save as filename", 
                                    value=f"my_agent_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.yml")
        
        if st.button("Save Configuration"):
            if st.session_state.config_data:
                # Create configs directory if it doesn't exist
                save_dir = Path("configs/custom")
                save_dir.mkdir(parents=True, exist_ok=True)
                
                save_path = save_dir / save_filename
                if save_config_to_file(st.session_state.config_data, str(save_path)):
                    st.success(f"Configuration saved to {save_path}")
                    st.session_state.current_config_file = str(save_path)
            else:
                st.warning("No configuration to save")

def render_agent_testing():
    """Render agent testing interface."""
    st.subheader("Test Agent")
    
    if not st.session_state.config_data:
        st.warning("Please configure your agent first")
        return
    
    # Validate configuration
    is_valid, validation_message = validate_config(st.session_state.config_data)
    if not is_valid:
        st.error(f"Cannot test agent: {validation_message}")
        return
    
    # Save temporary config file for testing
    temp_config_file = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            yaml.dump(st.session_state.config_data, f, default_flow_style=False)
            temp_config_file = f.name
        
        # Initialize agent
        if st.button("Initialize Agent"):
            try:
                st.session_state.agent_instance = ConfigurableAgent(temp_config_file)
                st.success("Agent initialized successfully!")
            except Exception as e:
                st.error(f"Error initializing agent: {str(e)}")
                st.session_state.agent_instance = None
        
        # Test interface
        if st.session_state.agent_instance:
            st.write("**Agent Ready for Testing**")
            
            test_input = st.text_area("Enter your test message:", 
                                    height=100,
                                    placeholder="Ask your agent a question or give it a task...")
            
            col1, col2 = st.columns([1, 4])
            
            with col1:
                if st.button("Send Message", type="primary"):
                    if test_input:
                        with st.spinner("Agent is thinking..."):
                            try:
                                response = st.session_state.agent_instance.run(test_input)
                                
                                st.write("**Agent Response:**")
                                st.write(response.get('response', 'No response'))
                                
                                # Show additional details in expander
                                with st.expander("Response Details"):
                                    st.json(response)
                                
                            except Exception as e:
                                st.error(f"Error running agent: {str(e)}")
                    else:
                        st.warning("Please enter a message")
            
            with col2:
                if st.button("Clear Agent"):
                    st.session_state.agent_instance = None
                    st.rerun()
    
    finally:
        # Clean up temporary file
        if temp_config_file and os.path.exists(temp_config_file):
            os.unlink(temp_config_file)

def render_hierarchical_agent_management():
    """Render hierarchical agent management interface."""
    st.subheader("🏢 Hierarchical Agent Management")
    
    st.write("Create and manage hierarchical agent teams with multiple specialized workers.")
    
    # Initialize hierarchical team in session state
    if 'hierarchical_team' not in st.session_state:
        st.session_state.hierarchical_team = None
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Create Hierarchical Team**")
        
        team_name = st.text_input("Team Name", 
                                 value="research_team",
                                 help="Name for your hierarchical team")
        
        if st.button("Create Hierarchical Team", type="primary"):
            try:
                from src.hierarchical import HierarchicalAgentTeam
                st.session_state.hierarchical_team = HierarchicalAgentTeam(name=team_name)
                st.success(f"Created hierarchical team: {team_name}")
            except ImportError as e:
                st.error(f"Hierarchical modules not available: {str(e)}")
                st.info("Install dependencies: pip install -r requirements.txt")
            except Exception as e:
                st.error(f"Error creating hierarchical team: {str(e)}")
    
    with col2:
        st.write("**Add Workers**")
        
        if st.session_state.hierarchical_team:
            # Available worker configs
            worker_configs = {
                "Web Researcher": "configs/examples/research_agent.yml",
                "Coding Assistant": "configs/examples/coding_assistant.yml",
                "Customer Support": "configs/examples/customer_support.yml",
                "Gemini Analyst": "configs/examples/gemini_agent.yml",
                "Groq Coder": "configs/examples/groq_agent.yml"
            }
            
            selected_worker = st.selectbox("Select Worker Type", 
                                         options=list(worker_configs.keys()))
            
            worker_name = st.text_input("Worker Name", 
                                      value=selected_worker.lower().replace(" ", "_"),
                                      help="Name for this worker agent")
            
            team_name = st.selectbox("Team Name", 
                                   options=["research", "development", "support", "analysis"],
                                   help="Which team to add the worker to")
            
            if st.button("Add Worker"):
                try:
                    worker = st.session_state.hierarchical_team.create_worker_from_config(
                        name=worker_name,
                        config_file=worker_configs[selected_worker],
                        team_name=team_name
                    )
                    st.success(f"Added {worker_name} to {team_name} team")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error adding worker: {str(e)}")
        else:
            st.info("Create a hierarchical team first")
    
    # Display team information
    if st.session_state.hierarchical_team:
        st.write("**Team Information**")
        
        hierarchy_info = st.session_state.hierarchical_team.get_hierarchy_info()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Teams", hierarchy_info['total_teams'])
        
        with col2:
            st.metric("Total Workers", hierarchy_info['total_workers'])
        
        with col3:
            st.metric("Coordinator", hierarchy_info['coordinator']['name'])
        
        # Display team structure
        st.write("**Team Structure**")
        for team_name, team_info in hierarchy_info['teams'].items():
            with st.expander(f"📋 {team_name} Team"):
                st.write(f"**Supervisor:** {team_info['supervisor']}")
                st.write(f"**Workers:** {team_info['worker_count']}")
                st.write(f"**Worker Names:** {', '.join(team_info['workers'])}")
        
        # Test hierarchical team
        st.write("**Test Hierarchical Team**")
        
        test_input = st.text_area("Enter your test message:", 
                                 height=100,
                                 placeholder="Ask your hierarchical team a question...")
        
        if st.button("Test Hierarchical Team"):
            if test_input:
                with st.spinner("Hierarchical team is working..."):
                    try:
                        result = st.session_state.hierarchical_team.run(test_input)
                        
                        st.write("**Team Response:**")
                        st.write(result.get('response', 'No response'))
                        
                        # Show routing information
                        with st.expander("Routing Information"):
                            st.write(f"**Team Used:** {result.get('team_used', 'Unknown')}")
                            st.write(f"**Worker Used:** {result.get('worker_response', {}).get('worker_used', 'Unknown')}")
                            st.write(f"**Decision Reasoning:** {result.get('decision_reasoning', 'No reasoning provided')}")
                        
                        # Show full result
                        with st.expander("Full Result"):
                            st.json(result)
                        
                    except Exception as e:
                        st.error(f"Error running hierarchical team: {str(e)}")
            else:
                st.warning("Please enter a message to test")
    
    # Quick actions section - will be moved to main content area
    st.write("**Quick Actions**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Load Hierarchical Template", use_container_width=True):
            example_path = Path("configs/examples/hierarchical_research_team.yml")
            if example_path.exists():
                config_data = load_config_from_file(str(example_path))
                if config_data:
                    st.session_state.config_data = config_data
                    st.session_state.current_config_file = str(example_path)
                    st.rerun()
    
    with col2:
        if st.button("Run Hierarchical Example", use_container_width=True):
            try:
                import subprocess
                result = subprocess.run([
                    sys.executable, "examples/hierarchical_agent_example.py"
                ], capture_output=True, text=True, timeout=60)
                
                if result.returncode == 0:
                    st.success("Hierarchical example completed successfully!")
                    with st.expander("Example Output"):
                        st.code(result.stdout)
                else:
                    st.error(f"Example failed: {result.stderr}")
            except subprocess.TimeoutExpired:
                st.error("Example timed out. This might be due to missing dependencies.")
                st.info("To run the full example with API calls, install dependencies: pip install -r requirements.txt")
            except Exception as e:
                st.error(f"Error running example: {str(e)}")
    
def render_template_selector():
    """Render compact template selector in sidebar."""
    st.sidebar.subheader("🤖 Agent Templates")
    
    # Define all available templates
    templates = {
        "🔬 Research Agent": {
            "file": "research_agent.yml",
            "description": "Web research and information gathering"
        },
        "💻 Coding Assistant": {
            "file": "coding_assistant.yml", 
            "description": "Code generation and programming help"
        },
        "🎧 Customer Support": {
            "file": "customer_support.yml",
            "description": "Customer service and support agent"
        },
        "🤖 Gemini Agent": {
            "file": "gemini_agent.yml",
            "description": "Google Gemini-powered agent"
        },
        "⚡ Groq Agent": {
            "file": "groq_agent.yml", 
            "description": "High-speed Groq inference agent"
        },
        "🏢 Hierarchical Research Team": {
            "file": "hierarchical_research_team.yml",
            "description": "Multi-agent research team"
        },
        "🌐 Web Content Team": {
            "file": "web_content_team.yml",
            "description": "Hierarchical team with web browser and writer agents"
        },
        "🔍 Web Browser Agent": {
            "file": "web_browser_agent.yml",
            "description": "Specialized web search and information gathering"
        },
        "✍️ Writer Agent": {
            "file": "writer_agent.yml",
            "description": "Content creation and writing specialist"
        }
    }
    
    # Get available templates
    available_templates = []
    for template_name, template_info in templates.items():
        example_path = Path(f"configs/examples/{template_info['file']}")
        if example_path.exists():
            available_templates.append(template_name)
    
    if available_templates:
        # Template selection dropdown
        selected_template = st.sidebar.selectbox(
            "Choose a template:",
            options=["Select template..."] + available_templates,
            help="Select a pre-configured agent template to load"
        )
        
        # Show description for selected template
        if selected_template != "Select template..." and selected_template in templates:
            st.sidebar.caption(f"📝 {templates[selected_template]['description']}")
        
        # Load button
        col1, col2 = st.sidebar.columns([2, 1])
        with col1:
            load_disabled = selected_template == "Select template..."
            if st.button("Load Template", disabled=load_disabled, use_container_width=True):
                if selected_template in templates:
                    template_info = templates[selected_template]
                    example_path = Path(f"configs/examples/{template_info['file']}")
                    config_data = load_config_from_file(str(example_path))
                    if config_data:
                        st.session_state.config_data = config_data
                        st.session_state.current_config_file = str(example_path)
                        st.sidebar.success(f"✅ Loaded!")
                        st.rerun()
        
        with col2:
            st.sidebar.caption(f"{len(available_templates)} available")
    else:
        st.sidebar.warning("No templates found")


def main():
    """Main Streamlit application."""
    st.title("🤖 Configurable LangGraph Agents")
    st.write("Create and configure AI agents with a user-friendly web interface")
    
    # Sidebar navigation with compact title
    st.sidebar.title("🔧 Configuration")
    
    # Show current configuration status compactly
    if st.session_state.current_config_file:
        st.sidebar.success(f"📄 {Path(st.session_state.current_config_file).name}")
    else:
        st.sidebar.info("No configuration loaded")
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11 = st.tabs([
        "Agent Info", "LLM Config", "Prompts", "Tools", "Memory", 
        "ReAct", "Optimization", "Runtime", "Preview", "Test", "Hierarchical"
    ])
    
    with tab1:
        render_agent_info_form()
    
    with tab2:
        render_llm_config_form()
    
    with tab3:
        render_prompts_config_form()
    
    with tab4:
        render_tools_config_form()
    
    with tab5:
        render_memory_config_form()
    
    with tab6:
        render_react_config_form()
    
    with tab7:
        render_optimization_config_form()
    
    with tab8:
        render_runtime_config_form()
    
    with tab9:
        render_yaml_preview()
        st.divider()
        render_file_operations()
    
    with tab10:
        render_agent_testing()
    
    with tab11:
        render_hierarchical_agent_management()
    
    # Render compact template selector
    render_template_selector()
    
    # Sidebar tools with better organization
    st.sidebar.divider()
    
    # Agent Management - More compact layout
    st.sidebar.subheader("⚙️ Agent Management")
    
    # Two-column layout for actions
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if st.button("🗑️ Clear", help="Clear all configuration", use_container_width=True):
            st.session_state.config_data = {}
            st.session_state.current_config_file = None
            st.session_state.agent_instance = None
            st.rerun()
    
    with col2:
        if st.button("💾 Save", help="Save current configuration", use_container_width=True):
            if st.session_state.config_data:
                save_filename = f"my_agent_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.yml"
                save_dir = Path("configs/custom")
                save_dir.mkdir(parents=True, exist_ok=True)
                save_path = save_dir / save_filename
                if save_config_to_file(st.session_state.config_data, str(save_path)):
                    st.sidebar.success(f"✅ Saved!")
            else:
                st.sidebar.warning("No configuration to save")
    
    # Test agent - full width
    if st.sidebar.button("🧪 Test Agent", use_container_width=True):
        if st.session_state.config_data:
            st.sidebar.success("Agent ready! Go to the 'Test' tab.")
        else:
            st.sidebar.warning("No agent configured yet")
    
    # Debug section - collapsible with compact styling
    st.sidebar.divider()
    with st.sidebar.expander("🔧 Debug Info"):
        st.caption(f"Config: {Path(st.session_state.current_config_file).name if st.session_state.current_config_file else 'None'}")
        st.caption(f"Data: {'✅' if st.session_state.config_data else '❌'}")
        st.caption(f"Agent: {'✅' if st.session_state.agent_instance else '❌'}")

if __name__ == "__main__":
    main() 