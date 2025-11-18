"""Integration tests for the complete instruction analysis pipeline."""

import unittest
import sys
import os
from io import StringIO
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from run_analysis import analyze_instruction_file, validate_pseudocode_file


class TestAnalyzeInstructionFile(unittest.TestCase):
    """Test the analyze command integration."""

    def setUp(self):
        """Set up test fixtures."""
        self.examples_dir = Path(__file__).parent.parent / "examples" / "inputs"
        self.user_auth_file = self.examples_dir / "sample_user_auth_instructions.md"
        self.api_file = self.examples_dir / "sample_api_instructions.md"
        self.data_pipeline_file = self.examples_dir / "sample_data_pipeline_instructions.md"

    def test_analyze_user_auth_file(self):
        """Test analyzing user authentication instructions."""
        self.assertTrue(self.user_auth_file.exists(), "User auth example file should exist")

        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            analyze_instruction_file(str(self.user_auth_file), verbose=False)
            output = captured_output.getvalue()

            # Verify key sections appear in output
            self.assertIn("Sections found:", output)
            self.assertIn("Tasks found:", output)
            self.assertIn("Questions found:", output)
            self.assertIn("Ambiguities found:", output)
            self.assertIn("DEPENDENCY ANALYSIS", output)

        finally:
            sys.stdout = sys.__stdout__

    def test_analyze_api_file(self):
        """Test analyzing API instructions."""
        self.assertTrue(self.api_file.exists(), "API example file should exist")

        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            analyze_instruction_file(str(self.api_file), verbose=False)
            output = captured_output.getvalue()

            # Verify analysis completed
            self.assertIn("Analyzing:", output)
            self.assertIn("DEPENDENCY ANALYSIS", output)

        finally:
            sys.stdout = sys.__stdout__

    def test_analyze_data_pipeline_file(self):
        """Test analyzing data pipeline instructions."""
        self.assertTrue(self.data_pipeline_file.exists(), "Data pipeline example file should exist")

        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            analyze_instruction_file(str(self.data_pipeline_file), verbose=False)
            output = captured_output.getvalue()

            # Verify analysis completed
            self.assertIn("Analyzing:", output)

        finally:
            sys.stdout = sys.__stdout__

    def test_analyze_verbose_mode(self):
        """Test analyzing with verbose mode enabled."""
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            analyze_instruction_file(str(self.user_auth_file), verbose=True)
            output = captured_output.getvalue()

            # Verbose mode should show more details
            self.assertIn("Analyzing:", output)

        finally:
            sys.stdout = sys.__stdout__

    def test_analyze_nonexistent_file(self):
        """Test analyzing a file that doesn't exist."""
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            analyze_instruction_file("nonexistent_file.md", verbose=False)
            output = captured_output.getvalue()

            # Should show error message
            self.assertIn("Error parsing file:", output)

        finally:
            sys.stdout = sys.__stdout__


class TestValidatePseudocodeFile(unittest.TestCase):
    """Test the validate command integration."""

    def setUp(self):
        """Set up test fixtures."""
        self.examples_dir = Path(__file__).parent.parent / "examples" / "outputs"
        self.pseudocode_file = self.examples_dir / "pseudocode_user_auth.md"

    def test_validate_pseudocode_file(self):
        """Test validating pseudocode file."""
        self.assertTrue(self.pseudocode_file.exists(), "Pseudocode example file should exist")

        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            validate_pseudocode_file(str(self.pseudocode_file))
            output = captured_output.getvalue()

            # Verify validation report appears
            self.assertIn("Pseudocode Validation Report", output)
            self.assertIn("Total Issues Found:", output)

        finally:
            sys.stdout = sys.__stdout__

    def test_validate_nonexistent_file(self):
        """Test validating a file that doesn't exist."""
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            validate_pseudocode_file("nonexistent_file.md")
            output = captured_output.getvalue()

            # Should show error message
            self.assertIn("Error reading file:", output)

        finally:
            sys.stdout = sys.__stdout__


class TestEndToEndPipeline(unittest.TestCase):
    """Test the complete analysis pipeline end-to-end."""

    def test_full_pipeline(self):
        """Test running the full analysis pipeline on an example."""
        examples_dir = Path(__file__).parent.parent / "examples" / "inputs"
        user_auth_file = examples_dir / "sample_user_auth_instructions.md"

        # Step 1: Analyze instruction file
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            analyze_instruction_file(str(user_auth_file), verbose=False)
            analysis_output = captured_output.getvalue()

            # Verify complete analysis pipeline
            self.assertIn("Sections found:", analysis_output)
            self.assertIn("Tasks found:", analysis_output)
            self.assertIn("DEPENDENCY ANALYSIS", analysis_output)
            self.assertIn("Execution Plan:", analysis_output)

            # Check for dependency analysis components
            self.assertTrue(
                "circular dependencies" in analysis_output.lower() or
                "no circular" in analysis_output.lower()
            )

        finally:
            sys.stdout = sys.__stdout__

    def test_pipeline_with_all_examples(self):
        """Test pipeline works with all example files."""
        examples_dir = Path(__file__).parent.parent / "examples" / "inputs"
        example_files = [
            "sample_user_auth_instructions.md",
            "sample_api_instructions.md",
            "sample_data_pipeline_instructions.md"
        ]

        for filename in example_files:
            filepath = examples_dir / filename

            with self.subTest(file=filename):
                self.assertTrue(filepath.exists(), f"{filename} should exist")

                # Capture stdout
                captured_output = StringIO()
                sys.stdout = captured_output

                try:
                    analyze_instruction_file(str(filepath), verbose=False)
                    output = captured_output.getvalue()

                    # Verify analysis completed without errors
                    self.assertIn("Analyzing:", output)
                    self.assertIn("DEPENDENCY ANALYSIS", output)

                finally:
                    sys.stdout = sys.__stdout__


if __name__ == "__main__":
    unittest.main()
