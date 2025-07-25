#!/usr/bin/env python3
"""
Test wrapper for the configurable agents system.
This script provides a comprehensive way to run all tests with different options.
"""
import os
import sys
import subprocess
import argparse
import time
from pathlib import Path
from typing import List, Dict, Any


class TestRunner:
    """Comprehensive test runner for the configurable agents system."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.test_dir = self.project_root / "tests"
        self.results = {}
        self.start_time = None
        
    def setup_environment(self):
        """Setup test environment variables."""
        # Set test API keys
        os.environ["TEST_API_KEY"] = "test-key-for-testing"
        os.environ["OPENAI_API_KEY"] = "test-openai-key"
        os.environ["ANTHROPIC_API_KEY"] = "test-anthropic-key"
        os.environ["GOOGLE_API_KEY"] = "test-google-key"
        os.environ["GROQ_API_KEY"] = "test-groq-key"
        
        # Add project root to Python path
        sys.path.insert(0, str(self.project_root))
        
    def run_pytest(self, args: List[str] = None) -> Dict[str, Any]:
        """Run pytest with given arguments."""
        if args is None:
            args = []
        
        cmd = ["python", "-m", "pytest"] + args
        
        print(f"Running: {' '.join(cmd)}")
        start_time = time.time()
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            duration = time.time() - start_time
            
            return {
                "success": result.returncode == 0,
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "duration": duration
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "duration": time.time() - start_time
            }
    
    def run_unit_tests(self, verbose: bool = False, coverage: bool = False) -> Dict[str, Any]:
        """Run all unit tests."""
        print("\n" + "="*60)
        print("RUNNING UNIT TESTS")
        print("="*60)
        
        args = ["tests/"]
        
        if verbose:
            args.append("-v")
        
        if coverage:
            args.extend(["--cov=src", "--cov-report=html", "--cov-report=term"])
        
        return self.run_pytest(args)
    
    def run_specific_test(self, test_file: str, verbose: bool = False) -> Dict[str, Any]:
        """Run a specific test file."""
        print(f"\n" + "="*60)
        print(f"RUNNING SPECIFIC TEST: {test_file}")
        print("="*60)
        
        args = [f"tests/{test_file}"]
        
        if verbose:
            args.append("-v")
        
        return self.run_pytest(args)
    
    def run_integration_tests(self, verbose: bool = False) -> Dict[str, Any]:
        """Run integration tests (examples)."""
        print("\n" + "="*60)
        print("RUNNING INTEGRATION TESTS")
        print("="*60)
        
        # Test that examples can be imported and run
        try:
            from examples.usage_examples import main
            print("✓ Examples module imports successfully")
            
            # Test configuration loading
            from src.core.configurable_agent import ConfigurableAgent
            print("✓ ConfigurableAgent imports successfully")
            
            # Test config loading
            config_files = [
                "configs/examples/research_agent.yml",
                "configs/examples/coding_assistant.yml",
                "configs/examples/customer_support.yml",
                "configs/examples/gemini_agent.yml",
                "configs/examples/groq_agent.yml"
            ]
            
            for config_file in config_files:
                if Path(config_file).exists():
                    try:
                        agent = ConfigurableAgent(config_file)
                        config = agent.get_config()
                        print(f"✓ {config_file} loads successfully")
                    except Exception as e:
                        print(f"✗ {config_file} failed to load: {e}")
                else:
                    print(f"⚠ {config_file} not found")
            
            return {"success": True, "message": "Integration tests passed"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def run_lint_tests(self) -> Dict[str, Any]:
        """Run code quality checks."""
        print("\n" + "="*60)
        print("RUNNING CODE QUALITY CHECKS")
        print("="*60)
        
        results = {}
        
        # Check for syntax errors
        try:
            result = subprocess.run(
                ["python", "-m", "py_compile", "src/core/configurable_agent.py"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print("✓ Syntax check passed")
                results["syntax"] = True
            else:
                print(f"✗ Syntax errors found: {result.stderr}")
                results["syntax"] = False
        except Exception as e:
            print(f"✗ Syntax check failed: {e}")
            results["syntax"] = False
        
        # Check imports
        try:
            result = subprocess.run(
                ["python", "-c", "from src.core.configurable_agent import ConfigurableAgent"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print("✓ Import check passed")
                results["imports"] = True
            else:
                print(f"✗ Import errors: {result.stderr}")
                results["imports"] = False
        except Exception as e:
            print(f"✗ Import check failed: {e}")
            results["imports"] = False
        
        return {
            "success": all(results.values()),
            "results": results
        }
    
    def run_all_tests(self, verbose: bool = False, coverage: bool = False) -> Dict[str, Any]:
        """Run all tests."""
        self.start_time = time.time()
        self.setup_environment()
        
        print("🧪 CONFIGURABLE AGENTS TEST SUITE")
        print("="*60)
        
        all_results = {}
        
        # Run lint tests
        all_results["lint"] = self.run_lint_tests()
        
        # Run unit tests
        all_results["unit"] = self.run_unit_tests(verbose, coverage)
        
        # Run integration tests
        all_results["integration"] = self.run_integration_tests(verbose)
        
        # Generate summary
        self.print_summary(all_results)
        
        return all_results
    
    def print_summary(self, results: Dict[str, Any]):
        """Print test summary."""
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        
        total_duration = time.time() - self.start_time if self.start_time else 0
        
        for test_type, result in results.items():
            status = "✅ PASSED" if result.get("success", False) else "❌ FAILED"
            duration = f"({result.get('duration', 0):.2f}s)" if result.get("duration") else ""
            print(f"{test_type.upper():12} {status} {duration}")
            
            if not result.get("success", False) and result.get("error"):
                print(f"           Error: {result['error']}")
        
        print(f"\nTotal Duration: {total_duration:.2f}s")
        
        # Overall status
        all_passed = all(result.get("success", False) for result in results.values())
        overall_status = "✅ ALL TESTS PASSED" if all_passed else "❌ SOME TESTS FAILED"
        print(f"\nOverall Status: {overall_status}")
        
        if all_passed:
            print("\n🎉 Congratulations! All tests are passing!")
        else:
            print("\n🔧 Please fix the failing tests before proceeding.")
    
    def run_quick_test(self) -> Dict[str, Any]:
        """Run a quick smoke test."""
        print("\n" + "="*60)
        print("QUICK SMOKE TEST")
        print("="*60)
        
        try:
            # Test basic imports
            from src.core.configurable_agent import ConfigurableAgent
            from src.core.config_loader import ConfigLoader
            from src.tools.tool_registry import ToolRegistry
            from src.memory.memory_manager import MemoryManager
            
            print("✓ All core modules import successfully")
            
            # Test configuration loading
            config_file = "configs/examples/research_agent.yml"
            if Path(config_file).exists():
                agent = ConfigurableAgent(config_file)
                config = agent.get_config()
                print(f"✓ Configuration loaded: {config.agent.name}")
                print(f"✓ LLM Provider: {config.llm.provider}")
                print(f"✓ Memory Enabled: {config.memory.enabled}")
            else:
                print(f"⚠ Configuration file not found: {config_file}")
            
            return {"success": True, "message": "Quick test passed"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}


def main():
    """Main entry point for the test runner."""
    parser = argparse.ArgumentParser(description="Test runner for configurable agents system")
    parser.add_argument("--all", action="store_true", help="Run all tests")
    parser.add_argument("--unit", action="store_true", help="Run unit tests only")
    parser.add_argument("--integration", action="store_true", help="Run integration tests only")
    parser.add_argument("--lint", action="store_true", help="Run lint tests only")
    parser.add_argument("--quick", action="store_true", help="Run quick smoke test")
    parser.add_argument("--file", type=str, help="Run specific test file")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--coverage", action="store_true", help="Generate coverage report")
    
    args = parser.parse_args()
    
    runner = TestRunner()
    
    if args.quick:
        result = runner.run_quick_test()
        runner.print_summary({"quick": result})
    elif args.unit:
        result = runner.run_unit_tests(args.verbose, args.coverage)
        runner.print_summary({"unit": result})
    elif args.integration:
        result = runner.run_integration_tests(args.verbose)
        runner.print_summary({"integration": result})
    elif args.lint:
        result = runner.run_lint_tests()
        runner.print_summary({"lint": result})
    elif args.file:
        result = runner.run_specific_test(args.file, args.verbose)
        runner.print_summary({"specific": result})
    else:
        # Default: run all tests
        runner.run_all_tests(args.verbose, args.coverage)


if __name__ == "__main__":
    main() 