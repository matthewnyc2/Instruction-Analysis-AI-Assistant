"""
Markdown Parser for Instruction Analysis

This module provides functionality to parse markdown instruction files
and extract structured information for analysis.
"""

import re
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class Section:
    """Represents a section in a markdown document."""
    level: int
    title: str
    content: str
    line_number: int


@dataclass
class TaskStep:
    """Represents a task step extracted from markdown."""
    step_number: int
    description: str
    dependencies: List[str]
    is_parallel: bool


class MarkdownParser:
    """Parser for markdown instruction files."""
    
    def __init__(self, content: str):
        """
        Initialize the parser with markdown content.
        
        Args:
            content: The markdown content to parse
        """
        self.content = content
        self.lines = content.split('\n')
        
    def parse_sections(self) -> List[Section]:
        """
        Parse markdown into sections based on headers.
        
        Returns:
            List of Section objects
        """
        sections = []
        current_section = None
        current_content = []
        
        for line_num, line in enumerate(self.lines, 1):
            header_match = re.match(r'^(#{1,6})\s+(.+)$', line)
            
            if header_match:
                # Save previous section if exists
                if current_section:
                    current_section.content = '\n'.join(current_content).strip()
                    sections.append(current_section)
                
                # Start new section
                level = len(header_match.group(1))
                title = header_match.group(2).strip()
                current_section = Section(level, title, '', line_num)
                current_content = []
            elif current_section:
                current_content.append(line)
        
        # Add the last section
        if current_section:
            current_section.content = '\n'.join(current_content).strip()
            sections.append(current_section)
            
        return sections
    
    def extract_tasks(self) -> List[TaskStep]:
        """
        Extract task steps from markdown content.
        Looks for numbered lists, bullet points with task indicators.
        
        Returns:
            List of TaskStep objects
        """
        tasks = []
        
        # Pattern for numbered tasks
        numbered_pattern = r'^\s*(\d+)\.\s+(.+)$'
        # Pattern for task IDs like T001
        task_id_pattern = r'T\d{3,}'
        # Pattern for dependencies
        dependency_pattern = r'(?:depends on|requires|after|following).*?(T\d{3,}(?:,\s*T\d{3,})*)'
        
        for line in self.lines:
            numbered_match = re.match(numbered_pattern, line)
            
            if numbered_match:
                step_num = int(numbered_match.group(1))
                description = numbered_match.group(2).strip()
                
                # Check for dependencies in description
                deps = []
                dep_match = re.search(dependency_pattern, description, re.IGNORECASE)
                if dep_match:
                    dep_str = dep_match.group(1)
                    deps = re.findall(task_id_pattern, dep_str)
                
                # Check if marked as parallel
                is_parallel = 'parallel' in description.lower() or '||' in description
                
                task = TaskStep(step_num, description, deps, is_parallel)
                tasks.append(task)
        
        return tasks
    
    def extract_code_blocks(self) -> List[Dict[str, str]]:
        """
        Extract code blocks from markdown.
        
        Returns:
            List of dictionaries with 'language' and 'code' keys
        """
        code_blocks = []
        in_code_block = False
        current_block = {'language': '', 'code': []}
        
        for line in self.lines:
            if line.strip().startswith('```'):
                if not in_code_block:
                    # Starting code block
                    in_code_block = True
                    lang = line.strip()[3:].strip()
                    current_block = {'language': lang, 'code': []}
                else:
                    # Ending code block
                    in_code_block = False
                    current_block['code'] = '\n'.join(current_block['code'])
                    code_blocks.append(current_block)
                    current_block = {'language': '', 'code': []}
            elif in_code_block:
                current_block['code'].append(line)
        
        return code_blocks
    
    def extract_questions(self) -> List[str]:
        """
        Extract questions from the markdown (lines ending with ?).
        
        Returns:
            List of question strings
        """
        questions = []
        
        for line in self.lines:
            line = line.strip()
            if line.endswith('?'):
                # Remove list markers
                line = re.sub(r'^\s*[\-\*\d+\.]\s*', '', line)
                questions.append(line)
        
        return questions
    
    def find_ambiguities(self) -> List[Dict[str, any]]:
        """
        Identify potentially ambiguous statements.
        
        Returns:
            List of dictionaries with 'line', 'text', and 'reason' keys
        """
        ambiguities = []
        ambiguous_terms = [
            'maybe', 'perhaps', 'possibly', 'might', 'could',
            'some', 'few', 'several', 'various', 'etc',
            'and so on', 'or something', 'kind of', 'sort of'
        ]
        
        for line_num, line in enumerate(self.lines, 1):
            line_lower = line.lower()
            for term in ambiguous_terms:
                if term in line_lower:
                    ambiguities.append({
                        'line': line_num,
                        'text': line.strip(),
                        'reason': f'Contains ambiguous term: "{term}"'
                    })
                    break
        
        return ambiguities


def parse_instruction_file(filepath: str) -> Dict:
    """
    Parse an instruction markdown file and return structured data.
    
    Args:
        filepath: Path to the markdown file
        
    Returns:
        Dictionary containing parsed data
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    parser = MarkdownParser(content)
    
    return {
        'sections': parser.parse_sections(),
        'tasks': parser.extract_tasks(),
        'code_blocks': parser.extract_code_blocks(),
        'questions': parser.extract_questions(),
        'ambiguities': parser.find_ambiguities()
    }


if __name__ == '__main__':
    # Example usage
    sample_md = """
# Project Setup

1. Install dependencies
2. Configure environment (depends on T001)
3. Run tests || parallel task

## Questions
- What version of Python?
- Should we use Docker?

Maybe we should add logging?
"""
    
    parser = MarkdownParser(sample_md)
    print("Sections:", len(parser.parse_sections()))
    print("Tasks:", len(parser.extract_tasks()))
    print("Questions:", len(parser.extract_questions()))
    print("Ambiguities:", len(parser.find_ambiguities()))
