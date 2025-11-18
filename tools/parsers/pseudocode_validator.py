"""
Pseudocode Validator

This module validates pseudocode for determinism, logic errors,
and big-picture issues.
"""

import re
from typing import List, Dict, Set
from dataclasses import dataclass
from enum import Enum


class IssueLevel(Enum):
    """Severity levels for detected issues."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class ValidationIssue:
    """Represents a validation issue found in pseudocode."""
    level: IssueLevel
    category: str
    message: str
    line_number: int
    suggestion: str = ""


class PseudocodeValidator:
    """Validates pseudocode for various issues."""
    
    # Keywords that may indicate non-deterministic operations
    NON_DETERMINISTIC_PATTERNS = [
        r'\brandom\b',
        r'\brand\b',
        r'\bcurrent[_\s]time\b',
        r'\bnow\(\)',
        r'\btoday\(\)',
        r'\btimestamp\b',
        r'\buuid\b',
        r'\bguid\b',
    ]
    
    # Patterns that may indicate logic errors
    LOGIC_ERROR_PATTERNS = [
        (r'for\s+\w+\s*=\s*(\d+)\s+to\s+(\d+)', 'off_by_one'),
        (r'while\s+true', 'infinite_loop_risk'),
        (r'if\s+\w+\s*==\s*true', 'redundant_comparison'),
        (r'if\s+.*=(?!=)', 'assignment_in_condition'),
    ]
    
    def __init__(self, pseudocode: str):
        """
        Initialize validator with pseudocode.
        
        Args:
            pseudocode: The pseudocode to validate
        """
        self.pseudocode = pseudocode
        self.lines = pseudocode.split('\n')
        self.issues: List[ValidationIssue] = []
    
    def validate_determinism(self) -> List[ValidationIssue]:
        """
        Check for non-deterministic operations.
        
        Returns:
            List of ValidationIssue objects
        """
        issues = []
        
        for line_num, line in enumerate(self.lines, 1):
            line_lower = line.lower()
            
            for pattern in self.NON_DETERMINISTIC_PATTERNS:
                if re.search(pattern, line_lower):
                    issues.append(ValidationIssue(
                        level=IssueLevel.WARNING,
                        category="Non-Deterministic",
                        message=f"Potential non-deterministic operation detected: {pattern}",
                        line_number=line_num,
                        suggestion="Consider using a seeded random generator, fixed timestamp, or parameterized input"
                    ))
        
        return issues
    
    def validate_logic(self) -> List[ValidationIssue]:
        """
        Check for common logic errors.
        
        Returns:
            List of ValidationIssue objects
        """
        issues = []
        
        for line_num, line in enumerate(self.lines, 1):
            line_lower = line.lower()
            
            for pattern, error_type in self.LOGIC_ERROR_PATTERNS:
                match = re.search(pattern, line_lower)
                if match:
                    message = ""
                    suggestion = ""
                    
                    if error_type == 'off_by_one':
                        message = "Potential off-by-one error in loop"
                        suggestion = "Verify loop bounds are correct (inclusive vs exclusive)"
                    elif error_type == 'infinite_loop_risk':
                        message = "Infinite loop detected - ensure there's a break condition"
                        suggestion = "Add explicit break condition or use bounded loop"
                    elif error_type == 'redundant_comparison':
                        message = "Redundant comparison with boolean"
                        suggestion = "Use variable directly: IF variable THEN"
                    elif error_type == 'assignment_in_condition':
                        message = "Assignment operator (=) used instead of comparison (==)"
                        suggestion = "Use == for comparison, = for assignment"
                    
                    issues.append(ValidationIssue(
                        level=IssueLevel.ERROR,
                        category="Logic Error",
                        message=message,
                        line_number=line_num,
                        suggestion=suggestion
                    ))
        
        return issues
    
    def validate_error_handling(self) -> List[ValidationIssue]:
        """
        Check if error handling is present.
        
        Returns:
            List of ValidationIssue objects
        """
        issues = []
        
        has_try_catch = any(
            re.search(r'\b(try|catch|throw|error|exception)\b', line, re.IGNORECASE)
            for line in self.lines
        )
        
        has_null_checks = any(
            re.search(r'\bis\s+null\b|\bnull\s+check\b|if\s+not\s+\w+', line, re.IGNORECASE)
            for line in self.lines
        )
        
        if not has_try_catch and len(self.lines) > 10:
            issues.append(ValidationIssue(
                level=IssueLevel.WARNING,
                category="Error Handling",
                message="No error handling detected",
                line_number=0,
                suggestion="Consider adding try-catch blocks for error handling"
            ))
        
        if not has_null_checks:
            issues.append(ValidationIssue(
                level=IssueLevel.INFO,
                category="Error Handling",
                message="No null checks detected",
                line_number=0,
                suggestion="Consider adding null/undefined checks for inputs"
            ))
        
        return issues
    
    def validate_resource_cleanup(self) -> List[ValidationIssue]:
        """
        Check if resources are properly cleaned up.
        
        Returns:
            List of ValidationIssue objects
        """
        issues = []
        
        # Look for open/allocate patterns
        opens = []
        closes = []
        
        for line_num, line in enumerate(self.lines, 1):
            line_lower = line.lower()
            
            if re.search(r'\b(open|allocate|create|connect|acquire)\b', line_lower):
                opens.append(line_num)
            
            if re.search(r'\b(close|free|delete|disconnect|release|cleanup)\b', line_lower):
                closes.append(line_num)
        
        if opens and not closes:
            issues.append(ValidationIssue(
                level=IssueLevel.WARNING,
                category="Resource Management",
                message="Resources are opened/allocated but not explicitly closed/freed",
                line_number=opens[0],
                suggestion="Add cleanup code to close/free resources"
            ))
        
        return issues
    
    def validate_variable_initialization(self) -> List[ValidationIssue]:
        """
        Check if variables are initialized before use.
        
        Returns:
            List of ValidationIssue objects
        """
        issues = []
        declared_vars: Set[str] = set()
        
        for line_num, line in enumerate(self.lines, 1):
            # Find variable declarations
            decl_match = re.search(r'\b(declare|let|var|set)\s+(\w+)', line, re.IGNORECASE)
            if decl_match:
                declared_vars.add(decl_match.group(2).lower())
            
            # Find variable usage (simple heuristic)
            # Look for variables used in expressions but not on left side of assignment
            if '=' in line:
                parts = line.split('=')
                if len(parts) >= 2:
                    # Right side of assignment
                    right_side = parts[1]
                    words = re.findall(r'\b[a-z_]\w*\b', right_side, re.IGNORECASE)
                    for word in words:
                        if word.lower() not in declared_vars and word.lower() not in ['true', 'false', 'null', 'none']:
                            issues.append(ValidationIssue(
                                level=IssueLevel.WARNING,
                                category="Variable Usage",
                                message=f"Variable '{word}' may be used before declaration",
                                line_number=line_num,
                                suggestion=f"Ensure '{word}' is declared before use"
                            ))
        
        return issues
    
    def validate_complexity(self) -> List[ValidationIssue]:
        """
        Analyze code complexity.
        
        Returns:
            List of ValidationIssue objects
        """
        issues = []
        
        # Count nesting depth
        max_nesting = 0
        current_nesting = 0
        nesting_line = 0
        
        for line_num, line in enumerate(self.lines, 1):
            line_stripped = line.strip().lower()
            
            if any(keyword in line_stripped for keyword in ['if', 'for', 'while', 'loop', 'function']):
                current_nesting += 1
                if current_nesting > max_nesting:
                    max_nesting = current_nesting
                    nesting_line = line_num
            
            if any(keyword in line_stripped for keyword in ['end', 'endif', 'endfor', 'endwhile']):
                current_nesting = max(0, current_nesting - 1)
        
        if max_nesting > 4:
            issues.append(ValidationIssue(
                level=IssueLevel.WARNING,
                category="Complexity",
                message=f"High nesting depth detected: {max_nesting} levels",
                line_number=nesting_line,
                suggestion="Consider refactoring into separate functions to reduce complexity"
            ))
        
        # Count lines of code
        code_lines = [line for line in self.lines if line.strip() and not line.strip().startswith('//')]
        if len(code_lines) > 100:
            issues.append(ValidationIssue(
                level=IssueLevel.INFO,
                category="Complexity",
                message=f"Long code block: {len(code_lines)} lines",
                line_number=0,
                suggestion="Consider breaking into smaller functions"
            ))
        
        return issues
    
    def validate_all(self) -> Dict[str, List[ValidationIssue]]:
        """
        Run all validation checks.
        
        Returns:
            Dictionary mapping category to list of issues
        """
        all_issues = []
        
        all_issues.extend(self.validate_determinism())
        all_issues.extend(self.validate_logic())
        all_issues.extend(self.validate_error_handling())
        all_issues.extend(self.validate_resource_cleanup())
        all_issues.extend(self.validate_variable_initialization())
        all_issues.extend(self.validate_complexity())
        
        # Group by category
        by_category = {}
        for issue in all_issues:
            if issue.category not in by_category:
                by_category[issue.category] = []
            by_category[issue.category].append(issue)
        
        return by_category
    
    def generate_report(self) -> str:
        """
        Generate a human-readable validation report.
        
        Returns:
            Formatted report string
        """
        results = self.validate_all()
        
        if not results:
            return "✓ No issues found. Pseudocode looks good!"
        
        report_lines = ["# Pseudocode Validation Report\n"]
        
        # Summary
        total_issues = sum(len(issues) for issues in results.values())
        by_level = {level: 0 for level in IssueLevel}
        for issues in results.values():
            for issue in issues:
                by_level[issue.level] += 1
        
        report_lines.append(f"**Total Issues Found:** {total_issues}\n")
        report_lines.append(f"- Critical: {by_level[IssueLevel.CRITICAL]}")
        report_lines.append(f"- Errors: {by_level[IssueLevel.ERROR]}")
        report_lines.append(f"- Warnings: {by_level[IssueLevel.WARNING]}")
        report_lines.append(f"- Info: {by_level[IssueLevel.INFO]}\n")
        
        # Detailed issues by category
        for category, issues in sorted(results.items()):
            report_lines.append(f"\n## {category}\n")
            for issue in issues:
                level_emoji = {
                    IssueLevel.CRITICAL: "🔴",
                    IssueLevel.ERROR: "❌",
                    IssueLevel.WARNING: "⚠️",
                    IssueLevel.INFO: "ℹ️"
                }
                emoji = level_emoji.get(issue.level, "•")
                
                line_str = f" (Line {issue.line_number})" if issue.line_number > 0 else ""
                report_lines.append(f"{emoji} **{issue.level.value.upper()}**{line_str}: {issue.message}")
                if issue.suggestion:
                    report_lines.append(f"  *Suggestion:* {issue.suggestion}")
                report_lines.append("")
        
        return "\n".join(report_lines)


def validate_pseudocode(pseudocode: str) -> Dict:
    """
    Validate pseudocode and return results.
    
    Args:
        pseudocode: The pseudocode string to validate
        
    Returns:
        Dictionary containing validation results and report
    """
    validator = PseudocodeValidator(pseudocode)
    issues_by_category = validator.validate_all()
    report = validator.generate_report()
    
    return {
        'issues': issues_by_category,
        'report': report,
        'total_issues': sum(len(issues) for issues in issues_by_category.values())
    }


if __name__ == '__main__':
    # Example usage
    sample_pseudocode = """
FUNCTION process_data(input)
    result = calculate(input)
    random_value = random()
    WHILE true
        DO something
    END WHILE
    RETURN result
END FUNCTION
"""
    
    result = validate_pseudocode(sample_pseudocode)
    print(result['report'])
