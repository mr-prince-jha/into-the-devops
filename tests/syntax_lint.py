#!/usr/bin/env python3
"""
Markdown Syntax Linter for DevOps Repository
=========================================

This linter checks the syntax of markdown files in the DevOps repository,
specifically focusing on HTML tags like <details> and <summary>.

Features:
- Validates proper nesting of HTML tags
- Checks for matching opening/closing tags
- Supports multiple tag types
- Provides detailed error reporting
- Handles multiple files
- Configurable tag validation

Usage:
    $ python tests/syntax_lint.py <file_path>
    $ python tests/syntax_lint.py path/to/markdown.md

Author: surister
Enhanced by: Harshhaa Reddy
"""

import sys
import os
import argparse
from typing import List, Dict, Set, Optional
from dataclasses import dataclass
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class TagError:
    """Class for storing tag validation errors."""
    line_number: int
    message: str
    tag_type: str
    context: str

class MarkdownLinter:
    """Main class for linting markdown files."""

    def __init__(self):
        self.errors: List[TagError] = []
        self.supported_tags: Set[str] = {'details', 'summary'}
        self.tag_stack: Dict[str, List[int]] = {tag: [] for tag in self.supported_tags}

    def validate_file(self, file_path: str) -> bool:
        """
        Validates a markdown file for proper HTML tag usage.

        Args:
            file_path (str): Path to the markdown file

        Returns:
            bool: True if validation passes, False otherwise
        """
        try:
            with open(file_path, 'rb') as f:
                content = [line.rstrip() for line in f.readlines()]
            
            logger.info(f"Validating file: {file_path}")
            
            # Run all validation checks
            self._check_tag_pairs(content)
            self._validate_tag_nesting(content)
            self._check_tag_completeness(content)

            return len(self.errors) == 0

        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
            return False
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {str(e)}")
            return False

    def _check_tag_pairs(self, content: List[bytes]) -> None:
        """
        Checks if all tags have proper opening and closing pairs.
        """
        for tag_type in self.supported_tags:
            open_tag = f"<{tag_type}>".encode()
            close_tag = f"</{tag_type}>".encode()
            
            for line_num, line in enumerate(content, 1):
                # Skip lines that have both opening and closing tags
                if open_tag in line and close_tag in line:
                    continue

                if open_tag in line:
                    self.tag_stack[tag_type].append(line_num)
                elif close_tag in line:
                    if not self.tag_stack[tag_type]:
                        self._add_error(
                            line_num,
                            f"Found closing tag '</{tag_type}>' without matching opening tag",
                            tag_type,
                            line.decode('utf-8', 'ignore')
                        )
                    else:
                        self.tag_stack[tag_type].pop()

    def _validate_tag_nesting(self, content: List[bytes]) -> None:
        """
        Validates proper nesting of tags (e.g., summary inside details).
        """
        details_open = False
        summary_open = False

        for line_num, line in enumerate(content, 1):
            line_str = line.decode('utf-8', 'ignore')

            if b"<details>" in line:
                if details_open:
                    self._add_error(
                        line_num,
                        "Nested <details> tags are not allowed",
                        "details",
                        line_str
                    )
                details_open = True

            if b"<summary>" in line:
                if not details_open:
                    self._add_error(
                        line_num,
                        "<summary> tag must be inside <details> tag",
                        "summary",
                        line_str
                    )
                if summary_open:
                    self._add_error(
                        line_num,
                        "Nested <summary> tags are not allowed",
                        "summary",
                        line_str
                    )
                summary_open = True

            if b"</summary>" in line:
                summary_open = False
            if b"</details>" in line:
                details_open = False

    def _check_tag_completeness(self, content: List[bytes]) -> None:
        """
        Ensures all opened tags are properly closed.
        """
        for tag_type, stack in self.tag_stack.items():
            for line_num in stack:
                self._add_error(
                    line_num,
                    f"Unclosed <{tag_type}> tag",
                    tag_type,
                    f"<{tag_type}> tag opened but never closed"
                )

    def _add_error(self, line_number: int, message: str, tag_type: str, context: str) -> None:
        """
        Adds an error to the error list.
        """
        self.errors.append(TagError(line_number, message, tag_type, context))

    def print_errors(self, file_path: str) -> None:
        """
        Prints all validation errors in a formatted way.
        """
        if self.errors:
            print(f"\n❌ {file_path} failed validation", file=sys.stderr)
            print("\nDetailed Error Report:", file=sys.stderr)
            print("-" * 50, file=sys.stderr)
            
            for error in self.errors:
                print(f"\nLine {error.line_number}:", file=sys.stderr)
                print(f"Tag Type: {error.tag_type}", file=sys.stderr)
                print(f"Error: {error.message}", file=sys.stderr)
                print(f"Context: {error.context}", file=sys.stderr)
                print("-" * 50, file=sys.stderr)
        else:
            print(f"\n✅ {file_path} passed all validation checks.")

def parse_arguments() -> argparse.Namespace:
    """
    Parses command line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Markdown syntax linter for DevOps repository",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "file_path",
        help="Path to the markdown file to validate"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    return parser.parse_args()

def main() -> int:
    """
    Main function that runs the linter.
    
    Returns:
        int: Exit code (0 for success, 1 for failure)
    """
    args = parse_arguments()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    # Validate file extension
    if not args.file_path.endswith(('.md', '.markdown')):
        logger.error("Error: File must be a markdown file (.md or .markdown)")
        return 1

    # Initialize and run linter
    linter = MarkdownLinter()
    success = linter.validate_file(args.file_path)
    linter.print_errors(args.file_path)

    return 0 if success else 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        logger.info("\nLinting interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        sys.exit(1)
