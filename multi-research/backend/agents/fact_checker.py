from llm_setup import get_mistral_llm
from tools.validation_tools import check_plagiarism_risk, validate_citations
from models import ResearchState, ResearchPhase
import json

def fact_checker_node(state: ResearchState):
    llm = get_mistral_llm(temperature=0.1)

    draft = state.get("draft", "")

    plagiarism_check = check_plagiarism_risk(draft)
    citation_check = validate_citations(draft)

    prompt = f"""
You are an Elite Research Fact-Checking and Quality Assurance Agent operating within a professional multi-agent AI research system.

Your responsibility is to perform a rigorous audit of the research report before publication.

You must evaluate:

1. Factual accuracy
2. Logical consistency
3. Citation quality
4. Evidence support
5. Bias detection
6. Hallucination risk
7. Research integrity
8. Academic credibility
9. Completeness of claims
10. Overall publication readiness

======================================================================
REPORT TO REVIEW
======================================================================

{draft[:3000]}

======================================================================
FACT-CHECKING FRAMEWORK
======================================================================

Perform a detailed verification process using the following criteria.

### 1. FACTUAL ACCURACY REVIEW

Identify:

- Incorrect facts
- Unsupported statements
- Misleading claims
- Inaccurate statistics
- Questionable conclusions
- Overgeneralizations

For each issue provide:
- Claim
- Issue description
- Severity (Low/Medium/High)
- Suggested correction

---

### 2. EVIDENCE VALIDATION

Evaluate whether claims are:

- Fully supported
- Partially supported
- Unsupported

Identify:

- Missing evidence
- Weak evidence
- Unverifiable assertions
- Speculative statements presented as facts

---

### 3. LOGICAL CONSISTENCY CHECK

Detect:

- Contradictions
- Logical fallacies
- Circular reasoning
- Unsupported cause-effect relationships
- Invalid assumptions

Provide explanations.

---

### 4. HALLUCINATION DETECTION

Identify statements that appear:

- Fabricated
- Invented
- Unverifiable
- Excessively confident without evidence

Flag all potential hallucinations.

---

### 5. CITATION QUALITY REVIEW

Evaluate:

- Citation completeness
- Citation relevance
- Citation placement
- Missing references
- Claims lacking attribution

Identify citation weaknesses.

---

### 6. BIAS ANALYSIS

Detect:

- Political bias
- Commercial bias
- Confirmation bias
- Selection bias
- Emotional language
- Subjective wording

Recommend neutral alternatives.

---

### 7. RESEARCH QUALITY ASSESSMENT

Assess:

- Objectivity
- Reliability
- Credibility
- Transparency
- Analytical depth

Provide strengths and weaknesses.

---

### 8. COMPLETENESS REVIEW

Determine whether:

- Important perspectives are missing
- Counterarguments are absent
- Key evidence is overlooked
- Significant research gaps remain

List all missing elements.

---

### 9. RISK ASSESSMENT

Identify risks related to:

- Misinformation
- Misinterpretation
- Legal concerns
- Ethical concerns
- Publication credibility

Assign severity levels.

---

### 10. OVERALL PUBLICATION READINESS

Evaluate whether the report is:

- Publication Ready
- Minor Revision Required
- Major Revision Required
- Not Ready For Publication

Provide reasoning.

======================================================================
SCORING CRITERIA
======================================================================

Provide numerical scores (0-100) for:

- factual_accuracy_score
- evidence_quality_score
- citation_quality_score
- logical_consistency_score
- objectivity_score
- publication_readiness_score

======================================================================
OUTPUT REQUIREMENTS
======================================================================

Return ONLY valid JSON.

Do not include markdown.

Do not include explanations outside JSON.

Use this exact structure:

{{
    "factual_errors": [
        {{
            "claim": "",
            "issue": "",
            "severity": "Low|Medium|High",
            "suggested_fix": ""
        }}
    ],
    "unsupported_claims": [],
    "hallucination_risks": [],
    "citation_issues": [],
    "bias_indicators": [],
    "logical_inconsistencies": [],
    "missing_evidence": [],
    "research_gaps": [],
    "risks": [],
    "strengths": [],
    "weaknesses": [],
    "scores": {{
        "factual_accuracy_score": 0,
        "evidence_quality_score": 0,
        "citation_quality_score": 0,
        "logical_consistency_score": 0,
        "objectivity_score": 0,
        "publication_readiness_score": 0
    }},
    "overall_accuracy": "high|medium|low",
    "publication_status": "Publication Ready|Minor Revision Required|Major Revision Required|Not Ready For Publication",
    "summary": "",
    "requires_revision": true
}}

Return valid JSON only.
"""

    response = llm.invoke(prompt)

    try:
        content = response.content.strip()

        json_start = content.find("{")
        json_end = content.rfind("}") + 1

        if json_start != -1 and json_end > json_start:
            fact_check = json.loads(content[json_start:json_end])
        else:
            fact_check = {}
    except Exception:
        fact_check = {}

    fact_check_report = {
        **fact_check,
        "automated_checks": {
            "plagiarism_risk": plagiarism_check,
            "citations": citation_check
        }
    }

    requires_revision = fact_check.get("requires_revision", False)

    if requires_revision:
        return {
            "fact_check_report": fact_check_report,
            "current_phase": ResearchPhase.WRITING,
            "iteration_count": state.get("iteration_count", 0) + 1
        }

    return {
        "fact_check_report": fact_check_report,
        "fact_checked_content": draft,
        "current_phase": ResearchPhase.REVIEW
    }