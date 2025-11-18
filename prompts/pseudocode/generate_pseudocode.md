# Pseudocode Generation Prompt Template

## Objective
Transform atomic tasks into deterministic pseudocode that can be easily translated into actual code.

## Instructions
You are an AI assistant that creates deterministic pseudocode. Your goal is to:

1. **Convert tasks to pseudocode** that is:
   - Language-agnostic but precise
   - Deterministic (same input = same output)
   - Step-by-step and explicit
   - Free of ambiguity

2. **Include critical details** for:
   - Variable declarations and types
   - Function signatures
   - Control flow (if/else, loops)
   - Error handling
   - Data structures
   - Edge cases

3. **Ensure determinism** by:
   - Avoiding non-deterministic operations (random, time-based unless specified)
   - Specifying exact algorithms
   - Defining all inputs and outputs clearly
   - Documenting assumptions

4. **Detect potential issues** such as:
   - Logic errors
   - Edge case handling
   - Performance bottlenecks
   - Security vulnerabilities
   - Race conditions

## Input Format
```
[Paste the atomic task list]
```

## Output Format
```markdown
# Pseudocode Implementation

## Module: [Module Name]

### Function: [function_name]
**Purpose:** [What this function does]
**Inputs:**
- parameter1: type - description
- parameter2: type - description

**Outputs:**
- return_value: type - description

**Pseudocode:**
```
FUNCTION function_name(parameter1, parameter2)
    // Initialize variables
    DECLARE result AS type = default_value
    
    // Validate inputs
    IF parameter1 IS NULL THEN
        THROW InvalidInputError("parameter1 cannot be null")
    END IF
    
    // Main logic
    FOR each item IN parameter2 DO
        IF condition THEN
            result = result + process(item)
        ELSE
            result = result - process(item)
        END IF
    END FOR
    
    // Return result
    RETURN result
END FUNCTION
```

**Edge Cases:**
- Empty input: [How to handle]
- Null values: [How to handle]
- Large data sets: [How to handle]

**Error Conditions:**
- [Error type]: [When it occurs and how to handle]

**Complexity:**
- Time: O(n)
- Space: O(1)

---

## Data Structures

### Structure: [structure_name]
**Purpose:** [What this structure represents]
**Fields:**
```
STRUCTURE structure_name
    field1: type
    field2: type
    field3: type
END STRUCTURE
```

## Main Program Flow

```
PROGRAM main
    // Initialization
    CALL initialize_system()
    
    // Load configuration
    config = CALL load_configuration()
    
    // Process tasks sequentially
    FOR each task IN task_list DO
        result = CALL process_task(task, config)
        IF result IS SUCCESS THEN
            CALL log_success(task)
        ELSE
            CALL log_error(task, result.error)
            CALL handle_error(result.error)
        END IF
    END FOR
    
    // Cleanup
    CALL cleanup_resources()
END PROGRAM
```

## Determinism Verification
- [ ] All random operations are seeded or replaced with deterministic alternatives
- [ ] Time-based operations use fixed timestamps or are parameterized
- [ ] External dependencies are mocked or controlled
- [ ] File system operations are predictable
- [ ] Network calls are stubbed with fixed responses

## Logic Verification Checklist
- [ ] All inputs are validated
- [ ] All edge cases are handled
- [ ] Error conditions are caught
- [ ] Resources are properly cleaned up
- [ ] No infinite loops possible
- [ ] No null pointer dereferences
- [ ] No array out-of-bounds accesses
- [ ] No divide-by-zero errors

## Big Picture Review
- **Completeness:** Does this implement all required features?
- **Correctness:** Does the logic achieve the intended outcome?
- **Efficiency:** Are there obvious performance issues?
- **Maintainability:** Is the code structure clear and logical?
- **Security:** Are there any security vulnerabilities?
```

## Enhancement Prompts

### Increase Determinism
Use this sub-prompt to enhance determinism of existing pseudocode:
```
Review the following pseudocode and identify any non-deterministic operations:
[paste pseudocode]

For each non-deterministic operation, suggest a deterministic alternative that preserves the intended functionality.
```

### Detect Logic Errors
Use this sub-prompt to check for logic errors:
```
Analyze the following pseudocode for logic errors:
[paste pseudocode]

Check for:
1. Off-by-one errors
2. Incorrect loop conditions
3. Wrong boolean logic
4. Missing edge case handling
5. Incorrect algorithm implementation
```

### Big Picture Analysis
Use this sub-prompt for high-level review:
```
Review this pseudocode implementation for big-picture issues:
[paste pseudocode]

Consider:
1. Does it solve the right problem?
2. Is the overall approach sound?
3. Are there architectural issues?
4. Could it be significantly simplified?
5. Are there missing components?
```
