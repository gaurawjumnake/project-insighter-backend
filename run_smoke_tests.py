import subprocess
import sys
import argparse
from pathlib import Path


class SmokeTestRunner:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.test_dir = self.project_root / "tests"
    
    def run_all_tests(self, verbose: bool = True):
        cmd = ["pytest", str(self.test_dir)]
        if verbose:
            cmd.append("-vv")
        return self._run_command(cmd)
    
    def run_orchestrator_tests(self, verbose: bool = True):
        cmd = [
            "pytest",
            str(self.test_dir / "test_insights_workflow" / "test_orchestrator.py")
        ]
        if verbose:
            cmd.append("-vv")
        return self._run_command(cmd)
    
    def run_service_tests(self, verbose: bool = True):
        cmd = [
            "pytest",
            str(self.test_dir / "test_insights_workflow" / "test_services.py")
        ]
        if verbose:
            cmd.append("-vv")
        return self._run_command(cmd)
    
    def run_integration_tests(self, verbose: bool = True):
        cmd = [
            "pytest",
            str(self.test_dir / "test_insights_workflow" / "test_integration.py")
        ]
        if verbose:
            cmd.append("-vv")
        return self._run_command(cmd)
    
    def run_smoke_tests(self, verbose: bool = True):
        """Run tests marked with @pytest.mark.smoke."""
        cmd = ["pytest", str(self.test_dir), "-m", "smoke"]
        if verbose:
            cmd.append("-vv")
        return self._run_command(cmd)
    
    def run_with_coverage(self):
        """Run tests with coverage report."""
        cmd = [
            "pytest",
            str(self.test_dir),
            "--cov=backend.insights_workflow",
            "--cov-report=html",
            "--cov-report=term",
            "-v"
        ]
        return self._run_command(cmd)
    
    def run_fast_tests(self, verbose: bool = True):
        """Run fast tests (unit tests only, excluding slow/integration)."""
        cmd = [
            "pytest",
            str(self.test_dir),
            "-v",
            "-m", "not slow"
        ]
        return self._run_command(cmd)
    
    def run_specific_test(self, test_path: str, verbose: bool = True):
        """Run a specific test file or test function."""
        cmd = ["pytest", test_path]
        if verbose:
            cmd.append("-vv")
        return self._run_command(cmd)
    
    def _run_command(self, cmd: list) -> int:
        """Execute a command and return exit code."""
        print(f"Running: {' '.join(cmd)}\n")
        try:
            result = subprocess.run(cmd, cwd=self.project_root)
            return result.returncode
        except Exception as e:
            print(f"Error running tests: {e}", file=sys.stderr)
            return 1


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Smoke test runner for Project Insighter Backend"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Test command")
    
    # All tests
    subparsers.add_parser("all", help="Run all tests")
    
    # Individual test suites
    subparsers.add_parser("orchestrator", help="Run orchestrator tests")
    subparsers.add_parser("services", help="Run service layer tests")
    subparsers.add_parser("integration", help="Run integration tests")
    
    # Special modes
    subparsers.add_parser("smoke", help="Run smoke tests")
    subparsers.add_parser("fast", help="Run fast tests (unit only)")
    subparsers.add_parser("coverage", help="Run tests with coverage report")
    
    # Specific test
    specific = subparsers.add_parser("specific", help="Run a specific test")
    specific.add_argument("path", help="Test file or function path")
    
    # Global options
    parser.add_argument("-q", "--quiet", action="store_true", help="Quiet mode")
    
    args = parser.parse_args()
    
    runner = SmokeTestRunner()
    verbose = not args.quiet
    
    exit_code = 1
    if args.command == "all" or args.command is None:
        exit_code = runner.run_all_tests(verbose=verbose)
    elif args.command == "orchestrator":
        exit_code = runner.run_orchestrator_tests(verbose=verbose)
    elif args.command == "services":
        exit_code = runner.run_service_tests(verbose=verbose)
    elif args.command == "integration":
        exit_code = runner.run_integration_tests(verbose=verbose)
    elif args.command == "smoke":
        exit_code = runner.run_smoke_tests(verbose=verbose)
    elif args.command == "fast":
        exit_code = runner.run_fast_tests(verbose=verbose)
    elif args.command == "coverage":
        exit_code = runner.run_with_coverage()
    elif args.command == "specific":
        exit_code = runner.run_specific_test(args.path, verbose=verbose)
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
