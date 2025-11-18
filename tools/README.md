# Tools - Parsers and Analysis Scripts

This directory contains Python scripts for parsing and analyzing instruction markdown files.

## Modules

### markdown_parser.py
Parses markdown instruction files to extract structured information.

**Features:**
- Parse markdown sections and headers
- Extract numbered task steps
- Identify task dependencies
- Find code blocks
- Extract questions
- Detect ambiguous statements

**Usage:**
```python
from tools.parsers.markdown_parser import parse_instruction_file

result = parse_instruction_file('path/to/instruction.md')
print(f"Found {len(result['sections'])} sections")
print(f"Found {len(result['tasks'])} tasks")
print(f"Found {len(result['ambiguities'])} ambiguities")
```

### dependency_analyzer.py
Analyzes task dependencies and creates execution plans.

**Features:**
- Build dependency graphs
- Detect circular dependencies
- Perform topological sort
- Find parallel execution opportunities
- Calculate critical path
- Generate execution plans with phases

**Usage:**
```python
from tools.parsers.dependency_analyzer import Task, analyze_task_dependencies

tasks = [
    Task('T001', 'Setup environment', []),
    Task('T002', 'Install dependencies', ['T001']),
    Task('T003', 'Configure database', ['T001']),
    Task('T004', 'Run tests', ['T002', 'T003']),
]

result = analyze_task_dependencies(tasks)

if not result['has_circular_dependencies']:
    plan = result['execution_plan']
    print(f"Total phases: {len(plan['phases'])}")
    print(f"Critical path time: {plan['critical_path_time']}")
    print(f"Parallelization factor: {plan['parallelization_factor']:.2f}x")
```

### pseudocode_validator.py
Validates pseudocode for determinism, logic errors, and other issues.

**Features:**
- Check for non-deterministic operations
- Detect logic errors (infinite loops, off-by-one, etc.)
- Validate error handling
- Check resource cleanup
- Analyze code complexity
- Generate detailed validation reports

**Usage:**
```python
from tools.parsers.pseudocode_validator import validate_pseudocode

pseudocode = """
FUNCTION process_data(input)
    result = calculate(input)
    RETURN result
END FUNCTION
"""

result = validate_pseudocode(pseudocode)
print(result['report'])
print(f"Total issues: {result['total_issues']}")
```

## Running Tests

All modules include unit tests in the `tests/` directory.

```bash
# Run all tests
python -m unittest discover tests

# Run specific test file
python -m unittest tests.test_markdown_parser
python -m unittest tests.test_dependency_analyzer
python -m unittest tests.test_pseudocode_validator
```

## Requirements

- Python 3.7+
- No external dependencies (uses only standard library)

## Example Workflow

1. **Parse instruction file:**
   ```python
   from tools.parsers.markdown_parser import parse_instruction_file
   data = parse_instruction_file('examples/inputs/sample_user_auth_instructions.md')
   ```

2. **Analyze dependencies:**
   ```python
   from tools.parsers.dependency_analyzer import Task, analyze_task_dependencies
   
   # Convert parsed tasks to Task objects
   tasks = [Task(f'T{i+1:03d}', task.description, task.dependencies) 
            for i, task in enumerate(data['tasks'])]
   
   analysis = analyze_task_dependencies(tasks)
   ```

3. **Validate pseudocode:**
   ```python
   from tools.parsers.pseudocode_validator import validate_pseudocode
   
   with open('examples/outputs/pseudocode_user_auth.md', 'r') as f:
       pseudocode = f.read()
   
   validation = validate_pseudocode(pseudocode)
   ```

## Contributing

When adding new parsers or analyzers:
1. Follow the existing code structure
2. Add comprehensive docstrings
3. Include unit tests
4. Update this README with usage examples
