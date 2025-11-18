"""
Task Dependency Analyzer

This module analyzes task dependencies and determines execution order,
identifies parallel execution opportunities, and detects circular dependencies.
"""

from typing import List, Set, Dict, Tuple
from dataclasses import dataclass
from collections import defaultdict, deque


@dataclass
class Task:
    """Represents a task with dependencies."""
    id: str
    name: str
    dependencies: List[str]
    estimated_time: int = 1
    priority: int = 1
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return isinstance(other, Task) and self.id == other.id


class DependencyAnalyzer:
    """Analyzes task dependencies and creates execution plans."""
    
    def __init__(self, tasks: List[Task]):
        """
        Initialize analyzer with list of tasks.
        
        Args:
            tasks: List of Task objects
        """
        self.tasks = {task.id: task for task in tasks}
        self.graph = self._build_graph()
        
    def _build_graph(self) -> Dict[str, Set[str]]:
        """
        Build dependency graph.
        
        Returns:
            Dictionary mapping task IDs to their dependencies
        """
        graph = defaultdict(set)
        for task_id, task in self.tasks.items():
            graph[task_id] = set(task.dependencies)
        return dict(graph)
    
    def detect_circular_dependencies(self) -> List[List[str]]:
        """
        Detect circular dependencies using DFS.
        
        Returns:
            List of cycles found, each cycle is a list of task IDs
        """
        cycles = []
        visited = set()
        rec_stack = set()
        path = []
        
        def dfs(task_id: str) -> bool:
            visited.add(task_id)
            rec_stack.add(task_id)
            path.append(task_id)
            
            for dependency in self.graph.get(task_id, []):
                if dependency not in visited:
                    if dfs(dependency):
                        return True
                elif dependency in rec_stack:
                    # Found cycle
                    cycle_start = path.index(dependency)
                    cycles.append(path[cycle_start:] + [dependency])
                    return True
            
            path.pop()
            rec_stack.remove(task_id)
            return False
        
        for task_id in self.tasks:
            if task_id not in visited:
                dfs(task_id)
        
        return cycles
    
    def topological_sort(self) -> List[str]:
        """
        Perform topological sort to get valid execution order.
        
        Returns:
            List of task IDs in valid execution order
            
        Raises:
            ValueError: If circular dependencies exist
        """
        cycles = self.detect_circular_dependencies()
        if cycles:
            raise ValueError(f"Circular dependencies detected: {cycles}")
        
        # Calculate in-degree: how many dependencies each task has
        in_degree = defaultdict(int)
        for task_id in self.tasks:
            in_degree[task_id] = len(self.graph.get(task_id, []))
        
        # Start with tasks that have no dependencies
        queue = deque([task_id for task_id in self.tasks if in_degree[task_id] == 0])
        result = []
        
        while queue:
            task_id = queue.popleft()
            result.append(task_id)
            
            # Find tasks that depend on the current task and reduce their in-degree
            for dependent_id in self.tasks:
                if task_id in self.graph.get(dependent_id, []):
                    in_degree[dependent_id] -= 1
                    if in_degree[dependent_id] == 0:
                        queue.append(dependent_id)
        
        if len(result) != len(self.tasks):
            raise ValueError("Graph has a cycle")
        
        return result
    
    def find_parallel_tasks(self) -> List[Set[str]]:
        """
        Identify tasks that can be executed in parallel.
        Groups tasks that have no dependencies on each other.
        
        Returns:
            List of sets, each set contains task IDs that can run in parallel
        """
        sorted_tasks = self.topological_sort()
        levels = []
        completed = set()
        
        while len(completed) < len(sorted_tasks):
            current_level = set()
            
            for task_id in sorted_tasks:
                if task_id in completed:
                    continue
                    
                # Check if all dependencies are completed
                dependencies = self.graph.get(task_id, set())
                if dependencies.issubset(completed):
                    current_level.add(task_id)
            
            if current_level:
                levels.append(current_level)
                completed.update(current_level)
            else:
                break
        
        return levels
    
    def calculate_critical_path(self) -> Tuple[List[str], int]:
        """
        Calculate the critical path (longest path through the dependency graph).
        
        Returns:
            Tuple of (path as list of task IDs, total estimated time)
        """
        # Calculate earliest start time for each task
        earliest_start = {}
        sorted_tasks = self.topological_sort()
        
        for task_id in sorted_tasks:
            task = self.tasks[task_id]
            max_dep_time = 0
            
            for dep_id in task.dependencies:
                if dep_id in earliest_start:
                    dep_end_time = earliest_start[dep_id] + self.tasks[dep_id].estimated_time
                    max_dep_time = max(max_dep_time, dep_end_time)
            
            earliest_start[task_id] = max_dep_time
        
        # Find the critical path by backtracking from the task with latest end time
        critical_path = []
        total_time = 0
        
        if earliest_start:
            # Find task with maximum end time
            end_times = {tid: earliest_start[tid] + self.tasks[tid].estimated_time 
                        for tid in self.tasks}
            last_task = max(end_times, key=end_times.get)
            total_time = end_times[last_task]
            
            # Backtrack to build critical path
            current = last_task
            critical_path.append(current)
            current_time = earliest_start[current]
            
            while current_time > 0:
                found = False
                for dep_id in self.tasks[current].dependencies:
                    dep_end = earliest_start[dep_id] + self.tasks[dep_id].estimated_time
                    if dep_end == current_time:
                        critical_path.append(dep_id)
                        current = dep_id
                        current_time = earliest_start[dep_id]
                        found = True
                        break
                if not found:
                    break
            
            critical_path.reverse()
        
        return critical_path, total_time
    
    def generate_execution_plan(self) -> Dict:
        """
        Generate a complete execution plan with phases and parallelization.
        
        Returns:
            Dictionary containing execution plan details
        """
        parallel_groups = self.find_parallel_tasks()
        critical_path, critical_time = self.calculate_critical_path()
        
        plan = {
            'phases': [],
            'critical_path': critical_path,
            'critical_path_time': critical_time,
            'total_tasks': len(self.tasks),
            'parallelization_factor': 0
        }
        
        total_sequential_time = sum(task.estimated_time for task in self.tasks.values())
        if critical_time > 0:
            plan['parallelization_factor'] = total_sequential_time / critical_time
        
        for phase_num, group in enumerate(parallel_groups, 1):
            phase_tasks = [self.tasks[tid] for tid in group]
            phase_time = max((task.estimated_time for task in phase_tasks), default=0)
            
            plan['phases'].append({
                'phase': phase_num,
                'tasks': [task.id for task in phase_tasks],
                'can_parallelize': len(phase_tasks) > 1,
                'estimated_time': phase_time
            })
        
        return plan


def analyze_task_dependencies(tasks: List[Task]) -> Dict:
    """
    Analyze task dependencies and return comprehensive analysis.
    
    Args:
        tasks: List of Task objects
        
    Returns:
        Dictionary containing dependency analysis results
    """
    analyzer = DependencyAnalyzer(tasks)
    
    try:
        execution_plan = analyzer.generate_execution_plan()
        cycles = []
    except ValueError as e:
        cycles = analyzer.detect_circular_dependencies()
        execution_plan = None
    
    return {
        'has_circular_dependencies': len(cycles) > 0,
        'circular_dependencies': cycles,
        'execution_plan': execution_plan
    }


if __name__ == '__main__':
    # Example usage
    sample_tasks = [
        Task('T001', 'Setup environment', []),
        Task('T002', 'Install dependencies', ['T001'], estimated_time=5),
        Task('T003', 'Configure database', ['T001'], estimated_time=3),
        Task('T004', 'Write tests', ['T002'], estimated_time=8),
        Task('T005', 'Write code', ['T002', 'T003'], estimated_time=10),
        Task('T006', 'Run tests', ['T004', 'T005'], estimated_time=2),
    ]
    
    result = analyze_task_dependencies(sample_tasks)
    print("Analysis complete:")
    print(f"Circular dependencies: {result['has_circular_dependencies']}")
    if result['execution_plan']:
        print(f"Total phases: {len(result['execution_plan']['phases'])}")
        print(f"Critical path time: {result['execution_plan']['critical_path_time']}")
        print(f"Parallelization factor: {result['execution_plan']['parallelization_factor']:.2f}x")
