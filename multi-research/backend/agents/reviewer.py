from llm_setup import get_mistral_llm
from tools.validation_tools import check_consistency
from models import ResearchState, ResearchPhase
import json


def reviewer_node(state: ResearchState):
    """
    Global Research Review Board (GRRB)

    Final quality assurance and publication review authority
    responsible for determining whether a research report
    meets world-class publication standards.
    """

    llm = get_mistral_llm(temperature=0.2)

    content = (
        state.get("fact_checked_content")
        or state.get("draft")
        or ""
    )

    prompt = f"""
You are the Global Research Review Board (GRRB), the highest-level quality assurance and publication review authority within an advanced Multi-Agent Research Intelligence System.

You are not a proofreader.

You are not an editor.

You are a world-class research review committee responsible for determining whether a research publication meets the standards of:

• Nature Research
• IEEE Publications
• ACM Journals
• MIT Research Reports
• Harvard Business Review
• Gartner Research
• McKinsey Global Institute
• Deloitte Insights
• World Economic Forum Reports

======================================================================
RESEARCH REPORT UNDER REVIEW
======================================================================

{content[:6000]}

======================================================================
REVIEW OBJECTIVE
======================================================================

Perform a comprehensive publication-grade review.

Determine whether this report demonstrates:

1. Research excellence
2. Analytical rigor
3. Intellectual depth
4. Evidence quality
5. Logical consistency
6. Strategic value
7. Practical relevance
8. Publication readiness
9. Academic credibility
10. Executive usefulness

You must identify strengths, weaknesses, risks, gaps, inconsistencies, and opportunities for improvement.

======================================================================
EVALUATION FRAMEWORK
======================================================================

### RESEARCH QUALITY

Evaluate:

- Topic coverage
- Research depth
- Intellectual rigor
- Quality of investigation
- Sophistication of analysis

---

### ANALYTICAL DEPTH

Assess:

- Critical thinking
- Interpretation quality
- Insight generation
- Strategic reasoning
- Quality of conclusions

Determine whether the report demonstrates expert-level analysis.

---

### EVIDENCE AND SUPPORT

Assess:

- Reliability of evidence
- Strength of arguments
- Support for conclusions
- Citation adequacy
- Data quality

Identify unsupported claims.

---

### LOGICAL CONSISTENCY

Review:

- Internal consistency
- Contradictions
- Reasoning quality
- Cause-effect logic
- Flow of arguments

Flag any weaknesses.

---

### COMPLETENESS

Assess whether the report adequately covers:

- Core concepts
- Technical considerations
- Industry implications
- Risks
- Opportunities
- Future outlook

Identify missing areas.

---

### STRATEGIC VALUE

Determine whether the report provides:

- Actionable insights
- Executive value
- Business relevance
- Policy relevance
- Research value

---

### PROFESSIONAL QUALITY

Evaluate:

- Writing quality
- Readability
- Organization
- Professional presentation
- Objectivity
- Neutrality

---

### FUTURE-READINESS

Assess:

- Future outlook quality
- Trend analysis quality
- Forecasting quality
- Innovation analysis

---

### PUBLICATION READINESS

Determine whether the report is:

APPROVE:
Ready for publication with no significant changes.

REVISE:
Requires improvements before publication.

REJECT:
Fails to meet publication standards.

======================================================================
SCORING SYSTEM
======================================================================

Score each category from 0 to 10.

Evaluate:

- research_quality
- analytical_depth
- evidence_quality
- logical_consistency
- completeness
- strategic_value
- professional_quality
- future_readiness
- publication_readiness

Calculate an overall score.

======================================================================
SEVERITY FRAMEWORK
======================================================================

For every weakness classify severity:

CRITICAL
HIGH
MEDIUM
LOW

======================================================================
OUTPUT FORMAT
======================================================================

Return ONLY valid JSON.

{{
    "decision": "APPROVE|REVISE|REJECT",

    "overall_score": 0,

    "executive_summary": "",

    "strengths": [
        ""
    ],

    "weaknesses": [
        {{
            "issue": "",
            "severity": "CRITICAL|HIGH|MEDIUM|LOW",
            "explanation": ""
        }}
    ],

    "research_gaps": [
        ""
    ],

    "improvement_suggestions": [
        ""
    ],

    "publication_risks": [
        ""
    ],

    "scores": {{
        "research_quality": 0,
        "analytical_depth": 0,
        "evidence_quality": 0,
        "logical_consistency": 0,
        "completeness": 0,
        "strategic_value": 0,
        "professional_quality": 0,
        "future_readiness": 0,
        "publication_readiness": 0
    }},

    "publication_assessment": "",

    "executive_feedback": "",

    "reviewer_recommendation": ""
}}

Return ONLY valid JSON.
"""

    response = llm.invoke(prompt)

    review_data = {}

    try:
        content_response = response.content.strip()

        json_start = content_response.find("{")
        json_end = content_response.rfind("}") + 1

        if json_start != -1 and json_end > json_start:
            review_data = json.loads(
                content_response[json_start:json_end]
            )

    except Exception as e:
        print(f"Reviewer parsing error: {e}")
        review_data = {}

    decision = (
        review_data.get("decision", "REVISE")
        .upper()
        .strip()
    )

    is_approved = decision == "APPROVE"

    quality_metrics = state.get("quality_metrics", {})

    if not isinstance(quality_metrics, dict):
        quality_metrics = {}

    consistency_score = 1.0

    if (
        state.get("draft")
        and state.get("fact_checked_content")
    ):
        consistency_score = check_consistency(
            state["draft"],
            state["fact_checked_content"]
        )

    scores = review_data.get("scores", {})

    overall_score = review_data.get(
        "overall_score",
        8.5 if is_approved else 6.0
    )

    quality_metrics.update({
        "overall_score": overall_score,
        "consistency_score": consistency_score,
        "research_quality": scores.get(
            "research_quality",
            0
        ),
        "analytical_depth": scores.get(
            "analytical_depth",
            0
        ),
        "evidence_quality": scores.get(
            "evidence_quality",
            0
        ),
        "logical_consistency": scores.get(
            "logical_consistency",
            0
        ),
        "completeness": scores.get(
            "completeness",
            0
        ),
        "strategic_value": scores.get(
            "strategic_value",
            0
        ),
        "professional_quality": scores.get(
            "professional_quality",
            0
        ),
        "future_readiness": scores.get(
            "future_readiness",
            0
        ),
        "publication_readiness": scores.get(
            "publication_readiness",
            0
        )
    })

    reviewer_feedback = []

    if review_data:

        if review_data.get("executive_feedback"):
            reviewer_feedback.append(
                review_data["executive_feedback"]
            )

        if review_data.get("publication_assessment"):
            reviewer_feedback.append(
                review_data["publication_assessment"]
            )

        if review_data.get("reviewer_recommendation"):
            reviewer_feedback.append(
                review_data["reviewer_recommendation"]
            )

    else:
        reviewer_feedback.append(
            response.content
        )

    return {
        "reviewer_feedback": reviewer_feedback,
        "review_report": review_data,
        "is_approved": is_approved,
        "quality_metrics": quality_metrics,
        "current_phase": (
            ResearchPhase.SUMMARIZATION
            if is_approved
            else ResearchPhase.WRITING
        ),
        "iteration_count": state.get(
            "iteration_count",
            0
        ) + 1,
        "review_metadata": {
            "review_board": "Global Research Review Board",
            "review_status": decision,
            "overall_score": overall_score,
            "consistency_score": consistency_score,
            "publication_ready": is_approved
        }
    }