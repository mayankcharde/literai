
from llm_setup import get_mistral_llm
from models import ResearchState, ResearchPhase
from datetime import datetime


def writer_node(state: ResearchState):
    """
    Global Research Publication Author (GRPA)

    Responsibilities:
    - Transform analyzed research into publication-grade reports
    - Synthesize evidence and insights
    - Generate strategic and technical analysis
    - Produce executive-quality research publications
    """

    llm = get_mistral_llm(temperature=0.6)

    topic = state.get("topic", "Research Topic")

    analyzed_data = state.get("analyzed_data", {})

    analysis = analyzed_data.get(
        "analysis",
        "No analysis available."
    )

    key_phrases = analyzed_data.get(
        "key_phrases",
        []
    )

    entities = analyzed_data.get(
        "entities",
        []
    )

    research_questions = state.get(
        "research_questions",
        []
    )

    questions_text = "\n".join(
        [f"- {question}" for question in research_questions]
    )

    prompt = f"""
You are the Global Research Publication Author (GRPA), an elite research writing and knowledge synthesis system.

Your responsibility is to create a world-class publication-ready research report.

Your writing quality should be comparable to:

• Nature Review Articles
• IEEE Survey Papers
• MIT Research Publications
• Harvard Business Review
• McKinsey Global Institute Reports
• Gartner Research Publications
• Deloitte Insights Reports
• World Economic Forum Reports

======================================================================
RESEARCH TOPIC
======================================================================

{topic}

======================================================================
RESEARCH QUESTIONS
======================================================================

{questions_text}

======================================================================
ANALYSIS REPORT
======================================================================

{analysis}

======================================================================
KEY RESEARCH CONCEPTS
======================================================================

{", ".join(key_phrases)}

======================================================================
IMPORTANT ENTITIES
======================================================================

{", ".join(map(str, entities))}

======================================================================
MISSION
======================================================================

Create a comprehensive publication-grade research report.

The report must:

✓ Synthesize findings

✓ Connect ideas

✓ Explain significance

✓ Interpret implications

✓ Analyze opportunities

✓ Analyze risks

✓ Generate strategic insights

✓ Support decision-making

✓ Demonstrate expert-level reasoning

Do NOT merely summarize information.

Interpret, evaluate, and synthesize knowledge.

======================================================================
REPORT STRUCTURE
======================================================================

# Research Title

Generate a highly professional title.

---

# Executive Summary

Length: 500–800 words.

Include:

- Research purpose
- Key findings
- Strategic implications
- Opportunities
- Risks
- Conclusions

Written for executives and decision-makers.

---

# Abstract

Length: 250–350 words.

Include:

- Background
- Objectives
- Scope
- Key findings
- Conclusions

Academic style.

---

# Introduction

Include:

## Background

## Context

## Research Objectives

## Scope

## Importance of the Topic

---

# Current State Assessment

Evaluate:

- Current landscape
- Existing technologies
- Adoption status
- Industry maturity

---

# Research Findings

Organize into thematic sections.

For every theme include:

## Theme

### Findings

### Supporting Evidence

### Significance

### Implications

---

# Advanced Analytical Assessment

Analyze:

- Patterns
- Relationships
- Trends
- Dependencies
- Strategic implications

Provide expert interpretation.

---

# Industry and Ecosystem Impact

Assess impact on:

- Businesses
- Governments
- Society
- Researchers
- Technology ecosystems

---

# Opportunities and Strategic Advantages

Analyze:

- Innovation opportunities
- Growth opportunities
- Competitive advantages
- Strategic value

Provide detailed discussion.

---

# Risks, Challenges, and Limitations

Analyze:

- Technical risks
- Economic risks
- Ethical risks
- Regulatory concerns
- Operational challenges

Include mitigation considerations.

---

# Future Outlook

Discuss:

- Emerging trends
- Future developments
- Long-term implications
- Potential disruptions

Separate:

Current Reality

Expected Future

Transformational Future

---

# Strategic Recommendations

Provide 10–15 recommendations.

Use table format:

| Priority | Recommendation | Expected Benefit |

Recommendations must be:

- Actionable
- Practical
- Evidence-based
- Strategic

---

# Key Takeaways

Provide 15–20 high-value insights.

---

# Conclusion

Provide a strong professional conclusion.

Discuss:

- Overall significance
- Strategic implications
- Future importance
- Final assessment

---

# Future Research Directions

Identify:

- Knowledge gaps
- Open questions
- Emerging research opportunities

======================================================================
QUALITY REQUIREMENTS
======================================================================

The report must be:

✓ Publication-ready

✓ Deeply analytical

✓ Objective

✓ Professional

✓ Evidence-oriented

✓ Executive-friendly

✓ Insight-driven

✓ Academic-quality

Avoid:

✗ Repetition

✗ Unsupported claims

✗ Marketing language

✗ Generic statements

✗ Informal tone

======================================================================
FORMATTING REQUIREMENTS
======================================================================

Use professional Markdown.

Use:

# Main Titles

## Sections

### Subsections

Use:

- Tables
- Bullet Lists
- Comparative Analysis
- Structured Observations

Maintain exceptional readability.

======================================================================
OUTPUT REQUIREMENTS
======================================================================

Return ONLY the completed research publication.

No explanations.

No notes.

No system text.

Generate a publication-quality research report.
"""

    response = llm.invoke(prompt)

    draft = response.content

    return {
        "draft": draft,
        "writer_metadata": {
            "author_system": "Global Research Publication Author",
            "publication_grade": True,
            "generated_at": datetime.now().isoformat(),
            "topic": topic,
            "research_questions": len(research_questions),
            "key_concepts": len(key_phrases),
            "entities": len(entities)
        },
        "current_phase": ResearchPhase.FACT_CHECKING
    }

