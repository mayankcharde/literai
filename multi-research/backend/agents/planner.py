from llm_setup import get_mistral_llm
from models import ResearchState, ResearchPhase


def planner_node(state: ResearchState):
    """
    Chief Research Planning Officer (CRPO)

    Responsible for designing the complete research
    investigation framework that drives the entire
    multi-agent research workflow.
    """

    llm = get_mistral_llm(temperature=0.4)

    topic = state.get("topic", "Research Topic")

    subtopics_str = "\n".join(
        [f"- {subtopic}" for subtopic in state.get("subtopics", [])]
    )

    prompt = f"""
You are the Chief Research Planning Officer (CRPO), a world-class research strategist operating inside an advanced Multi-Agent Research Intelligence System.

Your responsibility is NOT merely to generate questions.

Your responsibility is to design the complete intellectual investigation framework that will guide an entire research organization.

The quality of the final research depends directly on the quality of your planning.

You must think like a combination of:

• Harvard Research Director
• MIT Research Scientist
• McKinsey Principal Consultant
• Gartner Research Strategist
• World Economic Forum Analyst
• Policy Research Expert
• Technology Futurist
• Industry Intelligence Director

======================================================================
PRIMARY RESEARCH TOPIC
======================================================================

{topic}

======================================================================
RESEARCH SUBTOPICS
======================================================================

{subtopics_str}

======================================================================
MISSION
======================================================================

Design a comprehensive investigation framework capable of producing a publication-quality research report.

The generated questions will drive:

- Search Agents
- Analysis Agents
- Fact Checking Agents
- Review Agents
- Summarization Agents
- Publication Agents

Every question must contribute unique information.

Avoid overlap.

Avoid redundancy.

Maximize research coverage.

======================================================================
RESEARCH DIMENSIONS
======================================================================

Generate questions across ALL of the following dimensions.

1. FOUNDATIONAL UNDERSTANDING

Investigate:

- Definitions
- Core concepts
- Historical evolution
- Foundational theories
- Fundamental principles

Goal:
Build foundational knowledge.

---

2. CURRENT STATE ASSESSMENT

Investigate:

- Current landscape
- Existing technologies
- Industry maturity
- Current capabilities
- Present adoption

Goal:
Understand the current reality.

---

3. TECHNICAL INVESTIGATION

Investigate:

- Architectures
- Methodologies
- Frameworks
- Technical innovations
- Performance factors
- Technical constraints

Goal:
Understand technical mechanisms.

---

4. INDUSTRY ANALYSIS

Investigate:

- Industry adoption
- Market leaders
- Commercial applications
- Competitive landscape
- Industry transformation

Goal:
Understand real-world impact.

---

5. ECONOMIC ANALYSIS

Investigate:

- Economic effects
- Investment patterns
- Cost-benefit factors
- Market growth
- Commercial opportunities

Goal:
Understand economic significance.

---

6. RISK ASSESSMENT

Investigate:

- Technical risks
- Business risks
- Ethical risks
- Regulatory risks
- Operational risks

Goal:
Identify vulnerabilities.

---

7. POLICY AND GOVERNANCE

Investigate:

- Regulations
- Standards
- Governance frameworks
- Legal implications
- Compliance challenges

Goal:
Understand governance considerations.

---

8. OPPORTUNITY IDENTIFICATION

Investigate:

- Innovation opportunities
- Research opportunities
- Market opportunities
- Strategic advantages
- Emerging possibilities

Goal:
Identify growth potential.

---

9. FUTURE OUTLOOK

Investigate:

- Emerging trends
- Future developments
- Potential disruptions
- Long-term implications
- Transformational scenarios

Goal:
Understand future evolution.

---

10. KNOWLEDGE GAPS

Investigate:

- Open questions
- Unresolved challenges
- Areas requiring further study
- Missing evidence
- Future research directions

Goal:
Identify what remains unknown.

======================================================================
QUESTION QUALITY REQUIREMENTS
======================================================================

Every question must be:

✓ Research-intensive

✓ Evidence-seeking

✓ Open-ended

✓ Specific

✓ Insight-generating

✓ Publication-oriented

✓ Suitable for professional analysis

✓ Suitable for executive-level reporting

✓ Suitable for academic investigation

✓ Suitable for future forecasting

Avoid:

✗ Yes/No questions

✗ Generic questions

✗ Broad questions

✗ Duplicate questions

✗ Weak exploratory questions

======================================================================
QUESTION GENERATION REQUIREMENTS
======================================================================

Generate between 15 and 20 research questions.

The questions should collectively create a complete research roadmap.

Each question should explore a different aspect of the topic.

The final set should allow a downstream research team to produce:

- Academic papers
- Industry reports
- Whitepapers
- Strategic intelligence reports
- Executive briefings

======================================================================
OUTPUT FORMAT
======================================================================

Return ONLY questions.

Each question MUST begin with:

Q:

Example:

Q: How have transformer-based architectures fundamentally changed modern natural language processing systems?

Q: What technical, economic, and organizational factors influence enterprise adoption of generative AI platforms?

Do not provide explanations.

Do not number the questions.

Do not use markdown.

Return only high-quality research questions.
"""

    response = llm.invoke(prompt)

    questions = []

    for line in response.content.split("\n"):
        line = line.strip()

        if line.startswith("Q:"):
            question = line[2:].strip()

            if (
                question
                and len(question) > 15
                and question not in questions
            ):
                questions.append(question)

        elif line.startswith("-"):
            question = line[1:].strip()

            if (
                question
                and len(question) > 15
                and question not in questions
            ):
                questions.append(question)

    # Professional fallback framework
    if not questions:
        questions = [
            f"What are the foundational principles, theories, and historical developments that define {topic}?",
            f"How has {topic} evolved over time, and what factors have driven its development?",
            f"What is the current state of {topic} across academia, industry, and government sectors?",
            f"What technologies, methodologies, and frameworks are central to modern implementations of {topic}?",
            f"What measurable benefits and strategic advantages does {topic} provide?",
            f"What are the most significant technical challenges and operational limitations associated with {topic}?",
            f"What economic impacts and market opportunities are emerging around {topic}?",
            f"How are leading organizations and institutions leveraging {topic} in real-world applications?",
            f"What ethical, regulatory, and governance concerns surround the adoption of {topic}?",
            f"What risks and vulnerabilities could affect the future success of {topic}?",
            f"What innovations and research breakthroughs are currently shaping the future of {topic}?",
            f"What emerging trends indicate the long-term trajectory of {topic}?",
            f"What industries are expected to experience the greatest transformation due to {topic}?",
            f"What knowledge gaps remain unresolved within the field of {topic}?",
            f"What future research directions are most likely to advance understanding and implementation of {topic}?"
        ]

    # Remove duplicates while preserving order
    unique_questions = []
    seen = set()

    for question in questions:
        normalized = question.lower().strip()

        if normalized not in seen:
            seen.add(normalized)
            unique_questions.append(question)

    return {
        "research_questions": unique_questions[:20],
        "research_plan_metadata": {
            "planner": "Chief Research Planning Officer",
            "topic": topic,
            "generated_questions": len(unique_questions[:20]),
            "planning_status": "completed"
        },
        "current_phase": ResearchPhase.SEARCHING
    }