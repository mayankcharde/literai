import streamlit as st
import requests
import pandas as pd
import time

# API_URL = "http://127.0.0.1:8000"
API_URL = "https://literai-otr8.onrender.com"

st.set_page_config(
    page_title="Multi-Agent Research Assistant",
    page_icon="🔬",
    layout="wide"
)

# Custom CSS for RAG interface
st.markdown("""
<style>
    .rag-answer {
        background: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #667eea;
    }
    .confidence-high {
        color: #00c853;
        font-weight: bold;
    }
    .confidence-medium {
        color: #ffa000;
        font-weight: bold;
    }
    .confidence-low {
        color: #d32f2f;
        font-weight: bold;
    }
    .source-card {
        background: #fafafa;
        padding: 10px;
        border-radius: 8px;
        margin: 5px 0;
        font-size: 0.9em;
    }
    .stButton > button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

st.title("🔬 Multi-Agent Research Assistant")
st.markdown("Research any topic using your LangGraph Multi-Agent Workflow with **RAG Q&A**")

# Initialize session state
if 'rag_ready' not in st.session_state:
    st.session_state.rag_ready = False
if 'current_session_id' not in st.session_state:
    st.session_state.current_session_id = None
if 'research_results' not in st.session_state:
    st.session_state.research_results = None
if 'current_topic' not in st.session_state:
    st.session_state.current_topic = None
if 'rag_question' not in st.session_state:
    st.session_state.rag_question = ""

# Sidebar
st.sidebar.header("Research Settings")

topic = st.text_input(
    "Enter Research Topic",
    placeholder="Example: Impact of Generative AI on Healthcare"
)

col1, col2 = st.sidebar.columns(2)
with col1:
    start_btn = st.button("🚀 Start Research", use_container_width=True)
with col2:
    if st.button("🗑️ Clear", use_container_width=True):
        st.session_state.rag_ready = False
        st.session_state.current_session_id = None
        st.session_state.research_results = None
        st.session_state.current_topic = None
        st.rerun()

if start_btn and not topic.strip():
    st.warning("Please enter a topic")
    st.stop()

if start_btn:
    with st.spinner("🤖 Agents are researching your topic..."):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            status_text.info("🚀 Starting research workflow...")
            progress_bar.progress(10)
            
            response = requests.post(
                f"{API_URL}/research/start",
                json={"topic": topic},
                timeout=1200
            )
            
            progress_bar.progress(50)
            status_text.info("📊 Processing research results...")
            
            if response.status_code != 200:
                st.error(response.text)
                st.stop()

            data = response.json()
            result = data.get("result", {})
            session_id = data.get("session_id")
            
            progress_bar.progress(80)
            status_text.info("🔍 Extracting report data...")
            
            st.session_state.research_results = result
            st.session_state.current_session_id = session_id
            st.session_state.current_topic = topic
            st.session_state.rag_ready = False
            
            progress_bar.progress(100)
            status_text.success("✅ Research Completed Successfully!")
            
            st.balloons()
            time.sleep(1)
            st.rerun()
            
        except Exception as e:
            st.error(str(e))

# Display Research Results
if st.session_state.research_results:
    result = st.session_state.research_results
    topic = st.session_state.current_topic
    
    st.success(f"✅ Research Completed on: **{topic}**")
    
    # Metrics
    quality = result.get("quality_metrics", {})
    
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.metric(
            "Quality Score",
            f"{quality.get('overall_score', 'N/A')}/10"
        )
    with c2:
        st.metric(
            "Questions",
            len(result.get("research_questions", []))
        )
    with c3:
        st.metric(
            "Sources",
            len(result.get("search_results", []))
        )
    with c4:
        st.metric(
            "Iterations",
            result.get("iteration_count", 0)
        )
    
    st.divider()
    
    # Tabs for different sections
    tab1, tab2, tab3 = st.tabs(["📄 Research Report", "📊 Details", "🤖 RAG Q&A"])
    
    with tab1:
        report = (
            result.get("formatted_output")
            or result.get("draft")
            or result.get("summarized_content")
        )
        
        st.header("📄 Final Research Report")
        
        if report:
            st.markdown(report)
            
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    label="⬇ Download Report (MD)",
                    data=report,
                    file_name=f"{topic.replace(' ', '_')}_report.md",
                    mime="text/plain"
                )
            with col2:
                st.download_button(
                    label="⬇ Download Report (JSON)",
                    data=str(result),
                    file_name=f"{topic.replace(' ', '_')}_report.json",
                    mime="application/json"
                )
        else:
            st.warning("No report content available")
    
    with tab2:
        # Summary
        if result.get("summarized_content"):
            st.header("📝 Research Summary")
            st.info(result["summarized_content"])
            st.divider()
        
        # Research Questions
        questions = result.get("research_questions", [])
        if questions:
            st.header("❓ Research Questions")
            for i, q in enumerate(questions, 1):
                st.write(f"**{i}.** {q}")
            st.divider()
        
        # Subtopics
        subtopics = result.get("subtopics", [])
        if subtopics:
            st.header("📚 Subtopics")
            cols = st.columns(2)
            for i, sub in enumerate(subtopics):
                cols[i % 2].write(f"• {sub}")
            st.divider()
        
        # Search Results
        search_results = result.get("search_results", [])
        if search_results:
            st.header("🔍 Search Results")
            for idx, item in enumerate(search_results[:5], 1):
                with st.expander(f"Source {idx}"):
                    if isinstance(item, dict):
                        st.write(f"**Title:** {item.get('title', 'No Title')}")
                        st.write(f"**Content:** {str(item.get('content', item.get('snippet', 'No content')))[:300]}...")
                        if item.get('url'):
                            st.markdown(f"[Open Source]({item['url']})")
                    else:
                        st.write(str(item)[:300])
        
        # Reviewer Feedback
        feedback = result.get("reviewer_feedback", [])
        if feedback:
            st.header("⭐ Reviewer Feedback")
            for item in feedback:
                st.info(item[:300] + "..." if len(item) > 300 else item)
    
    with tab3:
        st.header("🤖 Ask Questions About the Research")
        st.markdown("Use RAG (Retrieval-Augmented Generation) to query the research report")
        
        # Initialize RAG button
        if not st.session_state.rag_ready:
            st.info("Click the button below to initialize the RAG system. This will chunk the report and create a vector store for Q&A.")
            
            if st.button("🔄 Initialize RAG System", use_container_width=True):
                with st.spinner("Setting up RAG system (chunking + vector store)..."):
                    try:
                        response = requests.post(
                            f"{API_URL}/research/rag/setup",
                            params={"session_id": st.session_state.current_session_id},
                            timeout=60
                        )
                        if response.status_code == 200:
                            st.session_state.rag_ready = True
                            st.success("✅ RAG system initialized successfully!")
                            st.rerun()
                        else:
                            st.error(f"Failed to initialize RAG: {response.text}")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        else:
            st.success("✅ RAG system is ready!")
            
            # RAG Statistics
            with st.expander("📊 RAG System Statistics"):
                try:
                    stats_response = requests.get(f"{API_URL}/research/rag/stats", timeout=10)
                    if stats_response.status_code == 200:
                        stats = stats_response.json()
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total Chunks", stats.get("total_chunks", 0))
                        with col2:
                            st.metric("Chunk Size", f"{stats.get('chunk_size', 500)} chars")
                        with col3:
                            st.metric("Overlap", f"{stats.get('chunk_overlap', 100)} chars")
                except:
                    st.caption("Statistics temporarily unavailable")
            
            # Quick Questions
            st.markdown("### 💡 Quick Questions")
            quick_questions = [
                "What are the main findings?",
                "Summarize the conclusion",
                "What methodology was used?",
                "What are the key recommendations?",
                "What limitations are mentioned?"
            ]
            
            cols = st.columns(len(quick_questions))
            for i, q in enumerate(quick_questions):
                with cols[i]:
                    if st.button(q[:15] + "...", key=f"quick_{i}"):
                        st.session_state.rag_question = q
            
            # Question Input
            st.markdown("### ❓ Ask Your Question")
            question = st.text_input(
                "Your question:",
                value=st.session_state.rag_question,
                placeholder="Example: What are the main challenges discussed in this research?",
                key="rag_input"
            )
            
            if st.button("🔍 Get Answer", type="primary", use_container_width=True) and question:
                with st.spinner("Searching the research report..."):
                    try:
                        response = requests.post(
                            f"{API_URL}/research/rag/ask",
                            json={"question": question},
                            timeout=30
                        )
                        
                        if response.status_code == 200:
                            rag_result = response.json()
                            
                            # Display answer
                            st.markdown("### 📝 Answer")
                            st.markdown(f'<div class="rag-answer">{rag_result["answer"]}</div>', unsafe_allow_html=True)
                            
                            # Confidence score
                            confidence = rag_result.get("confidence", 0)
                            if confidence > 0.7:
                                confidence_class = "confidence-high"
                                confidence_text = f"High Confidence: {confidence*100:.0f}%"
                            elif confidence > 0.4:
                                confidence_class = "confidence-medium"
                                confidence_text = f"Medium Confidence: {confidence*100:.0f}%"
                            else:
                                confidence_class = "confidence-low"
                                confidence_text = f"Low Confidence: {confidence*100:.0f}%"
                            
                            st.markdown(f'<p class="{confidence_class}">{confidence_text}</p>', unsafe_allow_html=True)
                            
                            # Sources
                            sources = rag_result.get("sources", [])
                            if sources:
                                with st.expander(f"📚 Sources ({len(sources)} relevant chunks)"):
                                    for i, source in enumerate(sources, 1):
                                        st.markdown(f'<div class="source-card"><b>Source {i}:</b><br>{source["text"]}</div>', unsafe_allow_html=True)
                                        if i < len(sources):
                                            st.divider()
                        else:
                            st.error(f"Error: {response.text}")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            
            # Simple Explanation Feature
            st.markdown("---")
            st.markdown("### 🎓 Simple Explanation")
            st.markdown("Explain a concept from the research in simple terms")
            
            concept = st.text_input(
                "Enter a concept to explain:",
                placeholder="Example: 'Machine Learning', 'Neural Networks', 'Transformer Architecture'",
                key="concept_input"
            )
            
            if st.button("📖 Explain Simply", use_container_width=True) and concept:
                with st.spinner("Creating simple explanation..."):
                    try:
                        response = requests.post(
                            f"{API_URL}/research/rag/explain",
                            json={"concept": concept},
                            timeout=30
                        )
                        
                        if response.status_code == 200:
                            explanation = response.json()
                            st.success(f"✨ Simple explanation of '{concept}':")
                            st.markdown(f'<div class="rag-answer">{explanation["simple_explanation"]}</div>', unsafe_allow_html=True)
                            st.caption(f"Found {explanation.get('sources_found', 0)} relevant sources")
                        else:
                            st.error(f"Error: {response.text}")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")

# Health Check
with st.sidebar:
    st.divider()
    st.markdown("### 🔌 System Status")
    
    try:
        health = requests.get(f"{API_URL}/health", timeout=5).json()
        st.success(f"✅ API: {health['status']}")
        
        if st.session_state.rag_ready:
            st.success("✅ RAG: Ready")
        else:
            st.info("⏳ RAG: Not initialized")
            
    except:
        st.error("❌ Backend Not Running")
        st.info("Start backend: cd backend && python -m uvicorn main:app --reload")
    
    st.divider()
    st.caption("Built with LangGraph | 9 Agents | RAG | Mistral AI")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>Multi-Agent Research Assistant | Powered by LangGraph, Mistral AI, ChromaDB, and RAG</div>",
    unsafe_allow_html=True
)