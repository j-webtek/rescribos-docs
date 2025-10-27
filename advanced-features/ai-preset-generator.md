# AI Preset Generator

The AI Preset Generator allows you to create custom analysis frameworks through natural language interaction. Instead of manually writing JSON configuration files, describe your strategic intelligence requirements and let the AI generate a complete, production-ready preset.

## Overview

**Purpose:** Rapid deployment of custom analysis frameworks for specialized intelligence workflows without requiring technical JSON knowledge.

**Workflow:**
1. **Define Objectives**: Describe your intelligence requirements (50+ characters)
2. **Refine Parameters**: Answer AI-generated clarifying questions
3. **Generate Framework**: AI creates complete preset configuration
4. **Deploy Preset**: Download and import ready-to-use JSON file

## Key Features

### Natural Language Interface

**No technical expertise required:**
- Describe needs in plain English
- AI interprets requirements and asks relevant questions
- Automatic schema validation ensures compliance
- Production-ready output in minutes

### Intelligent Question Generation

**AI asks targeted clarifying questions:**
- 3-5 questions based on your description
- Multiple choice and free-text options
- Ensures all required configuration covered
- Adapts questions to your domain

### Complete Preset Generation

**Generates all required components:**
- **Custom Audiences**: Tailored audience definitions with analysis directives
- **Voice Directives**: Professional analytical tone and structure
- **Output Configuration**: Format, sections, and length specifications
- **Metadata**: Timestamps, versioning, and attribution

### Framework Quality Assurance

**Built-in validation:**
- Conforms to v2.2.0 schema standards
- All required fields populated
- Consistent terminology and structure
- Best practices applied automatically

## Use Cases

### Policy Analysis

**Example Input:**
```
Policy analyst tracking regulatory changes in AI governance
and international standards
```

**Generated Output:**
- Custom "Policy Analysts" audience
- Regulatory framework analysis directives
- International standards alignment focus
- Structured policy analysis sections

### Technical Due Diligence

**Example Input:**
```
Investment team conducting technical due diligence on AI
infrastructure companies
```

**Generated Output:**
- Technical evaluation framework
- Due diligence checklist sections
- Risk assessment parameters
- Investment decision directives

### Security Research

**Example Input:**
```
Security researcher monitoring adversarial AI techniques
and emerging threat vectors
```

**Generated Output:**
- Threat analysis framework
- Technical vulnerability assessment
- Attack vector categorization
- Defensive recommendations structure

### Strategic Intelligence

**Example Input:**
```
Strategic intelligence on foundation model capabilities
and competitive positioning
```

**Generated Output:**
- Competitive analysis framework
- Technical capability assessment
- Market positioning evaluation
- Strategic implications analysis

## User Flow

### Step 1: Define Intelligence Requirements

**Prompt:** Define your intelligence requirements (minimum 50 characters)

**What to Include:**
- **Who**: Strategic role and expertise level
- **What**: Operational intelligence domain and scope
- **Why**: Strategic objectives and mission-critical goals
- **Parameters**: Classification level, analytical framework, output constraints

**Example Descriptions:**
```
"Policy analyst tracking regulatory changes in AI governance
and international standards"

"Investment team conducting technical due diligence on AI
infrastructure companies"

"Security researcher monitoring adversarial AI techniques
and emerging threat vectors"

"Strategic intelligence on foundation model capabilities
and competitive positioning"
```

### Step 2: Refine Parameters

**AI-Generated Questions** (examples):

1. **Audience Type**: Who is the primary audience?
   - Options: C-Suite Executives, Technical Teams, Policy Makers, Investors, etc.

2. **Analysis Focus**: What aspects should be emphasized?
   - Free text: "regulatory compliance, risk assessment, technical feasibility"

3. **Output Structure**: How should the analysis be organized?
   - Options: Structured sections, Executive summary focus, Technical deep dive, etc.

4. **Analytical Tone**: What tone should the analysis maintain?
   - Options: Analytical, Formal, Technical, Strategic, etc.

5. **Analysis Depth**: How detailed should the analysis be?
   - Options: Brief overview (200-400 words), Standard (400-700 words), Comprehensive (700+ words)

### Step 3: Generate Analysis Framework

**AI Processing:**
1. Analyzes your requirements and answers
2. Generates custom audience definition
3. Creates voice directive with analysis structure
4. Configures output parameters and sections
5. Adds metadata and tags
6. Validates against schema v2.2.0

**Generated Components:**

**Custom Audience:**
```json
{
  "policy_analysts": {
    "name": "Policy Analysts",
    "is_custom": true,
    "description": "Policy analyst tracking AI governance",
    "analysis_impact": "Focus on regulatory frameworks,
      international standards alignment (OECD, ISO, NIST),
      policy trajectory analysis...",
    "expertise_level": "advanced",
    "primary_concerns": [
      "regulatory_frameworks",
      "international_standards",
      "policy_trajectory"
    ]
  }
}
```

**Voice Directive:**
```
POLICY ANALYSIS: Analyze as policy analyst tracking AI governance
developments. Focus on regulatory framework evolution, international
standards alignment, cross-jurisdictional coordination, and policy
implementation pathways. Use policy terminology: regulatory frameworks
(OECD AI Principles, EU AI Act, NIST AI RMF), standards alignment,
compliance requirements, harmonization efforts. Structure analysis
around: Regulatory Landscape → Framework Analysis → International
Standards → Implementation Implications.
```

**Output Configuration:**
```json
{
  "format": "structured",
  "tone": "analytical",
  "perspective": "third_person",
  "max_length": 700,
  "sections": [
    "regulatory_landscape",
    "framework_analysis",
    "international_standards_alignment",
    "implementation_pathways",
    "strategic_implications"
  ]
}
```

### Step 4: Deploy Preset

**Download Options:**
- **Download JSON**: Save complete preset file
- **Copy to Clipboard**: Manual editing before import
- **Preview**: Review generated configuration
- **Start Over**: Create different preset

**Import Process:**
1. Save JSON file to `config/presets/` directory
2. Or use Import modal in Rescribos UI
3. Preset immediately available in analysis dropdown
4. Can be edited manually if needed

## Accessing the Generator

**Location:** Import Modal → "Generate Custom Preset with AI" button

**Navigation:**
1. Open Rescribos application
2. Go to Analysis/Import section
3. Click **"Style Presets"** or **"Import"**
4. Look for **"Generate Custom Preset with AI"** link
5. Click to launch generator modal

## Technical Architecture

### Frontend Components

**File:** `src/renderer/preset-generator.js`

**Key Methods:**
- `open()` - Launch generator modal
- `submitDescription()` - Process user requirements
- `generateQuestions()` - Request AI questions
- `renderQuestions()` - Display dynamic question UI
- `submitAnswers()` - Process user responses
- `generatePreset()` - Request preset generation
- `downloadPreset()` - Save generated JSON

### Backend Components

**File:** `scripts/preset_generator.py`

**AI Generation:**
- Uses GPT-4/5 for intelligent question generation
- Structured output for preset configuration
- Schema validation before return
- Error handling and retry logic

**Generated Schema:** v2.2.0 compliant

## Configuration

**Environment Variables:**
```env
# AI Model selection
OPENAI_API_KEY=your_api_key_here
PRESET_GENERATOR_MODEL=gpt-4              # AI model for generation

# Generation parameters
PRESET_GENERATOR_TEMPERATURE=0.7          # Creativity level
PRESET_GENERATOR_MAX_TOKENS=2000          # Response length
PRESET_GENERATOR_TIMEOUT=30000            # Request timeout (ms)
```

## Best Practices

### Writing Effective Descriptions

**Do:**
- Be specific about your role and objectives
- Mention domain expertise level
- Include key analytical focus areas
- Specify any constraints or requirements

**Don't:**
- Use vague or generic descriptions
- Omit critical context
- Rush through minimum character count
- Skip important parameters

**Examples:**

✅ **Good:**
```
"Policy analyst tracking regulatory changes in AI governance,
focusing on EU AI Act implementation, OECD framework alignment,
and cross-jurisdictional harmonization. Need analytical tone
suitable for senior policy makers."
```

❌ **Too Vague:**
```
"Someone who needs to analyze AI stuff for policy work"
```

### Answering Clarifying Questions

- **Be thorough**: Provide complete answers
- **Stay consistent**: Align with original description
- **Add context**: Free-text fields allow elaboration
- **Consider audience**: Think about who will read the analysis

### Customizing Generated Presets

**After Download:**
1. Generated presets are fully editable JSON
2. Modify sections, tone, or parameters as needed
3. Add custom fields or remove unnecessary ones
4. Test with sample content before production use

## Troubleshooting

**Generator not loading:**
- Verify internet connection (requires API access)
- Check OpenAI API key is configured
- Review browser console for errors
- Try refreshing the application

**Questions seem irrelevant:**
- Provide more specific initial description
- Include domain terminology in description
- Start over with revised description
- Contact support if issue persists

**Generated preset not working:**
- Verify JSON file is valid
- Check schema version compatibility
- Review error messages in logs
- Manually validate required fields

**AI responses too generic:**
- Provide more detailed answers to questions
- Use technical terminology in responses
- Specify exact requirements explicitly
- Iterate and regenerate if needed

## Related Documentation

- [AI Preset Generator - Complete Documentation](../../../AI_PRESET_GENERATOR.md) - Full technical reference
- [Custom Style Creation Guide](../../../CUSTOM_STYLE_CREATION_GUIDE.md) - Manual preset creation
- [Style System Complete Guide](../../../STYLE_SYSTEM_COMPLETE_GUIDE.md) - Style system overview
- [Prompt Optimization](../../../prompts.md) - Understanding prompt engineering
