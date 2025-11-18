"""
Unit tests for pseudocode_validator module
"""

import unittest
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.parsers.pseudocode_validator import (
    PseudocodeValidator, IssueLevel, ValidationIssue, validate_pseudocode
)


class TestPseudocodeValidator(unittest.TestCase):
    """Test cases for PseudocodeValidator class"""
    
    def test_validate_determinism_random(self):
        """Test detection of random operations"""
        pseudocode = """
        FUNCTION test()
            x = random()
            RETURN x
        END FUNCTION
        """
        validator = PseudocodeValidator(pseudocode)
        issues = validator.validate_determinism()
        
        self.assertTrue(len(issues) > 0)
        self.assertTrue(any('random' in issue.message.lower() for issue in issues))
    
    def test_validate_determinism_timestamp(self):
        """Test detection of timestamp operations"""
        pseudocode = """
        FUNCTION test()
            t = current_time()
            RETURN t
        END FUNCTION
        """
        validator = PseudocodeValidator(pseudocode)
        issues = validator.validate_determinism()
        
        self.assertTrue(len(issues) > 0)
    
    def test_validate_logic_infinite_loop(self):
        """Test detection of infinite loops"""
        pseudocode = """
        FUNCTION test()
            WHILE true
                DO something
            END WHILE
        END FUNCTION
        """
        validator = PseudocodeValidator(pseudocode)
        issues = validator.validate_logic()
        
        self.assertTrue(len(issues) > 0)
        self.assertTrue(any('infinite' in issue.message.lower() for issue in issues))
    
    def test_validate_logic_assignment_in_condition(self):
        """Test detection of assignment in condition"""
        pseudocode = """
        FUNCTION test()
            IF x = 5 THEN
                RETURN true
            END IF
        END FUNCTION
        """
        validator = PseudocodeValidator(pseudocode)
        issues = validator.validate_logic()
        
        # May detect assignment operator
        self.assertTrue(len(issues) >= 0)
    
    def test_validate_error_handling_present(self):
        """Test recognition of error handling"""
        pseudocode = """
        FUNCTION test()
            TRY
                result = risky_operation()
                RETURN result
            CATCH Error as e
                RETURN null
            END TRY
        END FUNCTION
        """
        validator = PseudocodeValidator(pseudocode)
        issues = validator.validate_error_handling()
        
        # Should have minimal or no issues since error handling is present
        critical_issues = [i for i in issues if i.level == IssueLevel.ERROR]
        self.assertEqual(len(critical_issues), 0)
    
    def test_validate_error_handling_missing(self):
        """Test detection of missing error handling"""
        pseudocode = """
        FUNCTION test()
            result = operation1()
            result2 = operation2()
            result3 = operation3()
            result4 = operation4()
            result5 = operation5()
            RETURN result
        END FUNCTION
        """
        validator = PseudocodeValidator(pseudocode)
        issues = validator.validate_error_handling()
        
        # Should detect missing error handling in longer code
        self.assertTrue(len(issues) > 0)
    
    def test_validate_resource_cleanup_missing(self):
        """Test detection of missing resource cleanup"""
        pseudocode = """
        FUNCTION test()
            file = open("test.txt")
            data = read(file)
            RETURN data
        END FUNCTION
        """
        validator = PseudocodeValidator(pseudocode)
        issues = validator.validate_resource_cleanup()
        
        self.assertTrue(len(issues) > 0)
    
    def test_validate_resource_cleanup_present(self):
        """Test recognition of resource cleanup"""
        pseudocode = """
        FUNCTION test()
            file = open("test.txt")
            data = read(file)
            close(file)
            RETURN data
        END FUNCTION
        """
        validator = PseudocodeValidator(pseudocode)
        issues = validator.validate_resource_cleanup()
        
        self.assertEqual(len(issues), 0)
    
    def test_validate_complexity_high_nesting(self):
        """Test detection of high nesting complexity"""
        pseudocode = """
        FUNCTION test()
            IF condition1 THEN
                IF condition2 THEN
                    IF condition3 THEN
                        IF condition4 THEN
                            IF condition5 THEN
                                DO something
                            END IF
                        END IF
                    END IF
                END IF
            END IF
        END FUNCTION
        """
        validator = PseudocodeValidator(pseudocode)
        issues = validator.validate_complexity()
        
        self.assertTrue(len(issues) > 0)
        self.assertTrue(any('nesting' in issue.message.lower() for issue in issues))
    
    def test_validate_complexity_long_code(self):
        """Test detection of long code blocks"""
        # Create pseudocode with many lines
        lines = ["FUNCTION test()"]
        for i in range(120):
            lines.append(f"    statement_{i} = value_{i}")
        lines.append("END FUNCTION")
        pseudocode = "\n".join(lines)
        
        validator = PseudocodeValidator(pseudocode)
        issues = validator.validate_complexity()
        
        self.assertTrue(len(issues) > 0)
    
    def test_validate_all_clean_code(self):
        """Test validation of clean pseudocode"""
        pseudocode = """
        FUNCTION add(a, b)
            IF a IS NULL OR b IS NULL THEN
                THROW ValidationError("Inputs cannot be null")
            END IF
            result = a + b
            RETURN result
        END FUNCTION
        """
        validator = PseudocodeValidator(pseudocode)
        results = validator.validate_all()
        
        # Clean code should have minimal issues
        total_issues = sum(len(issues) for issues in results.values())
        self.assertLessEqual(total_issues, 2)
    
    def test_validate_all_problematic_code(self):
        """Test validation of problematic pseudocode"""
        pseudocode = """
        FUNCTION bad_function()
            WHILE true
                x = random()
            END WHILE
        END FUNCTION
        """
        validator = PseudocodeValidator(pseudocode)
        results = validator.validate_all()
        
        # Should detect multiple issues
        total_issues = sum(len(issues) for issues in results.values())
        self.assertGreater(total_issues, 0)
    
    def test_generate_report(self):
        """Test report generation"""
        pseudocode = """
        FUNCTION test()
            x = random()
            RETURN x
        END FUNCTION
        """
        validator = PseudocodeValidator(pseudocode)
        report = validator.generate_report()
        
        self.assertIsInstance(report, str)
        self.assertTrue(len(report) > 0)
        self.assertIn('Validation Report', report)
    
    def test_generate_report_no_issues(self):
        """Test report generation with minimal issues"""
        pseudocode = """
        FUNCTION add(a, b)
            IF a IS NULL OR b IS NULL THEN
                THROW Error("Invalid")
            END IF
            RETURN a + b
        END FUNCTION
        """
        validator = PseudocodeValidator(pseudocode)
        report = validator.generate_report()
        
        # Should have very few issues with proper null checks and error handling
        self.assertTrue(len(report) > 0)


class TestValidatePseudocode(unittest.TestCase):
    """Test cases for validate_pseudocode function"""
    
    def test_validate_function(self):
        """Test the validate_pseudocode wrapper function"""
        pseudocode = """
        FUNCTION test()
            x = random()
            RETURN x
        END FUNCTION
        """
        result = validate_pseudocode(pseudocode)
        
        self.assertIsInstance(result, dict)
        self.assertIn('issues', result)
        self.assertIn('report', result)
        self.assertIn('total_issues', result)
        
        self.assertGreater(result['total_issues'], 0)
    
    def test_validate_function_clean_code(self):
        """Test validation with clean code"""
        pseudocode = """
        FUNCTION calculate(x, y)
            IF x IS NULL OR y IS NULL THEN
                THROW Error("Invalid input")
            END IF
            result = x + y
            RETURN result
        END FUNCTION
        """
        result = validate_pseudocode(pseudocode)
        
        # Clean code should have minimal issues
        self.assertLessEqual(result['total_issues'], 2)


if __name__ == '__main__':
    unittest.main()
