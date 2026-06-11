# from langgraph.graph import StateGraph, END
# from agents.orchestrator import orchestrator_node
# from agents.planner import planner_node
# from agents.searcher import searcher_node
# from agents.analyzer import analyzer_node
# from agents.writer import writer_node
# from agents.fact_checker import fact_checker_node
# from agents.reviewer import reviewer_node
# from agents.summarizer import summarizer_node
# from agents.formatter import formatter_node
# from models import ResearchState, ResearchPhase, create_initial_state

# def router_after_orchestrator(state: ResearchState):
#     if state.get("parallel_tasks"):
#         return "parallel_execution"
#     return "planner"

# def router_after_fact_check(state: ResearchState):
#     if state.get("iteration_count", 0) >= state.get("max_iterations", 3):
#         return "reviewer"
    
#     fact_check = state.get("fact_check_report", {})
#     if fact_check.get("requires_revision", False):
#         return "writer"
#     return "reviewer"

# def router_after_review(state: ResearchState):
#     if state.get("is_approved", False):
#         return "summarizer"
#     elif state.get("iteration_count", 0) < state.get("max_iterations", 3):
#         return "writer"
#     else:
#         return "summarizer"

# def build_research_graph():
#     """Build the complete multi-agent workflow"""
#     workflow = StateGraph(ResearchState)
    
#     # Add all agent nodes
#     workflow.add_node("orchestrator", orchestrator_node)
#     workflow.add_node("planner", planner_node)
#     workflow.add_node("searcher", searcher_node)
#     workflow.add_node("analyzer", analyzer_node)
#     workflow.add_node("writer", writer_node)
#     workflow.add_node("fact_checker", fact_checker_node)
#     workflow.add_node("reviewer", reviewer_node)
#     workflow.add_node("summarizer", summarizer_node)
#     workflow.add_node("formatter", formatter_node)
    
#     # Add conditional edges
#     workflow.set_entry_point("orchestrator")
    
#     workflow.add_conditional_edges(
#         "orchestrator",
#         router_after_orchestrator,
#         {
#             "parallel_execution": "searcher",
#             "planner": "planner"
#         }
#     )
    
#     # Main workflow edges
#     workflow.add_edge("planner", "searcher")
#     workflow.add_edge("searcher", "analyzer")
#     workflow.add_edge("analyzer", "writer")
#     workflow.add_edge("writer", "fact_checker")
    
#     workflow.add_conditional_edges(
#         "fact_checker",
#         router_after_fact_check,
#         {
#             "writer": "writer",
#             "reviewer": "reviewer"
#         }
#     )
    
#     workflow.add_conditional_edges(
#         "reviewer",
#         router_after_review,
#         {
#             "writer": "writer",
#             "summarizer": "summarizer"
#         }
#     )
    
#     # Final edges
#     workflow.add_edge("summarizer", "formatter")
#     workflow.add_edge("formatter", END)
    
#     return workflow.compile()

# async def run_research_async(topic: str, callback=None):
#     """Run the complete research workflow"""
#     print(f"🚀 Starting research workflow for: {topic}")
    
#     # Create initial state
#     initial_state = create_initial_state(topic)
#     print(f"✅ Initial state created")
    
#     # Build and run graph
#     graph = build_research_graph()
#     print(f"✅ Graph built")
    
#     final_state = None
#     step = 0
    
#     # Use astream for async iteration
#     async for event in graph.astream(initial_state):
#         step += 1
#         print(f"📊 Step {step}: {list(event.keys())}")
        
#         for node_name, node_state in event.items():
#             print(f"   ✓ {node_name} completed")
#             final_state = node_state
            
#             if callback:
#                 phase = node_state.get("current_phase", "unknown")
#                 await callback(f"🔄 {node_name.upper()} completed - Phase: {phase}", "progress")
    
#     print(f"✅ Workflow completed with {step} steps")
    
#     # Return the final state
#     return {"formatter": final_state} if final_state else {}




from langgraph.graph import StateGraph, END
# from langgraph.checkpoint import MemorySaver
from langgraph.checkpoint.memory import MemorySaver
from agents.orchestrator import orchestrator_node
from agents.planner import planner_node
from agents.searcher import searcher_node
from agents.analyzer import analyzer_node
from agents.writer import writer_node
from agents.fact_checker import fact_checker_node
from agents.reviewer import reviewer_node
from agents.summarizer import summarizer_node
from agents.formatter import formatter_node
from models import ResearchState, ResearchPhase, create_initial_state
import asyncio
from typing import Literal

def router_after_orchestrator(state: ResearchState) -> Literal["planner", "searcher", "END"]:
    """Advanced routing after orchestrator based on complexity"""
    complexity = state.get("metadata", {}).get("complexity", "medium")
    parallel_tasks = state.get("parallel_tasks", [])
    
    # If high complexity, go directly to parallel search
    if complexity == "high" or len(parallel_tasks) > 2:
        return "searcher"
    return "planner"

def router_after_analysis(state: ResearchState) -> Literal["writer", "searcher", "planner"]:
    """Route based on analysis quality"""
    analyzed_data = state.get("analyzed_data", {})
    data_points = analyzed_data.get("data_points", 0)
    
    # If insufficient data, go back to search
    if data_points < 3 and state.get("iteration_count", 0) < 2:
        print(" Insufficient data, re-searching...")
        return "searcher"
    # If no analysis, replan
    elif not analyzed_data.get("analysis"):
        return "planner"
    return "writer"

def router_after_fact_check(state: ResearchState) -> Literal["writer", "reviewer", "analyzer"]:
    """Advanced routing after fact checking"""
    iteration = state.get("iteration_count", 0)
    max_iterations = state.get("max_iterations", 3)
    fact_check = state.get("fact_check_report", {})
    
    # Critical errors - need rewrite
    if fact_check.get("requires_revision", False) and iteration < max_iterations:
        print(f" Fact check failed, revising (iteration {iteration + 1})")
        return "writer"
    
    # Minor issues - can proceed but note
    elif fact_check.get("overall_accuracy") == "low":
        print(" Low accuracy, but proceeding with reviewer")
        return "reviewer"
    
    # Perfect - proceed
    return "reviewer"

def router_after_review(state: ResearchState) -> Literal["writer", "summarizer", "analyzer", "END"]:
    """Advanced routing based on review feedback"""
    is_approved = state.get("is_approved", False)
    iteration = state.get("iteration_count", 0)
    max_iterations = state.get("max_iterations", 3)
    quality_score = state.get("quality_metrics", {}).get("overall_score", 0)
    
    # Approved with high quality
    if is_approved and quality_score >= 7:
        print("Report approved with high quality, proceeding to summarization")
        return "summarizer"
    
    # Approved but low quality - revise
    elif is_approved and quality_score < 7 and iteration < max_iterations:
        print(" Approved but low quality, revising...")
        return "writer"
    
    # Not approved but can revise
    elif not is_approved and iteration < max_iterations:
        print(f" Revision needed (iteration {iteration + 1}/{max_iterations})")
        return "writer"
    
    # Max iterations reached - force complete
    elif iteration >= max_iterations:
        print(" Max iterations reached, forcing completion")
        return "summarizer"
    
    return "summarizer"

def router_after_summary(state: ResearchState) -> Literal["formatter", "writer"]:
    """Route after summarization"""
    summary = state.get("summarized_content", "")
    
    # If summary is too short, go back to writer
    if len(summary) < 100 and state.get("iteration_count", 0) < 2:
        print(" Summary too short, returning to writer")
        return "writer"
    return "formatter"

def build_research_graph():
    """Build the complete multi-agent workflow with advanced routing"""
    workflow = StateGraph(ResearchState)
    
    # Add all agent nodes
    workflow.add_node("orchestrator", orchestrator_node)
    workflow.add_node("planner", planner_node)
    workflow.add_node("searcher", searcher_node)
    workflow.add_node("analyzer", analyzer_node)
    workflow.add_node("writer", writer_node)
    workflow.add_node("fact_checker", fact_checker_node)
    workflow.add_node("reviewer", reviewer_node)
    workflow.add_node("summarizer", summarizer_node)
    workflow.add_node("formatter", formatter_node)
    
    # Entry point
    workflow.set_entry_point("orchestrator")
    
    # Conditional routing from orchestrator
    workflow.add_conditional_edges(
        "orchestrator",
        router_after_orchestrator,
        {
            "planner": "planner",
            "searcher": "searcher",
            "END": END
        }
    )
    
    # Planner -> Searcher
    workflow.add_edge("planner", "searcher")
    
    # Searcher -> Analyzer
    workflow.add_edge("searcher", "analyzer")
    
    # Advanced routing from analyzer
    workflow.add_conditional_edges(
        "analyzer",
        router_after_analysis,
        {
            "writer": "writer",
            "searcher": "searcher",
            "planner": "planner"
        }
    )
    
    # Writer -> Fact Checker
    workflow.add_edge("writer", "fact_checker")
    
    # Advanced routing from fact checker
    workflow.add_conditional_edges(
        "fact_checker",
        router_after_fact_check,
        {
            "writer": "writer",
            "reviewer": "reviewer",
            "analyzer": "analyzer"
        }
    )
    
    # Advanced routing from reviewer
    workflow.add_conditional_edges(
        "reviewer",
        router_after_review,
        {
            "writer": "writer",
            "summarizer": "summarizer",
            "analyzer": "analyzer",
            "END": END
        }
    )
    
    # Advanced routing from summarizer
    workflow.add_conditional_edges(
        "summarizer",
        router_after_summary,
        {
            "formatter": "formatter",
            "writer": "writer"
        }
    )
    
    # Formatter -> END
    workflow.add_edge("formatter", END)
    
    # Add checkpointing for state persistence
    memory = MemorySaver()
    
    return workflow.compile(checkpointer=memory)

async def run_research_async(topic: str, callback=None, thread_id: str = None):
    """Run the complete research workflow with checkpointing"""
    import uuid
    from langgraph.types import Command
    
    thread_id = thread_id or str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    print(f" Starting research workflow for: {topic}")
    print(f" Thread ID: {thread_id}")
    
    # Create initial state
    initial_state = create_initial_state(topic)
    print(f" Initial state created")
    
    # Build graph
    graph = build_research_graph()
    print(f" Graph built with checkpointing")
    
    final_state = None
    step = 0
    errors = []
    
    try:
        # Run with streaming
        async for event in graph.astream(initial_state, config=config):
            step += 1
            print(f"\n Step {step}: {list(event.keys())}")
            
            for node_name, node_state in event.items():
                print(f"   ✓ {node_name} completed")
                final_state = node_state
                
                # Track progress
                if callback:
                    phase = node_state.get("current_phase", "unknown")
                    iteration = node_state.get("iteration_count", 0)
                    await callback(
                        f" {node_name.upper()} - Phase: {phase}, Iteration: {iteration}", 
                        "progress"
                    )
                
                # Check for errors in state
                if node_state.get("error"):
                    errors.append(f"{node_name}: {node_state['error']}")
                    print(f"    Error in {node_name}: {node_state['error']}")
        
        print(f"\n Workflow completed with {step} steps")
        
        if errors:
            print(f"⚠️ Completed with {len(errors)} warnings")
        
        # Return final state with metadata
        return {
            "formatter": final_state,
            "metadata": {
                "thread_id": thread_id,
                "total_steps": step,
                "errors": errors,
                "completed": True
            }
        } if final_state else {
            "error": "No final state generated",
            "metadata": {"thread_id": thread_id, "total_steps": step}
        }
        
    except Exception as e:
        print(f" Workflow failed: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return {
            "error": str(e),
            "metadata": {
                "thread_id": thread_id,
                "total_steps": step,
                "completed": False
            }
        }

async def resume_research_async(thread_id: str, callback=None):
    """Resume a previously interrupted research workflow"""
    config = {"configurable": {"thread_id": thread_id}}
    graph = build_research_graph()
    
    print(f" Resuming research for thread: {thread_id}")
    
    final_state = None
    step = 0
    
    async for event in graph.astream(None, config=config):
        step += 1
        for node_name, node_state in event.items():
            final_state = node_state
            if callback:
                await callback(f" Resumed {node_name}", "progress")
    
    return {"formatter": final_state} if final_state else {}