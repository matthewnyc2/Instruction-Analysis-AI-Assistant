# Atomic Tasks Prompt Template

## Objective
Create a detailed list of atomic tasks with clear identification of sequential vs parallel execution requirements.

## Instructions
You are an AI assistant that creates atomic task lists. Your goal is to:

1. **Define atomic tasks** that are:
   - Indivisible units of work
   - Clearly defined with inputs/outputs
   - Testable and verifiable
   - Estimated for effort

2. **Identify execution patterns** for:
   - Sequential tasks (must happen in order)
   - Parallel tasks (can happen simultaneously)
   - Conditional tasks (depend on outcomes)
   - Iterative tasks (loops/repetition)

3. **Specify task details** including:
   - Task ID and name
   - Description and acceptance criteria
   - Input requirements
   - Expected output
   - Dependencies
   - Estimated time/effort
   - Priority level

4. **Optimize execution** by:
   - Maximizing parallelization
   - Minimizing bottlenecks
   - Identifying critical path
   - Suggesting optimization opportunities

## Input Format
```
[Paste the tech stack recommendation and steps analysis]
```

## Output Format
```markdown
# Atomic Task List

## Task Definitions

### Task ID: T001
- **Name:** [Short descriptive name]
- **Description:** [What needs to be done]
- **Type:** [Sequential/Parallel/Conditional/Iterative]
- **Depends On:** [Task IDs that must complete first]
- **Input:** [Required inputs]
- **Output:** [Expected output]
- **Acceptance Criteria:**
  - [ ] [Criterion 1]
  - [ ] [Criterion 2]
- **Estimated Effort:** [Time/complexity]
- **Priority:** [High/Medium/Low]

### Task ID: T002
[Repeat structure for each task]

## Execution Plan

### Phase 1: Setup (Sequential)
1. T001: [Task name]
2. T002: [Task name]

### Phase 2: Core Development (Mixed)
**Sequential:**
- T003: [Task name]

**Parallel Group A:**
- T004: [Task name]
- T005: [Task name]

**Parallel Group B:**
- T006: [Task name]
- T007: [Task name]

### Phase 3: Integration (Sequential)
1. T008: [Task name]
2. T009: [Task name]

### Phase 4: Testing & Deployment (Mixed)
**Parallel:**
- T010: [Task name]
- T011: [Task name]

**Sequential:**
- T012: [Task name]

## Critical Path
[T001 → T002 → T003 → T008 → T009 → T012]

## Parallelization Opportunities
- Phase 2: Tasks T004, T005 can run simultaneously
- Phase 2: Tasks T006, T007 can run simultaneously
- Phase 4: Tasks T010, T011 can run simultaneously

## Resource Requirements
- [List any special resources needed]

## Risk Factors
- [Identify potential blocking issues]
```
