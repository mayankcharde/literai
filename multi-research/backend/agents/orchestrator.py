from llm_setup import get_mistral_llm
from models import ResearchState, ResearchPhase
import json

def orchestrator_node(state: ResearchState):
    print(f"🎯 Orchestrator processing topic: {state['topic']}")

    llm = get_mistral_llm(temperature=0.3)

    prompt = f"""
You are the Chief Research Orchestrator of an advanced Multi-Agent AI Research System.

Your responsibility is to design a comprehensive research execution plan for the topic provided below.

You act as a senior research strategist responsible for:

- Research planning
- Topic decomposition
- Task distribution
- Agent coordination
- Information coverage optimization
- Knowledge gap reduction

======================================================================
RESEARCH TOPIC
======================================================================

{state['topic']}

======================================================================
OBJECTIVE
======================================================================

Analyze the research topic and create a complete research strategy.

Break the topic into logical, non-overlapping research areas that collectively provide full topic coverage.

Think like:

- Senior Research Analyst
- Academic Research Planner
- Industry Intelligence Strategist
- Technical Research Director

======================================================================
RESEARCH DECOMPOSITION FRAMEWORK
======================================================================

Generate research areas covering:

1. Fundamental Concepts
   - Definitions
   - Background
   - Core principles

2. Current State
   - Present landscape
   - Existing solutions
   - Current technologies
   - Industry adoption

3. Trends and Innovations
   - Emerging developments
   - Recent breakthroughs
   - Market trends
   - Research directions

4. Challenges and Limitations
   - Technical barriers
   - Risks
   - Constraints
   - Open problems

5. Future Outlook
   - Predictions
   - Future developments
   - Growth opportunities

6. Real-World Applications
   - Industry use cases
   - Business impact
   - Practical implementations

======================================================================
SUBTOPIC GENERATION RULES
======================================================================

Generate between 4 and 8 highly focused research subtopics.

Requirements:

- No overlap between subtopics
- Comprehensive coverage
- Logical progression
- Research-friendly wording
- Search-engine optimized phrasing

Each subtopic should be specific enough for an independent research agent.

======================================================================
PARALLEL AGENT PLANNING
======================================================================

Recommend which specialized agents should participate.

Available agent types:

- searcher
- analyzer
- fact_checker
- reviewer
- summarizer
- trend_analyst
- technical_expert
- market_researcher
- risk_analyst
- citation_validator

Choose only the agents that would add value for this topic.

======================================================================
OUTPUT FORMAT
======================================================================

Return ONLY valid JSON.

Use this exact structure:

{{
    "research_complexity": "low|medium|high",
    "research_domain": "",
    "estimated_research_depth": "basic|standard|advanced",
    "subtopics": [
        "",
        "",
        "",
        ""
    ],
    "parallel_agents": [
        ""
    ],
    "research_objectives": [
        ""
    ],
    "expected_deliverables": [
        ""
    ]
}}

Return valid JSON only.
"""

    try:
        response = llm.invoke(prompt)
        content = response.content.strip()

        json_start = content.find("{")
        json_end = content.rfind("}") + 1

        if json_start != -1 and json_end > json_start:
            plan = json.loads(content[json_start:json_end])

            subtopics = plan.get("subtopics", [])
            parallel_agents = plan.get("parallel_agents", [])
            research_complexity = plan.get("research_complexity", "medium")
            research_domain = plan.get("research_domain", "General")
            research_depth = plan.get("estimated_research_depth", "standard")

        else:
            raise ValueError("No valid JSON returned")

    except Exception as e:
        print(f"Error in orchestrator: {e}")

        subtopics = []
        parallel_agents = []

        research_complexity = "medium"
        research_domain = "General"
        research_depth = "standard"

    # Fallback Plan
    if not subtopics:
        topic = state["topic"]

        subtopics = [
            f"Fundamentals and Core Concepts of {topic}",
            f"Current Technologies and Industry Landscape of {topic}",
            f"Challenges, Risks, and Limitations in {topic}",
            f"Future Trends and Emerging Innovations in {topic}",
            f"Real-World Applications and Case Studies of {topic}",
            f"Strategic Opportunities and Future Outlook of {topic}"
        ]

    if not parallel_agents:
        parallel_agents = [
            "searcher",
            "analyzer",
            "fact_checker",
            "reviewer",
            "summarizer"
        ]

    print(f"   Generated {len(subtopics)} research subtopics")
    print(f"   Assigned {len(parallel_agents)} agents")

    return {
        "subtopics": subtopics[:8],
        "parallel_tasks": parallel_agents,
        "research_plan": {
            "complexity": research_complexity,
            "domain": research_domain,
            "depth": research_depth,
            "total_subtopics": len(subtopics)
        },
        "current_phase": ResearchPhase.PLANNING
    }