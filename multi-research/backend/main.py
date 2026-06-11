from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
import uuid
from datetime import datetime
import sys
from pathlib import Path


# Add these imports to existing main.py
from rag_engine import ResearchRAGEngine
import json


# Initialize RAG engine globally
rag_engine = ResearchRAGEngine(chunk_size=500, chunk_overlap=100)

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
async def setup_rag_from_research(session_id: str):
    """Setup RAG from a completed research session"""
    if session_id not in research_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = research_sessions[session_id]
    if session["status"] != "completed":
        raise HTTPException(status_code=400, detail="Research not completed")
    
    result = session.get("result", {})
    report = result.get("formatted_output") or result.get("draft", "")
    
    if not report:
        raise HTTPException(status_code=400, detail="No report content found")
    
    # Setup RAG engine
    try:
        rag_engine.create_vectorstore(
            report=report,
            metadata={
                "session_id": session_id,
                "topic": session["topic"],
                "created_at": session.get("completed_at", "")
            }
        )
        
        return {
            "status": "success",
            "message": "RAG system initialized",
            "stats": rag_engine.get_chunk_statistics()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/research/rag/ask")
async def ask_question(question_data: dict):
    """Ask a question about the research report"""
    question = question_data.get("question")
    
    if not question:
        raise HTTPException(status_code=400, detail="Question required")
    
    try:
        result = rag_engine.ask_question(question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/research/rag/summary")
async def get_rag_summary():
    """Get a summary from the RAG system"""
    try:
        summary = rag_engine.get_summary()
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/research/rag/stats")
async def get_rag_stats():
    """Get RAG system statistics"""
    try:
        stats = rag_engine.get_chunk_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/research/rag/explain")
async def explain_simply(concept_data: dict):
    """Explain a concept from the report in simple terms"""
    concept = concept_data.get("concept")
    
    if not concept:
        raise HTTPException(status_code=400, detail="Concept required")
    
    # Search for relevant chunks about the concept
    if not rag_engine.vectorstore:
        raise HTTPException(status_code=400, detail="RAG not initialized")
    
    results = rag_engine.vectorstore.similarity_search(concept, k=3)
    context = "\n".join([doc.page_content for doc in results])
    
    # Use LLM for simple explanation
    from llm_setup import get_mistral_llm
    llm = get_mistral_llm(temperature=0.5)
    
    prompt = f"""
    Explain the concept "{concept}" in VERY simple terms (like explaining to a 12-year-old):
    
    Context from the research:
    {context[:1000]}
    
    Provide:
    1. Simple definition (1 sentence)
    2. Real-world example
    3. Why it matters (1 sentence)
    
    Keep it under 150 words total.
    """
    
    response = llm.invoke(prompt)
    
    return {
        "concept": concept,
        "simple_explanation": response.content,
        "sources_found": len(results)
    }
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)