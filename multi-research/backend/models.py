from typing import TypedDict, List, Annotated, Dict, Any, Optional
import operator
from datetime import datetime
from enum import Enum
from pydantic import BaseModel

class ResearchPhase(str, Enum):
    ORCHESTRATION = "orchestration"
    PLANNING = "planning"
    SEARCHING = "searching"
    ANALYSIS = "analysis"
    WRITING = "writing"
    FACT_CHECKING = "fact_checking"
    REVIEW = "review"
    SUMMARIZATION = "summarization"
    FORMATTING = "formatting"
    COMPLETED = "completed"

class QualityMetrics(BaseModel):
    relevance_score: float = 0.0
    accuracy_score: float = 0.0
    completeness_score: float = 0.0
    clarity_score: float = 0.0
    overall_score: float = 0.0

class AgentMetrics(BaseModel):
    agent_name: str
    start_time: datetime
    end_time: Optional[datetime] = None
    execution_time: float = 0.0
    status: str = "running"
    output_size: int = 0

class ResearchState(TypedDict):
    # Core data
    topic: str
    subtopics: List[str]
    research_questions: List[str]
    search_results: Annotated[List[Dict[str, Any]], operator.add]
    analyzed_data: Dict[str, Any]
    draft: str
    fact_checked_content: str
    reviewed_content: str
    summarized_content: str
    formatted_output: str
    
    # Quality control
    quality_metrics: QualityMetrics
    fact_check_report: Dict[str, Any]
    reviewer_feedback: List[str]
    
    # Workflow control
    current_phase: ResearchPhase
    iteration_count: int
    max_iterations: int
    is_approved: bool
    
    # Agent coordination
    agent_metrics: Annotated[List[AgentMetrics], operator.add]
    parallel_tasks: List[str]
    pending_reviews: List[str]
    
    # Metadata
    metadata: Dict[str, Any]

def create_initial_state(topic: str) -> ResearchState:
    return {
        "topic": topic,
        "subtopics": [],
        "research_questions": [],
        "search_results": [],
        "analyzed_data": {},
        "draft": "",
        "fact_checked_content": "",
        "reviewed_content": "",
        "summarized_content": "",
        "formatted_output": "",
        "quality_metrics": QualityMetrics(),
        "fact_check_report": {},
        "reviewer_feedback": [],
        "current_phase": ResearchPhase.ORCHESTRATION,
        "iteration_count": 0,
        "max_iterations": 3,
        "is_approved": False,
        "agent_metrics": [],
        "parallel_tasks": [],
        "pending_reviews": [],
        "metadata": {
            "created_at": datetime.now().isoformat(),
            "total_agents": 8,
            "version": "2.0"
        }
    }