from tools.search_tools import parallel_search, advanced_search
from models import ResearchState, ResearchPhase
import asyncio
import nest_asyncio
from collections import defaultdict


async def searcher_node_async(state: ResearchState):
    """
    Global Research Intelligence Collector (GRIC)

    Responsibilities:
    - Execute multi-dimensional research searches
    - Gather high-quality evidence
    - Expand promising findings
    - Improve source diversity
    - Maximize research coverage
    - Discover trends, risks, opportunities, and future directions
    - Build a comprehensive research evidence base
    """

    topic = state.get("topic", "")
    research_questions = state.get("research_questions", [])

    # ==========================================================
    # RESEARCH DIMENSIONS
    # ==========================================================

    research_dimensions = [
        "technical overview",
        "industry applications",
        "market analysis",
        "economic impact",
        "research papers",
        "case studies",
        "expert opinions",
        "current developments",
        "future trends",
        "risks and challenges",
        "opportunities and benefits",
        "emerging innovations"
    ]

    # ==========================================================
    # BUILD EXPANDED QUERY SET
    # ==========================================================

    expanded_queries = []

    if research_questions:

        for question in research_questions[:10]:

            expanded_queries.append(question)

            for dimension in research_dimensions:
                expanded_queries.append(
                    f"{question} {dimension}"
                )

    else:

        expanded_queries = [
            f"{topic} overview",
            f"{topic} technical analysis",
            f"{topic} industry applications",
            f"{topic} market trends",
            f"{topic} risks and challenges",
            f"{topic} future developments",
            f"{topic} research papers",
            f"{topic} expert analysis"
        ]

    # Remove duplicates while preserving order
    unique_queries = []
    seen_queries = set()

    for query in expanded_queries:
        normalized = query.lower().strip()

        if normalized not in seen_queries:
            seen_queries.add(normalized)
            unique_queries.append(query)

    # Limit search workload
    search_queries = unique_queries[:25]

    print(
        f"🔎 Global Research Intelligence Collector"
    )
    print(
        f"📚 Executing {len(search_queries)} research queries"
    )

    # ==========================================================
    # PHASE 1: PRIMARY PARALLEL SEARCH
    # ==========================================================

    primary_results = await parallel_search(
        search_queries,
        max_concurrent=5
    )

    enriched_results = []
    processed_titles = set()
    topic_clusters = defaultdict(list)

    # ==========================================================
    # PHASE 2: RESULT PROCESSING
    # ==========================================================

    for result in primary_results:

        if not isinstance(result, dict):
            continue

        if "error" in result:
            enriched_results.append(result)
            continue

        # Relevance Scoring
        relevance_score = 0

        if result.get("answer"):
            relevance_score += 5

        if result.get("results"):
            relevance_score += min(
                len(result["results"]),
                5
            )

        result["relevance_score"] = relevance_score

        enriched_results.append(result)

        # ======================================================
        # RESULT ENRICHMENT
        # ======================================================

        try:

            search_items = result.get("results", [])

            if not search_items:
                continue

            top_result = search_items[0]

            title = (
                top_result.get("title", "")
                .strip()
            )

            if not title:
                continue

            normalized_title = title.lower()

            if normalized_title in processed_titles:
                continue

            processed_titles.add(normalized_title)

            topic_clusters["primary_sources"].append(
                title
            )

            # ==================================================
            # ADVANCED FOLLOW-UP INVESTIGATION
            # ==================================================

            followup_queries = [
                f"{title} detailed technical analysis",
                f"{title} industry applications",
                f"{title} market trends and adoption",
                f"{title} risks and limitations",
                f"{title} future developments",
                f"{title} research challenges",
                f"{title} case studies",
                f"{title} expert opinions"
            ]

            for query in followup_queries:

                try:

                    followup_result = advanced_search(
                        query
                    )

                    if followup_result:

                        enriched_results.append({
                            "source_type": "followup_research",
                            "parent_title": title,
                            "query": query,
                            "relevance_score": 8,
                            "data": followup_result
                        })

                except Exception as e:
                    print(
                        f"⚠️ Follow-up search failed: {str(e)}"
                    )

        except Exception as e:
            print(
                f"⚠️ Result enrichment failed: {str(e)}"
            )

    # ==========================================================
    # PHASE 3: KNOWLEDGE DISCOVERY SEARCHES
    # ==========================================================

    discovery_queries = [
        f"{topic} latest breakthroughs",
        f"{topic} future predictions",
        f"{topic} emerging technologies",
        f"{topic} strategic opportunities",
        f"{topic} industry transformation"
    ]

    for query in discovery_queries:

        try:

            discovery_result = advanced_search(query)

            if discovery_result:

                enriched_results.append({
                    "source_type": "discovery_search",
                    "query": query,
                    "relevance_score": 9,
                    "data": discovery_result
                })

        except Exception:
            pass

    # ==========================================================
    # PHASE 4: QUALITY METRICS
    # ==========================================================

    successful_searches = sum(
        1
        for r in enriched_results
        if isinstance(r, dict)
        and "error" not in r
    )

    failed_searches = sum(
        1
        for r in enriched_results
        if isinstance(r, dict)
        and "error" in r
    )

    average_relevance = 0

    scored_results = [
        r.get("relevance_score", 0)
        for r in enriched_results
        if isinstance(r, dict)
    ]

    if scored_results:
        average_relevance = round(
            sum(scored_results)
            / len(scored_results),
            2
        )

    search_metadata = {
        "agent_name":
            "Global Research Intelligence Collector",

        "topic": topic,

        "queries_executed":
            len(search_queries),

        "successful_searches":
            successful_searches,

        "failed_searches":
            failed_searches,

        "total_results_collected":
            len(enriched_results),

        "average_relevance_score":
            average_relevance,

        "coverage_level":
            "High",

        "research_dimensions":
            len(research_dimensions),

        "search_status":
            "Completed"
    }

    print(
        f"✅ Research Collection Complete"
    )
    print(
        f"📊 Results Collected: {len(enriched_results)}"
    )
    print(
        f"🎯 Avg Relevance Score: {average_relevance}"
    )

    return {
        "search_results": enriched_results,
        "search_metadata": search_metadata,
        "current_phase": ResearchPhase.ANALYSIS
    }


def searcher_node(state: ResearchState):
    """
    Wrapper for async search execution.

    Supports:
    - LangGraph
    - FastAPI
    - Streamlit
    - Jupyter
    - Google Colab
    - Standard Python
    """

    try:

        loop = asyncio.get_running_loop()

        if loop.is_running():
            nest_asyncio.apply()
            return asyncio.run(
                searcher_node_async(state)
            )

    except RuntimeError:
        pass

    return asyncio.run(
        searcher_node_async(state)
    )