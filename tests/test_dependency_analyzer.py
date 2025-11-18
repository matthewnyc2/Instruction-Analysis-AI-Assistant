"""
Unit tests for dependency_analyzer module
"""

import unittest
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.parsers.dependency_analyzer import (
    DependencyAnalyzer, Task, analyze_task_dependencies
)


class TestDependencyAnalyzer(unittest.TestCase):
    """Test cases for DependencyAnalyzer class"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Simple linear dependency chain
        self.linear_tasks = [
            Task('T001', 'Setup', []),
            Task('T002', 'Install', ['T001']),
            Task('T003', 'Configure', ['T002']),
            Task('T004', 'Test', ['T003']),
        ]
        
        # Tasks with parallel opportunities
        self.parallel_tasks = [
            Task('T001', 'Setup', []),
            Task('T002', 'Database', ['T001']),
            Task('T003', 'Frontend', ['T001']),
            Task('T004', 'Backend', ['T001']),
            Task('T005', 'Integration', ['T002', 'T003', 'T004']),
        ]
        
        # Tasks with circular dependency
        self.circular_tasks = [
            Task('T001', 'A', ['T003']),
            Task('T002', 'B', ['T001']),
            Task('T003', 'C', ['T002']),
        ]
    
    def test_build_graph(self):
        """Test building dependency graph"""
        analyzer = DependencyAnalyzer(self.linear_tasks)
        
        self.assertIsInstance(analyzer.graph, dict)
        self.assertEqual(len(analyzer.graph), 4)
        self.assertEqual(analyzer.graph['T002'], {'T001'})
    
    def test_detect_no_circular_dependencies(self):
        """Test detecting no circular dependencies in valid graph"""
        analyzer = DependencyAnalyzer(self.linear_tasks)
        cycles = analyzer.detect_circular_dependencies()
        
        self.assertEqual(len(cycles), 0)
    
    def test_detect_circular_dependencies(self):
        """Test detecting circular dependencies"""
        analyzer = DependencyAnalyzer(self.circular_tasks)
        cycles = analyzer.detect_circular_dependencies()
        
        self.assertTrue(len(cycles) > 0)
    
    def test_topological_sort_linear(self):
        """Test topological sort on linear dependencies"""
        analyzer = DependencyAnalyzer(self.linear_tasks)
        sorted_ids = analyzer.topological_sort()
        
        self.assertEqual(len(sorted_ids), 4)
        self.assertEqual(sorted_ids[0], 'T001')
        self.assertEqual(sorted_ids[-1], 'T004')
    
    def test_topological_sort_fails_on_cycle(self):
        """Test that topological sort raises error on circular dependencies"""
        analyzer = DependencyAnalyzer(self.circular_tasks)
        
        with self.assertRaises(ValueError):
            analyzer.topological_sort()
    
    def test_find_parallel_tasks_linear(self):
        """Test finding parallel tasks in linear chain"""
        analyzer = DependencyAnalyzer(self.linear_tasks)
        parallel_groups = analyzer.find_parallel_tasks()
        
        # Linear chain should have one task per level
        self.assertEqual(len(parallel_groups), 4)
        for group in parallel_groups:
            self.assertEqual(len(group), 1)
    
    def test_find_parallel_tasks_with_parallelization(self):
        """Test finding parallel tasks when parallelization possible"""
        analyzer = DependencyAnalyzer(self.parallel_tasks)
        parallel_groups = analyzer.find_parallel_tasks()
        
        # Should have 3 levels: [T001], [T002, T003, T004], [T005]
        self.assertEqual(len(parallel_groups), 3)
        
        # First level should have just setup
        self.assertEqual(len(parallel_groups[0]), 1)
        self.assertIn('T001', parallel_groups[0])
        
        # Second level should have 3 parallel tasks
        self.assertEqual(len(parallel_groups[1]), 3)
        self.assertIn('T002', parallel_groups[1])
        self.assertIn('T003', parallel_groups[1])
        self.assertIn('T004', parallel_groups[1])
        
        # Third level should have integration
        self.assertEqual(len(parallel_groups[2]), 1)
        self.assertIn('T005', parallel_groups[2])
    
    def test_calculate_critical_path_linear(self):
        """Test calculating critical path for linear dependencies"""
        analyzer = DependencyAnalyzer(self.linear_tasks)
        path, total_time = analyzer.calculate_critical_path()
        
        self.assertEqual(len(path), 4)
        self.assertEqual(total_time, 4)  # 4 tasks, 1 time unit each
        self.assertEqual(path[0], 'T001')
        self.assertEqual(path[-1], 'T004')
    
    def test_calculate_critical_path_with_times(self):
        """Test critical path calculation with different task times"""
        tasks_with_time = [
            Task('T001', 'Setup', [], estimated_time=2),
            Task('T002', 'Fast path', ['T001'], estimated_time=1),
            Task('T003', 'Slow path', ['T001'], estimated_time=5),
            Task('T004', 'End', ['T002', 'T003'], estimated_time=2),
        ]
        analyzer = DependencyAnalyzer(tasks_with_time)
        path, total_time = analyzer.calculate_critical_path()
        
        # Critical path should be T001 -> T003 -> T004 (2 + 5 + 2 = 9)
        self.assertEqual(total_time, 9)
        self.assertIn('T003', path)
    
    def test_generate_execution_plan(self):
        """Test generating complete execution plan"""
        analyzer = DependencyAnalyzer(self.parallel_tasks)
        plan = analyzer.generate_execution_plan()
        
        self.assertIsInstance(plan, dict)
        self.assertIn('phases', plan)
        self.assertIn('critical_path', plan)
        self.assertIn('critical_path_time', plan)
        self.assertIn('total_tasks', plan)
        self.assertIn('parallelization_factor', plan)
        
        self.assertEqual(plan['total_tasks'], 5)
        self.assertTrue(len(plan['phases']) > 0)
    
    def test_execution_plan_phases(self):
        """Test execution plan phase details"""
        analyzer = DependencyAnalyzer(self.parallel_tasks)
        plan = analyzer.generate_execution_plan()
        
        # Check phase structure
        for phase in plan['phases']:
            self.assertIn('phase', phase)
            self.assertIn('tasks', phase)
            self.assertIn('can_parallelize', phase)
            self.assertIn('estimated_time', phase)
    
    def test_parallelization_factor(self):
        """Test parallelization factor calculation"""
        analyzer = DependencyAnalyzer(self.parallel_tasks)
        plan = analyzer.generate_execution_plan()
        
        # With parallel tasks, factor should be > 1
        self.assertGreater(plan['parallelization_factor'], 1.0)
    
    def test_empty_tasks(self):
        """Test with empty task list"""
        analyzer = DependencyAnalyzer([])
        sorted_ids = analyzer.topological_sort()
        
        self.assertEqual(len(sorted_ids), 0)
    
    def test_single_task(self):
        """Test with single task"""
        single_task = [Task('T001', 'Only task', [])]
        analyzer = DependencyAnalyzer(single_task)
        
        sorted_ids = analyzer.topological_sort()
        self.assertEqual(len(sorted_ids), 1)
        self.assertEqual(sorted_ids[0], 'T001')
        
        parallel_groups = analyzer.find_parallel_tasks()
        self.assertEqual(len(parallel_groups), 1)
        self.assertEqual(len(parallel_groups[0]), 1)


class TestAnalyzeTaskDependencies(unittest.TestCase):
    """Test cases for analyze_task_dependencies function"""
    
    def test_analyze_valid_tasks(self):
        """Test analyzing valid task dependencies"""
        tasks = [
            Task('T001', 'First', []),
            Task('T002', 'Second', ['T001']),
        ]
        
        result = analyze_task_dependencies(tasks)
        
        self.assertIsInstance(result, dict)
        self.assertIn('has_circular_dependencies', result)
        self.assertIn('circular_dependencies', result)
        self.assertIn('execution_plan', result)
        
        self.assertFalse(result['has_circular_dependencies'])
        self.assertIsNotNone(result['execution_plan'])
    
    def test_analyze_circular_dependencies(self):
        """Test analyzing tasks with circular dependencies"""
        tasks = [
            Task('T001', 'A', ['T002']),
            Task('T002', 'B', ['T001']),
        ]
        
        result = analyze_task_dependencies(tasks)
        
        self.assertTrue(result['has_circular_dependencies'])
        self.assertTrue(len(result['circular_dependencies']) > 0)
        self.assertIsNone(result['execution_plan'])


if __name__ == '__main__':
    unittest.main()
