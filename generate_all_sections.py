#!/usr/bin/env python3
"""
Complete GitBook generation script for all remaining sections
"""
import os
import re

source_file = r"C:\Users\Jack\Desktop\ai-news-extractor\docs\Rescribos_AI_Knowledge_Management_Whitepaper.md"
target_dir = r"C:\Users\Jack\Desktop\ai-news-extractor\docs\gitbook"

with open(source_file, 'r', encoding='utf-8') as f:
    content = f.read()

def write_file(path, file_content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(file_content)
    print(f"Created: {path}")

def extract_section(text, start, end=None):
    start_idx = text.find(start)
    if start_idx == -1:
        return ""
    if end:
        end_idx = text.find(end, start_idx + len(start))
        if end_idx == -1:
            end_idx = len(text)
    else:
        end_idx = len(text)
    return text[start_idx:end_idx].strip()

# AI Provider System files
ai_content = extract_section(content, "## 3. AI Provider System", "## 4. Privacy & Security")
write_file(os.path.join(target_dir, "ai-provider-system", "README.md"),
f"""# AI Provider System

{extract_section(ai_content, "### 3.1 Hybrid Architecture Overview", "### 3.2")}

## Sections

- [Hybrid Architecture](hybrid-architecture.md)
- [Provider Implementation](provider-implementation.md)
- [Offline Capabilities](offline-capabilities.md)
""")

write_file(os.path.join(target_dir, "ai-provider-system", "hybrid-architecture.md"),
f"""# Hybrid Architecture

{extract_section(ai_content, "### 3.1 Hybrid Architecture Overview", "### 3.2")}
""")

write_file(os.path.join(target_dir, "ai-provider-system", "provider-implementation.md"),
f"""# Provider Implementation Details

{extract_section(ai_content, "### 3.2 Provider Implementation Details", "### 3.3")}

{extract_section(ai_content, "### 3.3 Network-Aware Provider Selection", "### 3.4")}
""")

write_file(os.path.join(target_dir, "ai-provider-system", "offline-capabilities.md"),
f"""# Offline Capabilities

{extract_section(ai_content, "### 3.4 Offline Capabilities", "---")}
""")

print("AI Provider System files created!")

# Privacy & Security files
priv_content = extract_section(content, "## 4. Privacy & Security", "## 5. Data Processing Pipeline")
write_file(os.path.join(target_dir, "privacy-security", "README.md"),
f"""# Privacy & Security

{extract_section(priv_content, "### 4.1 Local-First Architecture", "### 4.2")}

## Sections

- [Local-First Architecture](local-first.md)
- [Bring Your Own Keys (BYOK)](byok.md)
- [License Management](license-management.md)
- [Enterprise Compliance](compliance.md)
""")

write_file(os.path.join(target_dir, "privacy-security", "local-first.md"),
f"""# Local-First Architecture

{extract_section(priv_content, "### 4.1 Local-First Architecture", "### 4.2")}
""")

write_file(os.path.join(target_dir, "privacy-security", "byok.md"),
f"""# Bring Your Own Keys (BYOK)

{extract_section(priv_content, "### 4.2 Bring Your Own Keys (BYOK)", "### 4.3")}
""")

write_file(os.path.join(target_dir, "privacy-security", "license-management.md"),
f"""# License Management System

{extract_section(priv_content, "### 4.3 License Management System", "### 4.4")}
""")

write_file(os.path.join(target_dir, "privacy-security", "compliance.md"),
f"""# Enterprise Compliance

{extract_section(priv_content, "### 4.4 Data Privacy Guarantees", "### 4.6")}

{extract_section(priv_content, "### 4.5 Enterprise Compliance Mapping", "### 4.6")}

{extract_section(priv_content, "### 4.6 Network Security", "---")}
""")

print("Privacy & Security files created!")

# Data Pipeline files
pipeline_content = extract_section(content, "## 5. Data Processing Pipeline", "## 6. Advanced Features")
write_file(os.path.join(target_dir, "data-pipeline", "README.md"),
f"""# Data Processing Pipeline

{extract_section(pipeline_content, "### 5.1 Complete Workflow Overview", "### 5.2")}

## Sections

- [Complete Workflow](workflow.md)
- [Data Schema](data-schema.md)
- [Performance Metrics](performance-metrics.md)
""")

write_file(os.path.join(target_dir, "data-pipeline", "workflow.md"),
f"""# Complete Workflow

{extract_section(pipeline_content, "### 5.1 Complete Workflow Overview", "### 5.2")}
""")

write_file(os.path.join(target_dir, "data-pipeline", "data-schema.md"),
f"""# Data Schema

{extract_section(pipeline_content, "### 5.2 Data Schema", "### 5.3")}

{extract_section(pipeline_content, "### 5.3 File Locations and Formats", "### 5.4")}
""")

write_file(os.path.join(target_dir, "data-pipeline", "performance-metrics.md"),
f"""# Performance Metrics

{extract_section(pipeline_content, "### 5.4 Performance Metrics", "### 5.5")}

{extract_section(pipeline_content, "### 5.5 Error Handling and Recovery", "---")}
""")

print("Data Pipeline files created!")

# Advanced Features files
adv_content = extract_section(content, "## 6. Advanced Features", "## 7. Technical Implementation")
write_file(os.path.join(target_dir, "advanced-features", "README.md"),
f"""# Advanced Features

Rescribos extends beyond basic knowledge management with advanced capabilities for document processing, workflow management, and automation.

## Sections

- [Document Processing](document-processing.md)
- [Cart-Based Workflow](cart-workflow.md)
- [Report Management](report-management.md)
""")

write_file(os.path.join(target_dir, "advanced-features", "document-processing.md"),
f"""# Document Processing

{extract_section(adv_content, "### 6.1 Document Processing", "### 6.2")}
""")

write_file(os.path.join(target_dir, "advanced-features", "cart-workflow.md"),
f"""# Cart-Based Workflow

{extract_section(adv_content, "### 6.2 Cart-Based Workflow", "### 6.3")}
""")

write_file(os.path.join(target_dir, "advanced-features", "report-management.md"),
f"""# Report Management and Exports

{extract_section(adv_content, "### 6.3 Report Management and Exports", "### 6.4")}

## CLI Tool

{extract_section(adv_content, "### 6.4 CLI Tool", "### 6.5")}

## Docker Support

{extract_section(adv_content, "### 6.5 Docker Support", "---")}
""")

print("Advanced Features files created!")

# Technical Implementation files
tech_content = extract_section(content, "## 7. Technical Implementation", "## 8. Use Cases")
write_file(os.path.join(target_dir, "technical-implementation", "README.md"),
f"""# Technical Implementation

{extract_section(tech_content, "### 7.1 Code Statistics", "### 7.2")}

## Sections

- [Electron Frontend](electron-frontend.md)
- [Node.js Backend](nodejs-backend.md)
- [Python Pipeline](python-pipeline.md)
""")

write_file(os.path.join(target_dir, "technical-implementation", "electron-frontend.md"),
"""# Electron Frontend

See the main Technical Implementation section for code statistics and structure.

The Electron frontend provides a rich, cross-platform desktop interface with:

- Multi-tab interface for reports, search, and chat
- Virtual rendering for large datasets (10,000+ rows)
- Real-time progress tracking
- Responsive design

## Key Files

- `src/renderer/index.html` - Main UI structure
- `src/renderer/app.js` - UI logic and interactions
- `src/renderer/search.js` - Search interface
- `src/renderer/chat.js` - Chat UI and streaming
""")

write_file(os.path.join(target_dir, "technical-implementation", "nodejs-backend.md"),
f"""# Node.js Backend

{extract_section(tech_content, "### 7.3 Configuration Management", "### 7.4")}

{extract_section(tech_content, "### 7.4 System Requirements", "---")}
""")

write_file(os.path.join(target_dir, "technical-implementation", "python-pipeline.md"),
f"""# Python Pipeline

{extract_section(tech_content, "### 7.2 Dependencies", "### 7.3")}
""")

print("Technical Implementation files created!")

# Use Cases files
use_content = extract_section(content, "## 8. Use Cases", "## 9. Deployment")
write_file(os.path.join(target_dir, "use-cases", "README.md"),
"""# Use Cases

Rescribos serves diverse use cases across research, business intelligence, and content curation.

## Primary Use Cases

- Research Intelligence
- Competitive Intelligence
- Due Diligence
- Content Curation

[View detailed examples →](examples.md)
""")

write_file(os.path.join(target_dir, "use-cases", "examples.md"),
f"""# Industry Examples

{use_content}
""")

print("Use Cases files created!")

# Deployment files
deploy_content = extract_section(content, "## 9. Deployment", "## 10. Performance & Scalability")
write_file(os.path.join(target_dir, "deployment", "README.md"),
f"""# Deployment Options

{extract_section(deploy_content, "### 9.1 Desktop Installers", "### 9.2")}

## Sections

- [Installation Guide](installation.md)
- [Configuration](configuration.md)
""")

write_file(os.path.join(target_dir, "deployment", "installation.md"),
f"""# Installation Guide

{extract_section(deploy_content, "### 9.1 Desktop Installers", "### 9.2")}

{extract_section(deploy_content, "### 9.2 Docker Deployment", "### 9.3")}
""")

write_file(os.path.join(target_dir, "deployment", "configuration.md"),
f"""# Configuration

{extract_section(deploy_content, "### 9.3 CLI Usage", "---")}
""")

print("Deployment files created!")

# Performance files
perf_content = extract_section(content, "## 10. Performance & Scalability", "## 11. Licensing")
write_file(os.path.join(target_dir, "performance", "README.md"),
f"""# Performance & Scalability

{extract_section(perf_content, "### 10.1 Benchmark Results", "### 10.2")}

## Sections

- [Benchmarks](benchmarks.md)
- [Optimization](optimization.md)
""")

write_file(os.path.join(target_dir, "performance", "benchmarks.md"),
f"""# Benchmark Results

{extract_section(perf_content, "### 10.1 Benchmark Results", "### 10.2")}

{extract_section(perf_content, "### 10.2 Benchmark Methodology & Reproducibility", "### 10.3")}
""")

write_file(os.path.join(target_dir, "performance", "optimization.md"),
f"""# Optimization Features

{extract_section(perf_content, "### 10.3 Optimization Features", "### 10.4")}

{extract_section(perf_content, "### 10.4 Memory Management", "### 10.5")}

{extract_section(perf_content, "### 10.5 Scalability Limits", "---")}
""")

print("Performance files created!")

# Licensing files
lic_content = extract_section(content, "## 11. Licensing & Deployment Options", "## Conclusion")
write_file(os.path.join(target_dir, "licensing", "README.md"),
f"""# Licensing & Deployment Options

{extract_section(lic_content, "### 11.1 Licensing Tiers Comparison", "### 11.2")}

## Sections

- [License Tiers](tiers.md)
- [Deployment Models](deployment-models.md)
- [FAQs](faqs.md)
""")

write_file(os.path.join(target_dir, "licensing", "tiers.md"),
f"""# License Tiers

{extract_section(lic_content, "### 11.1 Licensing Tiers Comparison", "### 11.2")}

{extract_section(lic_content, "### 11.2 Feature Comparison Matrix", "### 11.3")}
""")

write_file(os.path.join(target_dir, "licensing", "deployment-models.md"),
f"""# Deployment Models

{extract_section(lic_content, "### 11.3 Deployment Models", "### 11.4")}
""")

write_file(os.path.join(target_dir, "licensing", "faqs.md"),
f"""# Licensing FAQs

{extract_section(lic_content, "### 11.4 Volume Licensing & Educational Pricing", "---")}

{extract_section(lic_content, "### 11.5 Migration & Upgrade Paths", "### 11.6")}

{extract_section(lic_content, "### 11.6 Licensing FAQs", "---")}
""")

print("Licensing files created!")

# Appendices
appendix_content = extract_section(content, "## Appendix A:", "## About Rescribos")
write_file(os.path.join(target_dir, "appendices", "file-path-reference.md"),
f"""# Appendix A: File Path Reference

{extract_section(content, "## Appendix A: File Path Reference", "## Appendix B:")}
""")

write_file(os.path.join(target_dir, "appendices", "configuration-examples.md"),
f"""# Appendix B: Configuration Examples

{extract_section(content, "## Appendix B: Configuration Examples", "## Appendix C:")}
""")

write_file(os.path.join(target_dir, "appendices", "troubleshooting.md"),
f"""# Appendix C: Troubleshooting

{extract_section(content, "## Appendix C: Troubleshooting", "## About Rescribos")}
""")

print("Appendices created!")

print("\n✅ All sections generated successfully!")
