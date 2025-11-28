# Prompt Templates

This directory contains structured prompt templates used by the Singapore Education Counselor AI agents.

## Structure

```
prompts/
├── README.md                    # This file
├── orchestrator_summary.txt     # Main LLM summary generation prompt
└── translation.txt              # Multi-language translation prompt
```

## Prompt Files

### `orchestrator_summary.txt`

**Used by**: `src/services/orchestrator.py`  
**Purpose**: Generates comprehensive, personalized education counseling summaries  
**Model**: gemini-2.5-flash-lite (configurable)

**Template Variables**:
- `{student_name}` - Student's name
- `{interests}` - Comma-separated interests
- `{strengths}` - Comma-separated strengths  
- `{target_level}` - Academic level (Bachelor, Master, PhD)
- `{budget_category}` - Budget category (Low, Medium, High)
- `{constraints}` - Any constraints or preferences
- `{career_data}` - Career guidance agent output (JSON string)
- `{program_data}` - Institutional data agent output (JSON string)
- `{financial_data}` - Financial aid agent output (JSON string)
- `{skill_data}` - Skill gap agent output (JSON string)
- `{scholarship_data}` - Scholarship matcher output (JSON string)
- `{interview_data}` - Interview prep agent output (JSON string)
- `{learning_data}` - Learning path agent output (JSON string)

**Output**: 400-600 word personalized counseling summary with:
- Top 3 program recommendations with rationale
- Financial strategy and scholarship guidance
- Skill development plan
- Immediate action steps with deadlines
- Interview preparation tips
- Learning roadmap
- Motivational closing

**Key Features**:
- Singapore-specific context (MOE, SkillsFuture, Smart Nation)
- Academic calendar awareness (Aug-Sep intake, Mar-Apr deadlines)
- Culturally appropriate tone
- Actionable next steps

### `translation.txt`

**Used by**: `src/agents/multilang_agent.py`  
**Purpose**: Translates counseling content to target languages  
**Model**: gemini-2.5-flash-lite (configurable)

**Template Variables**:
- `{target_language}` - Target language name (e.g., "Mandarin Chinese", "Tamil", "Malay")
- `{content}` - English content to translate

**Output**: Professionally translated content maintaining:
- Educational terminology accuracy
- Singapore-specific proper nouns (NUS, MOE, etc.)
- Professional counseling tone
- Markdown formatting

**Supported Languages**:
- Mandarin Chinese (zh)
- Tamil (ta)
- Malay (ms)
- And any language supported by the LLM

## Usage

Prompts are loaded at runtime by `src/services/prompt_loader.py`:

```python
from src.services.prompt_loader import load_prompt

# Load and format a prompt
prompt = load_prompt(
    "orchestrator_summary",
    student_name="Jane Doe",
    interests="AI, Machine Learning",
    career_data=json.dumps(career_results),
    # ... other variables
)

# Use with GenAI client
summary = genai_client.summarize(prompt)
```

## Best Practices

### Prompt Engineering
- Keep instructions clear and structured
- Provide examples for complex tasks
- Specify tone, style, and length expectations
- Include domain-specific guidelines (Singapore education context)
- Use consistent variable naming with `{curly_braces}`

### Variable Formatting
- Pass JSON data as formatted strings: `json.dumps(data, indent=2)`
- Keep text variables concise (lists as comma-separated)
- Handle None/missing values gracefully
- Sanitize user input to prevent prompt injection

### Maintenance
- Version prompts when making significant changes
- Test prompts with diverse student profiles
- Monitor LLM output quality and adjust prompts iteratively
- Document any Singapore-specific terminology or requirements

### Performance
- Keep prompts focused (avoid unnecessary context)
- Use token-efficient formatting
- Cache prompt templates (loaded once at startup)
- Monitor token usage per prompt execution

## Testing Prompts

Test prompts with sample data:

```bash
# Test orchestrator summary generation
python -c "from src.services.prompt_loader import load_prompt; print(load_prompt('orchestrator_summary', student_name='Test', interests='AI', strengths='Python', target_level='Bachelor', budget_category='Medium', constraints='None', career_data='{}', program_data='{}', financial_data='{}', skill_data='{}', scholarship_data='{}', interview_data='{}', learning_data='{}'))"

# Test with actual orchestrator
python main.py
```

Use `evaluation.py` to batch test prompt quality across multiple profiles.

## Extending

To add new prompts:

1. Create `prompts/your_prompt_name.txt`
2. Define template variables with `{variable_name}` syntax
3. Document the prompt in this README
4. Update `prompt_loader.py` if custom logic needed
5. Use in agent: `load_prompt("your_prompt_name", variable=value)`

## Singapore Context Reference

When editing prompts, maintain awareness of:

- **Universities**: NUS, NTU, SMU, SUTD, SIT, SUSS
- **Government Initiatives**: MOE, SkillsFuture, Smart Nation, MAS FinTech
- **Scholarships**: MOE Tuition Grant, ASEAN Scholarship, NUS Global Merit
- **Academic Calendar**: Aug-Sep intake, Mar-Apr application deadlines
- **Cultural Context**: Multicultural (English, Mandarin, Malay, Tamil), meritocratic, tech-forward

## Version History

- **v1.0** (Nov 2025): Initial structured prompt system with orchestrator and translation templates
