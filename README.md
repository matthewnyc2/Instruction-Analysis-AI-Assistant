# Instruction-Analysis-AI-Assistant

A comprehensive repository for AI prompts and tools designed to process markdown instruction files through a complete analysis pipeline. This system helps clarify tasks, identify optimal execution steps, recommend appropriate technology stacks, create atomic task lists, generate deterministic pseudocode, and detect potential errors.

## 📁 Repository Structure

```
.
├── prompts/                 # AI prompt templates for each analysis phase
│   ├── clarification/      # Prompts for identifying ambiguities and questions
│   ├── steps/              # Prompts for breaking down tasks and ordering
│   ├── tech-stack/         # Prompts for technology recommendations
│   ├── atomic-tasks/       # Prompts for creating detailed task lists
│   └── pseudocode/         # Prompts for generating deterministic pseudocode
│
├── tools/                   # Python analysis and parsing tools
│   └── parsers/            # Markdown, dependency, and pseudocode analysis
│
├── examples/                # Sample inputs and outputs
│   ├── inputs/             # Example instruction markdown files
│   └── outputs/            # Generated analysis results
│
├── tests/                   # Unit tests for all tools
└── run_analysis.py         # Command-line interface for running analysis
```

## 🎯 Features

### 1. Task Clarification
- Identify ambiguous statements and vague requirements
- Extract questions that need answers
- Detect unclear dependencies and contradictions
- Prioritize clarification needs (high/medium/low)

### 2. Step Identification
- Break down complex tasks into simple, actionable steps
- Determine optimal execution order
- Identify dependencies between steps
- Find opportunities for parallel execution

### 3. Technology Stack Recommendations
- Suggest appropriate programming languages and frameworks
- Recommend databases and infrastructure
- Justify technology choices based on requirements
- Consider scalability, security, and team expertise

### 4. Atomic Task Lists
- Create detailed, indivisible task units
- Specify inputs, outputs, and acceptance criteria
- Organize tasks into execution phases
- Calculate critical path and parallelization opportunities
- Estimate effort and identify risks

### 5. Pseudocode Generation
- Transform tasks into deterministic, language-agnostic pseudocode
- Include comprehensive error handling
- Define all data structures and functions
- Validate determinism and detect logic errors
- Check for security vulnerabilities and edge cases

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- No external dependencies (uses only standard library)

### Installation

Clone the repository:
```bash
git clone https://github.com/matthewnyc2/Instruction-Analysis-AI-Assistant.git
cd Instruction-Analysis-AI-Assistant
```

### Running Tests

Run all unit tests:
```bash
python -m unittest discover tests
```

Run specific test modules:
```bash
python -m unittest tests.test_markdown_parser
python -m unittest tests.test_dependency_analyzer
python -m unittest tests.test_pseudocode_validator
```

## 📖 Usage

### Command-Line Interface

Analyze an instruction file:
```bash
python run_analysis.py analyze examples/inputs/sample_user_auth_instructions.md
```

Analyze with verbose output:
```bash
python run_analysis.py analyze examples/inputs/sample_api_instructions.md --verbose
```

Validate pseudocode:
```bash
python run_analysis.py validate examples/outputs/pseudocode_user_auth.md
```

### Python API

#### Parse Markdown Instructions
```python
from tools.parsers.markdown_parser import parse_instruction_file

result = parse_instruction_file('path/to/instruction.md')
print(f"Found {len(result['sections'])} sections")
print(f"Found {len(result['tasks'])} tasks")
print(f"Found {len(result['ambiguities'])} ambiguities")
```

#### Analyze Task Dependencies
```python
from tools.parsers.dependency_analyzer import Task, analyze_task_dependencies

tasks = [
    Task('T001', 'Setup environment', []),
    Task('T002', 'Install dependencies', ['T001']),
    Task('T003', 'Run tests', ['T002']),
]

result = analyze_task_dependencies(tasks)
if result['execution_plan']:
    plan = result['execution_plan']
    print(f"Critical path: {' -> '.join(plan['critical_path'])}")
    print(f"Parallelization factor: {plan['parallelization_factor']:.2f}x")
```

#### Validate Pseudocode
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

## 📝 Prompt Templates

Each phase of analysis has detailed prompt templates in the `prompts/` directory:

- **clarify_instructions.md** - Identify ambiguities and generate clarifying questions
- **identify_steps.md** - Break down tasks and determine execution order
- **recommend_tech.md** - Suggest appropriate technology stack
- **create_task_list.md** - Create detailed atomic task lists with dependencies
- **generate_pseudocode.md** - Transform tasks into deterministic pseudocode

## 🧪 Examples

The `examples/` directory contains complete workflow demonstrations:

### Input Examples
- `sample_user_auth_instructions.md` - User authentication system requirements
- `sample_data_pipeline_instructions.md` - Data processing pipeline specifications
- `sample_api_instructions.md` - REST API development requirements

### Output Examples
- `clarified_user_auth.md` - Clarification questions and assumptions
- `steps_user_auth.md` - Step-by-step breakdown with dependencies
- `tech_stack_user_auth.md` - Technology recommendations with justifications
- `atomic_tasks_user_auth.md` - Detailed task list with execution plan
- `pseudocode_user_auth.md` - Complete deterministic pseudocode implementation

## 🛠️ Tools

### Markdown Parser (`markdown_parser.py`)
- Parse markdown sections and headers
- Extract numbered task steps
- Identify task dependencies
- Find code blocks and questions
- Detect ambiguous statements

### Dependency Analyzer (`dependency_analyzer.py`)
- Build dependency graphs
- Detect circular dependencies
- Perform topological sort
- Find parallel execution opportunities
- Calculate critical path
- Generate optimized execution plans

### Pseudocode Validator (`pseudocode_validator.py`)
- Check for non-deterministic operations
- Detect logic errors (infinite loops, off-by-one, etc.)
- Validate error handling
- Check resource cleanup
- Analyze code complexity
- Generate detailed validation reports

## 🤖 AI Integration

This repository is designed to work with AI assistants. The prompt templates provide:

1. **Clear objectives** for each analysis phase
2. **Step-by-step instructions** for the AI to follow
3. **Input/output format specifications**
4. **Example usage** to guide the AI
5. **Quality checklists** for validation

### Recommended Workflow

1. **Start with clarification** using `prompts/clarification/clarify_instructions.md`
2. **Identify steps** using `prompts/steps/identify_steps.md`
3. **Select technology** using `prompts/tech-stack/recommend_tech.md`
4. **Create atomic tasks** using `prompts/atomic-tasks/create_task_list.md`
5. **Generate pseudocode** using `prompts/pseudocode/generate_pseudocode.md`
6. **Validate results** using the analysis tools

## 🔬 Testing

All tools include comprehensive unit tests:
- **43 total test cases** covering all functionality
- **100% pass rate** on core features
- Tests for edge cases, error conditions, and normal operations

## 📊 Analysis Capabilities

### Dependency Analysis
- ✅ Topological sorting for valid execution order
- ✅ Circular dependency detection
- ✅ Parallel task identification
- ✅ Critical path calculation
- ✅ Parallelization factor metrics

### Code Quality Checks
- ✅ Determinism validation
- ✅ Logic error detection
- ✅ Error handling verification
- ✅ Resource cleanup checks
- ✅ Complexity analysis

### Documentation Extraction
- ✅ Section parsing
- ✅ Task extraction
- ✅ Question identification
- ✅ Code block extraction
- ✅ Ambiguity detection

## 🤝 Contributing

Contributions are welcome! Please ensure:
1. All tests pass before submitting
2. New features include unit tests
3. Code follows existing style conventions
4. Documentation is updated accordingly

## 📄 License

This project is open source and available under the MIT License.

## 🙋 Support

For questions, issues, or suggestions, please open an issue on GitHub.
