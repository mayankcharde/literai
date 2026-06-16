from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
import uuid
from datetime import datetime
import sys
from pathlib import Path
import os


# Add these imports to existing main.py
from rag_engine import ResearchRAGEngine
import json


# Store RAG engines per research/session ID
rag_engines: Dict[str, ResearchRAGEngine] = {}

# New Pydantic models for RAG
class RAGSetupRequest(BaseModel):
    research_id: Optional[str] = None
    session_id: Optional[str] = None
    report: str
    topic: Optional[str] = ""

class RAGAskRequest(BaseModel):
    research_id: Optional[str] = None
    session_id: Optional[str] = None
    question: str

# Add backend directory to path
sys.path.insert(0, str(Path(__file__).parent))

from graph.research_graph import run_research_async

app = FastAPI(title="Multi-Agent Research Assistant API", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store research sessions
research_sessions: Dict[str, Dict[str, Any]] = {}

class ResearchRequest(BaseModel):
    topic: str
    session_id: Optional[str] = None

class ResearchResponse(BaseModel):
    session_id: str
    status: str
    result: Optional[Dict[str, Any]] = None
    message: str

@app.get("/")
async def root():
    return {"message": "Multi-Agent Research Assistant API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/research/start", response_model=ResearchResponse)
async def start_research(request: ResearchRequest):
    """Start a new research task"""
    session_id = request.session_id or str(uuid.uuid4())
    
    try:
        research_sessions[session_id] = {
            "topic": request.topic,
            "status": "running",
            "started_at": datetime.now().isoformat(),
            "result": None
        }
        
        print(f"🔬 Starting research on: {request.topic}")
        
        # Run research
        result = await run_research_async(request.topic)
        
        print(f"📊 Research completed. Result type: {type(result)}")
        print(f"Result keys: {result.keys() if isinstance(result, dict) else 'Not a dict'}")
        
        # Extract the final state properly
        final_state = {}
        
        if isinstance(result, dict):
            # Try to find the formatter output (last node)
            if "formatter" in result and isinstance(result["formatter"], dict):
                final_state = result["formatter"]
                print("✅ Found formatter state")
            elif "summarizer" in result and isinstance(result["summarizer"], dict):
                final_state = result["summarizer"]
                print("✅ Found summarizer state")
            elif "reviewer" in result and isinstance(result["reviewer"], dict):
                final_state = result["reviewer"]
                print("✅ Found reviewer state")
            else:
                # Get the last state from workflow
                for key in ["formatter", "summarizer", "reviewer", "writer", "fact_checker"]:
                    if key in result and isinstance(result[key], dict):
                        final_state = result[key]
                        print(f"✅ Found {key} state")
                        break
                
                if not final_state:
                    # Take the last key's value
                    last_key = list(result.keys())[-1] if result.keys() else None
                    if last_key and isinstance(result[last_key], dict):
                        final_state = result[last_key]
                        print(f"✅ Using last state: {last_key}")
                    else:
                        final_state = result
                        print("⚠️ Using entire result as state")
        
        # Ensure we have a dictionary
        if not isinstance(final_state, dict):
            final_state = {}
        
        # Build clean result with all data
        clean_result = {
            "topic": request.topic,
            "formatted_output": final_state.get("formatted_output", ""),
            "summarized_content": final_state.get("summarized_content", ""),
            "draft": final_state.get("draft", ""),
            "fact_checked_content": final_state.get("fact_checked_content", ""),
            "research_questions": final_state.get("research_questions", []),
            "search_results": final_state.get("search_results", []),
            "quality_metrics": final_state.get("quality_metrics", {}),
            "iteration_count": final_state.get("iteration_count", 0),
            "subtopics": final_state.get("subtopics", []),
            "analyzed_data": final_state.get("analyzed_data", {}),
            "reviewer_feedback": final_state.get("reviewer_feedback", []),
            "metadata": final_state.get("metadata", {}),
            "is_approved": final_state.get("is_approved", False)
        }
        
        # Log what we found
        print(f"📝 Report length: {len(clean_result['formatted_output'])} chars")
        print(f"📋 Questions: {len(clean_result['research_questions'])}")
        print(f"🔍 Search results: {len(clean_result['search_results'])}")
        print(f"⭐ Quality score: {clean_result['quality_metrics'].get('overall_score', 'N/A')}")
        
        research_sessions[session_id]["status"] = "completed"
        research_sessions[session_id]["result"] = clean_result
        research_sessions[session_id]["completed_at"] = datetime.now().isoformat()
        
        return ResearchResponse(
            session_id=session_id,
            status="completed",
            result=clean_result,
            message="Research completed successfully"
        )
        
    except Exception as e:
        print(f"❌ Error in research: {str(e)}")
        import traceback
        traceback.print_exc()
        
        research_sessions[session_id]["status"] = "failed"
        research_sessions[session_id]["error"] = str(e)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/research/status/{session_id}")
async def get_research_status(session_id: str):
    if session_id not in research_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = research_sessions[session_id]
    return {
        "session_id": session_id,
        "status": session["status"],
        "topic": session["topic"],
        "started_at": session.get("started_at"),
        "completed_at": session.get("completed_at"),
        "has_result": session.get("result") is not None
    }

@app.get("/research/result/{session_id}")
async def get_research_result(session_id: str):
    if session_id not in research_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = research_sessions[session_id]
    if session["status"] != "completed":
        raise HTTPException(status_code=400, detail="Research not completed yet")
    
    return session.get("result", {})

@app.get("/research/sessions")
async def list_sessions():
    return {
        "sessions": [
            {
                "session_id": sid,
                "topic": session["topic"],
                "status": session["status"],
                "started_at": session.get("started_at")
            }
            for sid, session in research_sessions.items()
        ]
    }
    

#***********************RAG END POINTS****************************************************************************

# Add these new endpoints after your existing ones

@app.post("/research/rag/setup")
async def setup_rag(request: RAGSetupRequest):
    """Setup RAG with report text directly. Accepts either research_id or session_id."""
    # Get the ID (research_id takes priority if both are provided)
    id_value = request.research_id or request.session_id
    if not id_value:
        raise HTTPException(status_code=400, detail="Either research_id or session_id is required")
    
    if not request.report:
        raise HTTPException(status_code=400, detail="Report content is required")
    
    try:
        # Create a new RAG engine for this ID
        rag_engine = ResearchRAGEngine(chunk_size=500, chunk_overlap=100)
        rag_engine.create_vectorstore(
            report=request.report,
            metadata={
                "id": id_value,
                "topic": request.topic,
                "created_at": datetime.now().isoformat()
            }
        )
        rag_engines[id_value] = rag_engine
        
        return {
            "status": "success",
            "message": "RAG system initialized",
            "id": id_value,
            "stats": rag_engine.get_chunk_statistics()
        }
    except Exception as e:
        print(f"RAG setup error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/research/rag/ask")
async def ask_question(request: RAGAskRequest):
    """Ask a question about a specific research report. Accepts either research_id or session_id."""
    if not request.question:
        raise HTTPException(status_code=400, detail="Question required")
    
    id_value = request.research_id or request.session_id
    if not id_value:
        raise HTTPException(status_code=400, detail="Either research_id or session_id is required")
    
    try:
        rag_engine = rag_engines.get(id_value)
        if not rag_engine or not rag_engine.is_initialized:
            raise HTTPException(status_code=400, detail="RAG not initialized for this research/session. Please call /research/rag/setup first.")
        
        result = rag_engine.ask_question(request.question)
        return result
    except HTTPException:
        raise
    except Exception as e:
        print(f"RAG ask error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/research/rag/summary")
async def get_rag_summary(
    research_id: Optional[str] = None, 
    session_id: Optional[str] = None, 
    report: Optional[str] = None
):
    """Get a summary from a specific RAG system, or generate directly from report."""
    try:
        id_value = research_id or session_id
        
        if id_value and id_value in rag_engines:
            rag_engine = rag_engines.get(id_value)
            if rag_engine and rag_engine.is_initialized:
                summary = rag_engine.get_summary()
                return {"summary": summary}
        
        # If no engine, generate simple summary from report
        if report:
            simple_summary = report[:1000] + ("..." if len(report) > 1000 else "")
            return {"summary": simple_summary}
        
        raise HTTPException(status_code=400, detail="Either research_id/session_id with initialized RAG or report is required")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/research/rag/stats")
async def get_rag_stats(
    research_id: Optional[str] = None, 
    session_id: Optional[str] = None
):
    """Get RAG system statistics for a specific research/session."""
    try:
        id_value = research_id or session_id
        if not id_value:
            raise HTTPException(status_code=400, detail="Either research_id or session_id is required")
            
        rag_engine = rag_engines.get(id_value)
        if not rag_engine:
            raise HTTPException(status_code=400, detail="RAG not initialized for this research/session")
        
        stats = rag_engine.get_chunk_statistics()
        return stats
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

if __name__ == "__main__":
    import uvicorn
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    # Get host and port from environment variables, with defaults
    host = os.getenv("HOST", "0.0.0.0")  # Use 0.0.0.0 for production, 127.0.0.1 for local
    port = int(os.getenv("PORT", "8000"))
    
    # Run with production-ready settings
    uvicorn.run(
        app, 
        host=host, 
        port=port, 
        reload=False,  # Always disable reload in production
        timeout_keep_alive=600
    )
