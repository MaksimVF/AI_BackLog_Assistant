


"""
Document Schema Generator module for analyzing and structuring document content.
This module automatically identifies and categorizes document sections, headers, tables,
lists, and paragraphs to create a hierarchical document structure.
"""

import re
from typing import List, Dict, Union, Optional
import logging

# Set up logger
logger = logging.getLogger(__name__)

class DocumentSchemaGenerator:
    """
    Generates a structured schema from document text by identifying and categorizing
    different content blocks such as headers, paragraphs, tables, and lists.
    """

    # Regex patterns for different block types
    # Enhanced header patterns for better detection
    header_pattern = re.compile(
        r"^(?:\d+(\.\d+)*\s+)?[А-ЯA-Z][\w\s\-]{1,50}$",
        re.MULTILINE
    )
    # More comprehensive list detection
    list_pattern = re.compile(r"^\s*[-\*\d\.\)]\s+")
    # Enhanced table detection (Markdown, ASCII, and simple grid tables)
    table_pattern = re.compile(r"\||\+[-+]+\+")
    # Roman numeral sections and other section markers
    section_pattern = re.compile(r"^\s*[IVXLC]+(\.[IVXLC]+)*\s+")
    # Additional patterns for better document structure detection
    metadata_pattern = re.compile(r"^(?:Дата|Date|Автор|Author|Версия|Version):", re.IGNORECASE)
    footer_pattern = re.compile(r"^(?:Страница|Page|©|Copyright)\s+", re.IGNORECASE)

    def __init__(self):
        """
        Initialize the document schema generator.
        """
        # Custom patterns can be added for specific document types
        self.custom_patterns = {}

        # Enhanced table detection patterns
        self.table_start_patterns = [
            re.compile(r"^\s*\|"),  # Markdown table with leading pipe
            re.compile(r"^\s*\+\-+"),  # ASCII table border
            re.compile(r"^\s*\d+\s+[^\d]"),  # Number followed by non-digit (simple table)
        ]

        # Metadata extraction patterns
        self.metadata_extractors = {
            "date": re.compile(r"\b(?:Дата|Date):\s*(.*)", re.IGNORECASE),
            "author": re.compile(r"\b(?:Автор|Author):\s*(.*)", re.IGNORECASE),
            "version": re.compile(r"\b(?:Версия|Version):\s*(.*)", re.IGNORECASE),
        }

    def add_custom_pattern(self, pattern_name: str, pattern: str) -> None:
        """
        Add a custom regex pattern for specific document structures.

        Args:
            pattern_name: Name of the pattern (e.g., 'custom_header')
            pattern: Regex pattern string
        """
        try:
            compiled_pattern = re.compile(pattern)
            self.custom_patterns[pattern_name] = compiled_pattern
            logger.info(f"Added custom pattern: {pattern_name}")
        except re.error as e:
            logger.error(f"Invalid regex pattern: {e}")

    def generate_schema(self, text: str) -> List[Dict[str, Union[str, List]]]:
        """
        Parse text and return a list of content blocks with types and content.

        Args:
            text: Input document text

        Returns:
            List of document blocks with structure information
        """
        if not text or not isinstance(text, str):
            return []

        lines = text.splitlines()
        schema = []
        buffer = []
        current_block_type = None

        def flush_block():
            """Helper function to finalize and add a block to the schema."""
            nonlocal buffer, current_block_type
            if buffer:
                content = "\n".join(buffer).strip()
                if content:  # Only add non-empty blocks
                    schema.append({
                        "type": current_block_type,
                        "content": content,
                        "start_line": max(0, len(lines) - len(buffer)),
                        "end_line": len(lines) - 1
                    })
                buffer = []

        for i, line in enumerate(lines):
            line_strip = line.strip()

            # Skip empty lines (they'll be used as block separators)
            if not line_strip:
                flush_block()
                current_block_type = None
                continue

            # Check for metadata (date, author, version)
            if self.metadata_pattern.match(line_strip):
                flush_block()
                current_block_type = "metadata"
                buffer.append(line_strip)
                flush_block()
                current_block_type = None
                continue

            # Check for footers/page numbers
            if self.footer_pattern.match(line_strip):
                flush_block()
                current_block_type = "footer"
                buffer.append(line_strip)
                flush_block()
                current_block_type = None
                continue

            # Check for headers
            if self.header_pattern.match(line_strip):
                flush_block()
                current_block_type = "header"
                buffer.append(line_strip)
                flush_block()
                current_block_type = None
                continue

            # Check for tables (enhanced detection)
            if self.table_pattern.search(line_strip):
                if current_block_type != "table":
                    flush_block()
                    current_block_type = "table"
                buffer.append(line_strip)
                continue

            # Check for lists (enhanced detection)
            if self.list_pattern.match(line_strip):
                if current_block_type != "list":
                    flush_block()
                    current_block_type = "list"
                buffer.append(line_strip)
                continue

            # Check for section markers (Roman numerals, etc.)
            if self.section_pattern.match(line_strip):
                flush_block()
                current_block_type = "section"
                buffer.append(line_strip)
                flush_block()
                current_block_type = None
                continue

            # Check custom patterns
            for pattern_name, pattern in self.custom_patterns.items():
                if pattern.match(line_strip):
                    flush_block()
                    current_block_type = f"custom_{pattern_name}"
                    buffer.append(line_strip)
                    flush_block()
                    current_block_type = None
                    break

            # Default to paragraph if no other pattern matched
            if current_block_type != "paragraph":
                flush_block()
                current_block_type = "paragraph"
            buffer.append(line_strip)

        # Flush any remaining content
        flush_block()

        # Post-process to create hierarchical structure
        return self._create_hierarchy(schema)

    def _create_hierarchy(self, blocks: List[Dict]) -> List[Dict]:
        """
        Create hierarchical structure from flat block list.

        Args:
            blocks: List of document blocks

        Returns:
            List of blocks with hierarchical relationships
        """
        hierarchy = []
        stack = []

        for i, block in enumerate(blocks):
            # Determine block level based on content
            level = self._determine_block_level(block)

            # Pop stack until we find the right parent
            while stack and stack[-1]["level"] >= level:
                stack.pop()

            # Set parent relationship
            if stack:
                block["parent"] = stack[-1]["id"]
                block["level"] = level
            else:
                block["level"] = level

            # Add to hierarchy
            block["id"] = i
            hierarchy.append(block)
            stack.append(block)

        return hierarchy

    def _determine_block_level(self, block: Dict) -> int:
        """
        Determine the hierarchical level of a block.

        Args:
            block: Document block

        Returns:
            Hierarchical level (0 = top level, higher = deeper)
        """
        content = block["content"]

        # Check for numbered sections
        if re.match(r"^\d+(\.\d+)*", content):
            # Count dots to determine level
            dots = content.count(".")
            return dots + 1

        # Check for Roman numeral sections
        if self.section_pattern.match(content):
            return 1

        # Headers are level 2 by default
        if block["type"] == "header":
            return 2

        # Other blocks inherit from parent or are level 3
        return 3

    def extract_metadata(self, blocks: List[Dict]) -> Dict[str, str]:
        """
        Extract metadata from document blocks.

        Args:
            blocks: List of document blocks

        Returns:
            Dictionary of extracted metadata
        """
        metadata = {}
        for block in blocks:
            if block["type"] == "metadata":
                for key, pattern in self.metadata_extractors.items():
                    match = pattern.search(block["content"])
                    if match:
                        metadata[key] = match.group(1).strip()
        return metadata

    def to_dict(self, schema: List[Dict]) -> Dict:
        """
        Convert schema to a nested dictionary structure.

        Args:
            schema: List of document blocks

        Returns:
            Nested dictionary representing document hierarchy
        """
        root = {"type": "document", "children": []}
        blocks_by_id = {block["id"]: block for block in schema}
        children_by_parent = {}

        # Group children by parent
        for block in schema:
            parent_id = block.get("parent")
            if parent_id is None:
                root["children"].append(block)
            else:
                if parent_id not in children_by_parent:
                    children_by_parent[parent_id] = []
                children_by_parent[parent_id].append(block)

        # Build nested structure
        def build_nested(block):
            """Recursively build nested structure."""
            nested = {
                "type": block["type"],
                "content": block["content"],
                "children": []
            }
            if block["id"] in children_by_parent:
                for child in children_by_parent[block["id"]]:
                    nested["children"].append(build_nested(child))
            return nested

        # Build from root children
        nested_structure = []
        for child in root["children"]:
            nested_structure.append(build_nested(child))

        return {"document": nested_structure}

    def to_json(self, schema: List[Dict]) -> str:
        """
        Convert schema to JSON string.

        Args:
            schema: List of document blocks

        Returns:
            JSON string representation
        """
        import json
        nested = self.to_dict(schema)
        return json.dumps(nested, ensure_ascii=False, indent=2)

# Example usage
if __name__ == "__main__":
    # Sample document text
    sample_text = """
    1 Введение
    Это первый абзац документа.

    - Пункт списка 1
    - Пункт списка 2

    | Колонка1 | Колонка2 |
    | -------- | -------- |
    | Значение | Значение |

    2 Основная часть
    Текст основного блока.
    """

    # Create generator and generate schema
    generator = DocumentSchemaGenerator()
    schema = generator.generate_schema(sample_text)

    print("Generated Schema:")
    for block in schema:
        print(f"{block['type']} (level {block.get('level', 0)}): {block['content'][:30]}...")

    print("\nHierarchical Structure:")
    nested = generator.to_dict(schema)
    print(nested)

    print("\nJSON Output:")
    json_output = generator.to_json(schema)
    print(json_output)


