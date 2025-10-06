#!/usr/bin/env python3
"""
Script to generate GitBook structure from Rescribos whitepaper
"""
import os
import re

# Read the source whitepaper
source_file = r"C:\Users\Jack\Desktop\ai-news-extractor\docs\Rescribos_AI_Knowledge_Management_Whitepaper.md"
target_dir = r"C:\Users\Jack\Desktop\ai-news-extractor\docs\gitbook"

with open(source_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Split by main sections
sections = re.split(r'\n## (\d+\. .+?)\n', content)

# Helper function to write files
def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created: {path}")

# Extract sections by heading pattern
def extract_section(content, start_pattern, end_pattern=None):
    """Extract content between two patterns"""
    start = content.find(start_pattern)
    if start == -1:
        return ""

    if end_pattern:
        end = content.find(end_pattern, start + len(start_pattern))
        if end == -1:
            end = len(content)
    else:
        end = len(content)

    return content[start:end].strip()

# Architecture files
arch_content = extract_section(content, "## 1. System Architecture", "## 2. Core Capabilities")
write_file(os.path.join(target_dir, "architecture", "README.md"),
f"""# System Architecture

This section provides a comprehensive overview of the Rescribos platform architecture, including the multi-layer design, technology stack, and cross-platform support.

{extract_section(arch_content, "### 1.1 Multi-Layer Design", "### 1.2")}

[Continue to Multi-Layer Design →](multi-layer-design.md)
""")

write_file(os.path.join(target_dir, "architecture", "multi-layer-design.md"),
f"""# Multi-Layer Design

{extract_section(arch_content, "### 1.1 Multi-Layer Design", "### 1.2")}
""")

write_file(os.path.join(target_dir, "architecture", "technology-stack.md"),
f"""# Technology Stack

{extract_section(arch_content, "### 1.2 Technology Stack", "### 1.3")}
""")

write_file(os.path.join(target_dir, "architecture", "cross-platform.md"),
f"""# Cross-Platform Support

{extract_section(arch_content, "### 1.3 Cross-Platform Support", "---")}
""")

print("Architecture files created successfully!")

# Core Capabilities files
cap_content = extract_section(content, "## 2. Core Capabilities", "## 3. AI Provider System")
write_file(os.path.join(target_dir, "core-capabilities", "README.md"),
"""# Core Capabilities

Rescribos offers a comprehensive suite of AI-powered capabilities for knowledge management and research intelligence.

## Overview

- [Data Extraction](data-extraction.md) - Multi-source content collection
- [AI-Powered Analysis](ai-analysis.md) - Intelligent summarization and scoring
- [Thematic Analysis](thematic-analysis.md) - Advanced pattern recognition
- [Semantic Search](semantic-search.md) - Vector-based discovery
- [Interactive AI Chat](ai-chat.md) - Natural language queries

Navigate to each section for detailed information.
""")

write_file(os.path.join(target_dir, "core-capabilities", "data-extraction.md"),
f"""# Intelligent Data Extraction

{extract_section(cap_content, "### 2.1 Intelligent Data Extraction", "### 2.2")}
""")

write_file(os.path.join(target_dir, "core-capabilities", "ai-analysis.md"),
f"""# AI-Powered Analysis

{extract_section(cap_content, "### 2.2 AI-Powered Analysis", "### 2.3")}
""")

write_file(os.path.join(target_dir, "core-capabilities", "thematic-analysis.md"),
f"""# Thematic Analysis Engine

{extract_section(cap_content, "### 2.3 Thematic Analysis Engine", "### 2.4")}
""")

write_file(os.path.join(target_dir, "core-capabilities", "semantic-search.md"),
f"""# Semantic Search & Discovery

{extract_section(cap_content, "### 2.4 Semantic Search & Discovery", "### 2.5")}
""")

write_file(os.path.join(target_dir, "core-capabilities", "ai-chat.md"),
f"""# Interactive AI Chat

{extract_section(cap_content, "### 2.5 Interactive AI Chat", "---")}
""")

print("Core capabilities files created successfully!")

print("\n=== Generation complete! ===")
print("Now run this script with Python to generate all remaining files.")
