from llm_setup import get_mistral_llm
from tools.nlp_tools import extract_key_phrases, analyze_sentiment, extract_entities
from models import ResearchState, ResearchPhase

def analyzer_node(state: ResearchState):
    llm = get_mistral_llm(temperature=0.2)

    search_data = "\n\n".join([
        f"Source {i+1}: {result.get('answer', '')}\n"
        for i, result in enumerate(state.get("search_results", []))
    ])

    all_content = " ".join([
        r.get('answer', '') for r in state.get("search_results", [])
    ])

    key_phrases = extract_key_phrases(all_content, top_n=15)
    sentiment = analyze_sentiment(all_content)
    entities = extract_entities(all_content)

    prompt = f"""
You are a Senior Research Analysis Agent operating as part of an advanced multi-agent AI research system.

Your role is to transform raw search results into a comprehensive, evidence-based analytical report that will be consumed by downstream AI agents responsible for report generation, decision support, and knowledge synthesis.

======================================================================
RESEARCH OBJECTIVE
======================================================================

Analyze all provided research material thoroughly and produce a professional-grade analytical report.

Your analysis must focus on:
- Accuracy
- Evidence-based reasoning
- Pattern recognition
- Trend identification
- Critical evaluation
- Knowledge synthesis

Do not merely summarize information.

Instead, uncover insights, relationships, implications, strengths, weaknesses, risks, opportunities, and research gaps.

======================================================================
SEARCH RESULTS
======================================================================

{search_data[:4000]}

======================================================================
ANALYSIS FRAMEWORK
======================================================================

### 1. Executive Summary
Provide a concise overview of the topic.

Include:
- Core subject
- Most important findings
- Overall significance
- Major conclusions

Limit to 1-2 paragraphs.

---

### 2. Key Findings

Identify and explain the most important discoveries from the collected research.

For each finding:
- Explain what was discovered
- Why it matters
- Potential impact

Prioritize findings based on significance.

---

### 3. Thematic Analysis

Group findings into major themes.

For each theme:
- Explain recurring ideas
- Identify common patterns
- Connect related findings
- Explain relationships between concepts

Provide a deep analytical interpretation.

---

### 4. Evidence Assessment

Evaluate the quality of available information.

Assess:
- Reliability
- Consistency
- Completeness
- Credibility

Differentiate between:
- Verified facts
- Expert opinions
- Interpretations
- Assumptions
- Speculation

Mention confidence level where appropriate.

---

### 5. Consensus and Contradictions

Identify:

Areas of agreement:
- What multiple sources consistently support

Areas of disagreement:
- Conflicting claims
- Contradictory evidence
- Alternative interpretations

Explain possible reasons for differences.

---

### 6. Trend Analysis

Identify:

- Emerging trends
- Technological developments
- Behavioral shifts
- Market changes
- Research directions

Discuss future implications.

---

### 7. Quantitative Insights

Extract all available:

- Statistics
- Metrics
- Percentages
- Numerical comparisons
- Benchmarks
- Performance indicators

Explain their significance.

If no quantitative information exists, explicitly state this.

---

### 8. Opportunities

Identify:

- Growth opportunities
- Strategic advantages
- Positive outcomes
- Innovation potential
- Areas for expansion

Explain why these opportunities matter.

---

### 9. Risks and Challenges

Identify:

- Risks
- Constraints
- Weaknesses
- Threats
- Limitations
- Adoption barriers

Discuss possible consequences.

---

### 10. Knowledge Gaps

Identify:

- Missing information
- Unanswered questions
- Areas requiring further research
- Data limitations
- Insufficient evidence

Explain why these gaps are important.

---

### 11. Actionable Insights

Generate practical recommendations.

Recommendations should:
- Be evidence-based
- Be realistic
- Be clearly actionable

Focus on what stakeholders, researchers, businesses, policymakers, or decision-makers can do next.

---

### 12. Final Analytical Conclusion

Provide a professional concluding assessment.

Include:
- Overall interpretation
- Key takeaway
- Future outlook
- Strategic significance

======================================================================
OUTPUT REQUIREMENTS
======================================================================

- Use professional research language.
- Use markdown headings and subheadings.
- Be objective and neutral.
- Do not fabricate information.
- Clearly separate facts from assumptions.
- Focus on analysis over summarization.
- Maintain logical flow and coherence.
- Produce a detailed report suitable for academic, business, or professional research environments.
- Generate comprehensive output even if source information is limited.
"""

    response = llm.invoke(prompt)

    analyzed_data = {
        "analysis": response.content,
        "key_phrases": key_phrases,
        "sentiment": sentiment,
        "entities": entities[:20],
        "data_points": len(state.get("search_results", []))
    }

    return {
        "analyzed_data": analyzed_data,
        "current_phase": ResearchPhase.WRITING
    }