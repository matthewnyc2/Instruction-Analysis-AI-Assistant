"""
Main runner script for the Instruction Analysis AI Assistant tools

This script provides a command-line interface to run various analysis tools
on instruction markdown files.
"""

import argparse
import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from tools.parsers.markdown_parser import parse_instruction_file
from tools.parsers.dependency_analyzer import Task, analyze_task_dependencies
from tools.parsers.pseudocode_validator import validate_pseudocode


def analyze_instruction_file(filepath: str, verbose: bool = False):
    """
    Analyze an instruction markdown file.
    
    Args:
        filepath: Path to the markdown file
        verbose: Whether to print detailed output
    """
    print(f"\n{'='*60}")
    print(f"Analyzing: {filepath}")
    print(f"{'='*60}\n")
    
    # Parse the file
    try:
        result = parse_instruction_file(filepath)
    except Exception as e:
        print(f"Error parsing file: {e}")
        return
    
    # Print summary
    print(f"📄 Sections found: {len(result['sections'])}")
    if verbose and result['sections']:
        for section in result['sections']:
            indent = "  " * (section.level - 1)
            print(f"  {indent}- {section.title} (Level {section.level})")
    
    print(f"\n✓ Tasks found: {len(result['tasks'])}")
    if verbose and result['tasks']:
        for task in result['tasks']:
            deps = f" (depends on: {', '.join(task.dependencies)})" if task.dependencies else ""
            parallel = " [PARALLEL]" if task.is_parallel else ""
            print(f"  {task.step_number}. {task.description}{deps}{parallel}")
    
    print(f"\n❓ Questions found: {len(result['questions'])}")
    if verbose and result['questions']:
        for question in result['questions']:
            print(f"  - {question}")
    
    print(f"\n⚠️  Ambiguities found: {len(result['ambiguities'])}")
    if verbose and result['ambiguities']:
        for amb in result['ambiguities']:
            print(f"  Line {amb['line']}: {amb['text']}")
            print(f"    Reason: {amb['reason']}")
    
    print(f"\n💻 Code blocks found: {len(result['code_blocks'])}")
    
    # Analyze dependencies if tasks exist
    if result['tasks']:
        print(f"\n{'='*60}")
        print("DEPENDENCY ANALYSIS")
        print(f"{'='*60}\n")
        
        # Convert to Task objects
        tasks = []
        for i, task in enumerate(result['tasks']):
            task_id = f"T{i+1:03d}"
            tasks.append(Task(task_id, task.description, task.dependencies, estimated_time=1))
        
        analysis = analyze_task_dependencies(tasks)
        
        if analysis['has_circular_dependencies']:
            print("❌ Circular dependencies detected!")
            for cycle in analysis['circular_dependencies']:
                print(f"  Cycle: {' -> '.join(cycle)}")
        else:
            print("✓ No circular dependencies")
            
            if analysis['execution_plan']:
                plan = analysis['execution_plan']
                print(f"\nExecution Plan:")
                print(f"  Total tasks: {plan['total_tasks']}")
                print(f"  Total phases: {len(plan['phases'])}")
                print(f"  Critical path: {' -> '.join(plan['critical_path'])}")
                print(f"  Critical path time: {plan['critical_path_time']} units")
                print(f"  Parallelization factor: {plan['parallelization_factor']:.2f}x")
                
                if verbose:
                    print(f"\n  Phase breakdown:")
                    for phase in plan['phases']:
                        parallel_note = " (can parallelize)" if phase['can_parallelize'] else ""
                        print(f"    Phase {phase['phase']}: {len(phase['tasks'])} tasks{parallel_note}")
                        print(f"      Tasks: {', '.join(phase['tasks'])}")
                        print(f"      Estimated time: {phase['estimated_time']} units")


def validate_pseudocode_file(filepath: str):
    """
    Validate a pseudocode file.
    
    Args:
        filepath: Path to the pseudocode file
    """
    print(f"\n{'='*60}")
    print(f"Validating Pseudocode: {filepath}")
    print(f"{'='*60}\n")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            pseudocode = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return
    
    result = validate_pseudocode(pseudocode)
    print(result['report'])


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description='Instruction Analysis AI Assistant - Command Line Tools',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze an instruction file
  python run_analysis.py analyze examples/inputs/sample_user_auth_instructions.md
  
  # Analyze with verbose output
  python run_analysis.py analyze examples/inputs/sample_api_instructions.md --verbose
  
  # Validate pseudocode
  python run_analysis.py validate examples/outputs/pseudocode_user_auth.md
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze an instruction markdown file')
    analyze_parser.add_argument('file', help='Path to instruction markdown file')
    analyze_parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate pseudocode file')
    validate_parser.add_argument('file', help='Path to pseudocode file')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Check if file exists
    if not os.path.exists(args.file):
        print(f"Error: File not found: {args.file}")
        sys.exit(1)
    
    if args.command == 'analyze':
        analyze_instruction_file(args.file, args.verbose)
    elif args.command == 'validate':
        validate_pseudocode_file(args.file)


if __name__ == '__main__':
    main()
