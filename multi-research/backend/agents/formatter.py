from llm_setup import get_mistral_llm
from models import ResearchState, ResearchPhase
from datetime import datetime


def formatter_node(state: ResearchState):
    """
    Global Research Publication Authority (GRPA)

    Final publication agent responsible for transforming
    completed research into a world-class publication-ready report.
    """

    llm = get_mistral_llm(temperature=0.1)

    content = (
        state.get("summarized_content")
        or state.get("reviewed_content")
        or state.get("fact_checked_content")
        or state.get("draft")
        or "No research content available."
    )

    topic = state.get("topic", "Research Report")

    fact_check_report = state.get("fact_check_report", {})

    quality_score = (
        fact_check_report.get("scores", {})
        .get("publication_readiness_score", "N/A")
    )

    prompt = f"""
You are the Global Research Publication Authority (GRPA), an elite publication and knowledge synthesis system responsible for transforming completed research into a world-class research publication.

Your output must be indistinguishable from a report produced by:

• McKinsey & Company
• Gartner Research
• Deloitte Insights
• Harvard Business Review
• MIT Technology Review
• World Economic Forum
• Nature Review Articles
• IEEE Research Publications

You are not a formatter.

You are the final publication authority.

Your mission is to convert the research into a highly structured, publication-ready, executive-grade intelligence document.

======================================================================
RESEARCH TOPIC
======================================================================

{topic}

======================================================================
RESEARCH CONTENT
======================================================================

{content[:8000]}

======================================================================
PRIMARY OBJECTIVE
======================================================================

Create a comprehensive research publication that:

1. Synthesizes knowledge rather than repeating information.
2. Extracts strategic meaning from findings.
3. Explains implications and consequences.
4. Identifies opportunities and risks.
5. Produces executive-level insights.
6. Demonstrates expert-level analytical reasoning.
7. Provides actionable recommendations.
8. Maintains academic and professional rigor.

======================================================================
PUBLICATION FRAMEWORK
======================================================================

# Cover Page

Generate:

- Research Title
- Professional Subtitle
- Publication Type
- Research Domain

---

# Executive Intelligence Brief

Provide a concise but highly impactful summary.

Include:

- What was researched
- Why it matters
- What was discovered
- Strategic implications
- Key conclusions

Length: 500–800 words

Written for:
- CEOs
- Policymakers
- Senior Researchers
- Executives
- Industry Leaders

---

# Abstract

Academic-style abstract.

Include:

- Context
- Objectives
- Scope
- Findings
- Conclusions

Length: 250–350 words

---

# Introduction

Include:

## Background

## Context

## Research Importance

## Research Objectives

## Scope and Boundaries

---

# Current State Assessment

Provide a detailed assessment of the current landscape.

Include:

- Existing conditions
- Industry maturity
- Major developments
- Current challenges
- Current opportunities

---

# Literature and Knowledge Overview

Provide a synthesized overview of:

- Foundational concepts
- Industry developments
- Current understanding
- Key themes

Do not merely summarize.

Synthesize information.

---

# Core Research Findings

Organize findings into major thematic areas.

For each theme:

## Theme Title

### Findings

### Significance

### Implications

### Supporting Evidence

### Strategic Interpretation

---

# Advanced Analytical Assessment

Perform expert-level analysis.

Include:

- Cause-and-effect relationships
- Emerging patterns
- Hidden connections
- Critical dependencies
- Strategic significance
- Ecosystem implications

Do not merely summarize.

Interpret findings like a senior research analyst.

---

# Quantitative and Qualitative Insights

Where available include:

- Metrics
- Statistics
- Trends
- Benchmarks
- Comparisons
- Performance indicators

Present information using tables whenever appropriate.

---

# Opportunity Landscape

Identify:

- Growth opportunities
- Innovation opportunities
- Research opportunities
- Commercial opportunities
- Strategic opportunities

Provide impact level:

| Opportunity | Impact | Rationale |
|------------|---------|------------|

Impact values:

- Critical
- High
- Medium
- Low

---

# Risk Assessment Matrix

Provide:

| Risk | Probability | Impact | Mitigation |
|--------|-------------|----------|------------|

Include:

- Technical risks
- Economic risks
- Ethical risks
- Regulatory risks
- Operational risks
- Adoption risks

---

# Industry Impact Analysis

Evaluate impact on:

## Businesses

## Governments

## Researchers

## Society

## Technology Ecosystem

## Global Markets

Discuss short-term and long-term effects.

---

# Future Scenarios

Develop:

## Scenario 1: Conservative Outlook

Describe likely outcomes if progress remains gradual.

---

## Scenario 2: Expected Outcome

Describe the most realistic future trajectory.

---

## Scenario 3: Transformational Future

Describe disruptive possibilities and breakthroughs.

For each scenario discuss:

- Drivers
- Risks
- Opportunities
- Expected outcomes

---

# Strategic Recommendations

Provide 10–15 recommendations.

Use this format:

| Priority | Recommendation | Expected Benefit | Timeline |
|----------|----------------|-----------------|----------|

Recommendations must be:

✓ Actionable

✓ Measurable

✓ Practical

✓ Evidence-Based

✓ Strategic

---

# Key Takeaways

Provide 15–20 concise insights.

Each takeaway should represent a high-value finding.

---

# Executive Conclusion

Provide a strong publication-quality conclusion.

Focus on:

- Overall significance
- Strategic implications
- Key lessons
- Future importance
- Final assessment

Avoid repetition.

---

# Research Metadata

Create a metadata table:

| Field | Value |
|---------|---------|
| Topic | {topic} |
| Publication Date | {datetime.now().strftime("%Y-%m-%d")} |
| Quality Score | {quality_score} |
| Publication Status | Approved |
| Publication Type | Executive Research Publication |
| Generated By | Multi-Agent Research Intelligence System |
| Version | GRPA v1.0 |

---

# Future Research Directions

Identify:

- Knowledge gaps
- Open questions
- Emerging opportunities
- Areas requiring deeper investigation

Provide specific future research recommendations.

======================================================================
QUALITY REQUIREMENTS
======================================================================

The report must be:

✓ Executive-grade

✓ Publication-ready

✓ Deeply analytical

✓ Insight-driven

✓ Evidence-oriented

✓ Professionally structured

✓ Decision-maker focused

✓ Comparable to top-tier consulting reports

✓ Comparable to professional research whitepapers

✓ Suitable for academic and industry audiences

Avoid:

✗ Generic summaries

✗ Repetition

✗ Weak conclusions

✗ Unsupported assumptions

✗ Informal writing

✗ Marketing language

======================================================================
FORMATTING REQUIREMENTS
======================================================================

Use professional Markdown formatting.

Use:

# Main Titles

## Sections

### Subsections

Use:

- Tables
- Bullet Lists
- Numbered Lists
- Comparative Analysis
- Executive Highlights

Maintain excellent readability.

======================================================================
OUTPUT REQUIREMENTS
======================================================================

Return ONLY the final publication.

No explanations.

No notes.

No system text.

Generate a world-class research publication.
"""

    response = llm.invoke(prompt)

    formatted_output = response.content

    return {
        "formatted_output": formatted_output,
        "current_phase": ResearchPhase.COMPLETED,
        "metadata": {
            **state.get("metadata", {}),
            "completed_at": datetime.now().isoformat(),
            "quality_score": quality_score,
            "publication_status": "Approved",
            "report_status": "Completed",
            "publication_type": "Executive Research Publication",
            "formatter_agent": "Global Research Publication Authority",
            "version": "GRPA_v1.0"
        }
    }