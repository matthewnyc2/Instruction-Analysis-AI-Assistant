"""
Unit tests for markdown_parser module
"""

import unittest
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.parsers.markdown_parser import MarkdownParser, parse_instruction_file, Section, TaskStep


class TestMarkdownParser(unittest.TestCase):
    """Test cases for MarkdownParser class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.sample_markdown = """# Main Title

This is the introduction.

## Section 1

Some content here.

### Subsection 1.1

Detailed content.

## Section 2

1. First task
2. Second task (depends on T001)
3. Third task || parallel

## Questions

- What version should we use?
- Should we add logging?

Maybe we should implement caching?
"""
        self.parser = MarkdownParser(self.sample_markdown)
    
    def test_parse_sections(self):
        """Test parsing markdown into sections"""
        sections = self.parser.parse_sections()
        
        self.assertIsInstance(sections, list)
        self.assertTrue(len(sections) > 0)
        
        # Check first section
        self.assertEqual(sections[0].level, 1)
        self.assertEqual(sections[0].title, "Main Title")
        self.assertIn("introduction", sections[0].content)
    
    def test_parse_sections_levels(self):
        """Test parsing different header levels"""
        sections = self.parser.parse_sections()
        
        # Find sections with different levels
        level_1 = [s for s in sections if s.level == 1]
        level_2 = [s for s in sections if s.level == 2]
        level_3 = [s for s in sections if s.level == 3]
        
        self.assertTrue(len(level_1) > 0)
        self.assertTrue(len(level_2) > 0)
        self.assertTrue(len(level_3) > 0)
    
    def test_extract_tasks(self):
        """Test extracting task steps"""
        tasks = self.parser.extract_tasks()
        
        self.assertIsInstance(tasks, list)
        self.assertEqual(len(tasks), 3)
        
        # Check first task
        self.assertEqual(tasks[0].step_number, 1)
        self.assertIn("First task", tasks[0].description)
        self.assertEqual(len(tasks[0].dependencies), 0)
        self.assertFalse(tasks[0].is_parallel)
    
    def test_extract_tasks_with_dependencies(self):
        """Test extracting tasks with dependencies"""
        tasks = self.parser.extract_tasks()
        
        # Second task should have dependency
        task_2 = next(t for t in tasks if t.step_number == 2)
        self.assertTrue(len(task_2.dependencies) > 0)
        self.assertIn("T001", task_2.dependencies)
    
    def test_extract_tasks_parallel(self):
        """Test identifying parallel tasks"""
        tasks = self.parser.extract_tasks()
        
        # Third task should be marked as parallel
        task_3 = next(t for t in tasks if t.step_number == 3)
        self.assertTrue(task_3.is_parallel)
    
    def test_extract_code_blocks(self):
        """Test extracting code blocks"""
        md_with_code = """
# Example

```python
def hello():
    print("world")
```

```javascript
console.log("test");
```
"""
        parser = MarkdownParser(md_with_code)
        code_blocks = parser.extract_code_blocks()
        
        self.assertEqual(len(code_blocks), 2)
        self.assertEqual(code_blocks[0]['language'], 'python')
        self.assertIn('def hello', code_blocks[0]['code'])
        self.assertEqual(code_blocks[1]['language'], 'javascript')
    
    def test_extract_questions(self):
        """Test extracting questions"""
        questions = self.parser.extract_questions()
        
        self.assertIsInstance(questions, list)
        self.assertTrue(len(questions) >= 2)
        self.assertTrue(any("version" in q.lower() for q in questions))
        self.assertTrue(any("logging" in q.lower() for q in questions))
    
    def test_find_ambiguities(self):
        """Test finding ambiguous statements"""
        ambiguities = self.parser.find_ambiguities()
        
        self.assertIsInstance(ambiguities, list)
        self.assertTrue(len(ambiguities) > 0)
        
        # Should find "maybe"
        maybe_found = any("maybe" in a['reason'].lower() for a in ambiguities)
        self.assertTrue(maybe_found)
    
    def test_empty_markdown(self):
        """Test parsing empty markdown"""
        parser = MarkdownParser("")
        sections = parser.parse_sections()
        tasks = parser.extract_tasks()
        
        self.assertEqual(len(sections), 0)
        self.assertEqual(len(tasks), 0)
    
    def test_markdown_without_headers(self):
        """Test markdown without headers"""
        parser = MarkdownParser("Just some plain text without headers.")
        sections = parser.parse_sections()
        
        self.assertEqual(len(sections), 0)


class TestParseInstructionFile(unittest.TestCase):
    """Test cases for parse_instruction_file function"""
    
    def setUp(self):
        """Set up test file"""
        self.test_file = '/tmp/test_instruction.md'
        with open(self.test_file, 'w') as f:
            f.write("""# Test Instruction

1. First task
2. Second task

## Questions
- What database to use?
""")
    
    def tearDown(self):
        """Clean up test file"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_parse_file(self):
        """Test parsing a file"""
        result = parse_instruction_file(self.test_file)
        
        self.assertIsInstance(result, dict)
        self.assertIn('sections', result)
        self.assertIn('tasks', result)
        self.assertIn('code_blocks', result)
        self.assertIn('questions', result)
        self.assertIn('ambiguities', result)
        
        self.assertTrue(len(result['sections']) > 0)
        self.assertTrue(len(result['tasks']) > 0)
        self.assertTrue(len(result['questions']) > 0)


if __name__ == '__main__':
    unittest.main()
