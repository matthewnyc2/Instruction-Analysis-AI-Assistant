.PHONY: help install test test-verbose clean build lint

help:
	@echo "Instruction Analysis AI Assistant - Development Commands"
	@echo ""
	@echo "Available commands:"
	@echo "  make install       Install the package in development mode"
	@echo "  make test          Run all tests"
	@echo "  make test-verbose  Run tests with verbose output"
	@echo "  make lint          Check Python syntax"
	@echo "  make clean         Remove build artifacts and cache files"
	@echo "  make build         Build distribution packages"
	@echo ""

install:
	python -m pip install -e .

test:
	python -m unittest discover -s tests

test-verbose:
	python -m unittest discover -s tests -v

lint:
	python -m py_compile run_analysis.py
	python -m py_compile tools/parsers/markdown_parser.py
	python -m py_compile tools/parsers/dependency_analyzer.py
	python -m py_compile tools/parsers/pseudocode_validator.py
	@echo "✓ All Python files have valid syntax"

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	@echo "✓ Cleaned build artifacts and cache files"

build:
	python -m pip install --upgrade build
	python -m build
	@echo "✓ Package built successfully"
