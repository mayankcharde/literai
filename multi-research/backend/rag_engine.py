# import hashlib
# from typing import List, Dict, Any, Optional
# from dataclasses import dataclass
# import numpy as np

# # RAG imports with correct modern paths
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_community.vectorstores import Chroma
# from langchain_mistralai import ChatMistralAI
# # from langchain.chains import RetrievalQA
# from langchain_classic.chains import RetrievalQA
# from langchain_core.prompts import PromptTemplate

# import os
# from dotenv import load_dotenv

# load_dotenv()

# @dataclass
# class ChunkInfo:
#     """Information about a text chunk"""
#     id: str
#     text: str
#     metadata: Dict[str, Any]
#     start_idx: int
#     end_idx: int

# class ResearchRAGEngine:
#     """RAG Engine for research report with chunking and Q&A"""
    
#     def __init__(self, chunk_size: int = 400, chunk_overlap: int = 40):
#         self.chunk_size = chunk_size
#         self.chunk_overlap = chunk_overlap
#         self.vectorstore = None
#         self.qa_chain = None
        
#         # Initialize embeddings with error handling
#         try:
#             self.embeddings = HuggingFaceEmbeddings(
#                 model_name="sentence-transformers/all-MiniLM-L6-v2",
#                 model_kwargs={'device': 'cpu'}
#             )
#         except Exception as e:
#             print(f"Warning: Could not load embeddings: {e}")
#             self.embeddings = None
            
#         # Initialize LLM
#         api_key = os.getenv("MISTRAL_API_KEY")
#         if not api_key:
#             print("Warning: MISTRAL_API_KEY not found in environment variables")
        
#         try:
#             self.llm = ChatMistralAI(
#                 model="mistral-large-latest",
#                 temperature=0.3,
#                 api_key=api_key
#             )
#         except Exception as e:
#             print(f"Warning: Could not initialize LLM: {e}")
#             self.llm = None
        
#     def chunk_report(self, report: str, metadata: Optional[Dict] = None) -> List[ChunkInfo]:
#         """
#         Split the research report into semantic chunks
#         """
#         if not report:
#             return []
        
#         # Use LangChain's text splitter
#         text_splitter = RecursiveCharacterTextSplitter(
#             chunk_size=self.chunk_size,
#             chunk_overlap=self.chunk_overlap,
#             length_function=len,
#             separators=["\n\n", "\n", ".", " ", ""],
#             add_start_index=True
#         )
        
#         # Create chunks
#         chunks = text_splitter.create_documents(
#             [report],
#             metadatas=[metadata or {}]
#         )
        
#         chunk_infos = []
#         for i, chunk in enumerate(chunks):
#             chunk_info = ChunkInfo(
#                 id=hashlib.md5(chunk.page_content.encode()).hexdigest(),
#                 text=chunk.page_content,
#                 metadata={
#                     "chunk_id": i,
#                     "total_chunks": len(chunks),
#                     "chunk_size": len(chunk.page_content),
#                     **chunk.metadata
#                 },
#                 start_idx=chunk.metadata.get("start_index", 0),
#                 end_idx=chunk.metadata.get("end_index", len(chunk.page_content))
#             )
#             chunk_infos.append(chunk_info)
        
#         return chunk_infos
    
#     def create_vectorstore(self, report: str, metadata: Optional[Dict] = None) -> None:
#         """
#         Create a vector store from the chunked report
#         """
#         if not report:
#             raise ValueError("Report content is empty")
        
#         if not self.embeddings:
#             raise ValueError("Embeddings model not loaded")
        
#         print(f"📚 Creating vector store from report...")
        
#         # Chunk the report
#         chunks = self.chunk_report(report, metadata)
#         print(f"✅ Created {len(chunks)} chunks (size: {self.chunk_size}, overlap: {self.chunk_overlap})")
        
#         if len(chunks) == 0:
#             raise ValueError("No chunks created from report")
        
#         # Create vector store
#         texts = [chunk.text for chunk in chunks]
#         metadatas = [chunk.metadata for chunk in chunks]
        
#         try:
#             self.vectorstore = Chroma.from_texts(
#                 texts=texts,
#                 embedding=self.embeddings,
#                 metadatas=metadatas,
#                 persist_directory="./research_chroma_db"
#             )
#         except Exception as e:
#             print(f"Error creating vector store: {e}")
#             raise
        
#         # Create QA chain with custom prompt
#         prompt_template = """
#         You are an AI assistant specialized in explaining research reports in easy-to-understand language.
        
#         Context from the research report:
#         {context}
        
#         Question: {question}
        
#         Instructions:
#         1. Answer based ONLY on the provided context
#         2. If the answer is not in the context, say "The research report doesn't contain information about this"
#         3. Explain in simple, easy-to-understand language (avoid jargon)
#         4. Use examples if helpful
#         5. Keep answers concise but comprehensive
        
#         Answer:
#         """
        
#         PROMPT = PromptTemplate(
#             template=prompt_template,
#             input_variables=["context", "question"]
#         )
        
#         self.qa_chain = RetrievalQA.from_chain_type(
#             llm=self.llm,
#             chain_type="stuff",
#             retriever=self.vectorstore.as_retriever(search_kwargs={"k": 4}),
#             chain_type_kwargs={"prompt": PROMPT},
#             return_source_documents=True
#         )
        
#         print(f"✅ Vector store created and ready for Q&A")
        
#     def ask_question(self, question: str) -> Dict[str, Any]:
#         """
#         Ask a question about the research report
#         """
#         if not self.qa_chain:
#             return {
#                 "answer": "Please load a research report first. Click 'Initialize RAG' button.",
#                 "sources": [],
#                 "confidence": 0,
#                 "question": question
#             }
        
#         if not question or not question.strip():
#             return {
#                 "answer": "Please enter a valid question.",
#                 "sources": [],
#                 "confidence": 0,
#                 "question": question
#             }
        
#         print(f"❓ Answering: {question}")
        
#         try:
#             # Get answer from RAG
#             result = self.qa_chain({"query": question})
            
#             # Extract source chunks
#             sources = []
#             for doc in result.get("source_documents", []):
#                 sources.append({
#                     "text": doc.page_content[:300] + "..." if len(doc.page_content) > 300 else doc.page_content,
#                     "metadata": doc.metadata
#                 })
            
#             # Calculate confidence (based on source relevance)
#             confidence = min(1.0, len(sources) / 4) if sources else 0.3
            
#             return {
#                 "answer": result["result"],
#                 "sources": sources,
#                 "confidence": confidence,
#                 "question": question
#             }
#         except Exception as e:
#             print(f"Error answering question: {e}")
#             return {
#                 "answer": f"An error occurred: {str(e)}",
#                 "sources": [],
#                 "confidence": 0,
#                 "question": question
#             }
    
#     def get_summary(self, max_chunks: int = 5) -> str:
#         """
#         Get a quick summary of the report using top chunks
#         """
#         if not self.vectorstore:
#             return "No report loaded. Please initialize RAG first."
        
#         try:
#             # Retrieve most representative chunks
#             dummy_query = "summary overview introduction conclusion key findings"
#             results = self.vectorstore.similarity_search(dummy_query, k=max_chunks)
            
#             if not results:
#                 return "No summary available"
            
#             summary = "\n\n".join([doc.page_content for doc in results])
#             return summary[:1000] + "..." if len(summary) > 1000 else summary
#         except Exception as e:
#             return f"Error generating summary: {str(e)}"
    
#     def get_chunk_statistics(self) -> Dict[str, Any]:
#         """
#         Get statistics about the chunks
#         """
#         if not self.vectorstore:
#             return {"error": "No report loaded", "total_chunks": 0}
        
#         # Get collection info
#         try:
#             # Try to get count from vectorstore
#             if hasattr(self.vectorstore, '_collection'):
#                 count = self.vectorstore._collection.count()
#             else:
#                 count = len(self.vectorstore.get()['ids']) if hasattr(self.vectorstore, 'get') else 0
            
#             return {
#                 "total_chunks": count,
#                 "chunk_size": self.chunk_size,
#                 "chunk_overlap": self.chunk_overlap,
#                 "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
#                 "vector_dimension": 384,
#                 "status": "ready" if count > 0 else "empty"
#             }
#         except Exception as e:
#             return {
#                 "total_chunks": 0,
#                 "error": str(e),
#                 "status": "error"
#             }

# class SimpleExplainer:
#     """Helper class for explaining complex concepts simply"""
    
#     @staticmethod
#     def explain_simply(text: str, concept: str) -> str:
#         """
#         Explain a concept from the report in simple terms
#         """
#         prompt = f"""
#         Explain this concept from the research report in simple terms (like explaining to a 12-year-old):
        
#         Concept: {concept}
        
#         Related text: {text[:500]}
        
#         Provide a simple explanation with:
#         1. What it means in everyday language
#         2. A real-world example
#         3. Why it's important (1 sentence)
#         """
        
#         return prompt


import hashlib
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import numpy as np
import os
import tempfile
from dotenv import load_dotenv

# RAG imports with fallbacks for different environments
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import PromptTemplate

# Conditional imports for embeddings
try:
    from langchain_community.embeddings import HuggingFaceEmbeddings
    HUGGINGFACE_AVAILABLE = True
except ImportError:
    HUGGINGFACE_AVAILABLE = False
    print("⚠️ HuggingFaceEmbeddings not available")

try:
    from langchain_community.vectorstores import Chroma
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False
    print("⚠️ Chroma not available")

# Try different RetrievalQA import paths
try:
    from langchain.chains import RetrievalQA
    RETRIEVAL_AVAILABLE = True
except ImportError:
    try:
        from langchain_classic.chains import RetrievalQA
        RETRIEVAL_AVAILABLE = True
    except ImportError:
        RETRIEVAL_AVAILABLE = False
        print("⚠️ RetrievalQA not available")

load_dotenv()

# Detect environment
IS_RENDER = os.environ.get('RENDER', False) or os.path.exists('/etc/render')

@dataclass
class ChunkInfo:
    """Information about a text chunk"""
    id: str
    text: str
    metadata: Dict[str, Any]
    start_idx: int
    end_idx: int

class ResearchRAGEngine:
    """RAG Engine for research report with chunking and Q&A"""
    
    def __init__(self, chunk_size: int = 300, chunk_overlap: int = 50):
        # Use smaller chunks for Render free tier
        self.chunk_size = chunk_size if not IS_RENDER else 300
        self.chunk_overlap = chunk_overlap if not IS_RENDER else 50
        self.vectorstore = None
        self.qa_chain = None
        self.use_fallback = False
        self.is_initialized = False  # Track initialization status
        self.text_chunks = []  # Initialize empty list
        self.chunk_metadatas = []  # Initialize empty list
        
        # Determine storage path
        if IS_RENDER:
            self.persist_dir = tempfile.mkdtemp()
            print(f"🔧 Running on Render - using temp storage: {self.persist_dir}")
        else:
            self.persist_dir = "./research_chroma_db"
        
        # Initialize embeddings
        if IS_RENDER or not HUGGINGFACE_AVAILABLE:
            print("🔧 Render mode: Using lightweight configuration")
            self.embeddings = None
            self.use_fallback = True
        else:
            try:
                self.embeddings = HuggingFaceEmbeddings(
                    model_name="sentence-transformers/all-MiniLM-L6-v2",
                    model_kwargs={'device': 'cpu'},
                    encode_kwargs={'normalize_embeddings': True}
                )
                print("✅ Loaded local HuggingFace embeddings")
            except Exception as e:
                print(f"⚠️ Could not load embeddings: {e}")
                self.embeddings = None
                self.use_fallback = True
        
        # Initialize LLM
        api_key = os.getenv("MISTRAL_API_KEY")
        if not api_key:
            print("⚠️ MISTRAL_API_KEY not found")
        
        try:
            self.llm = ChatMistralAI(
                model="mistral-large-latest",
                temperature=0.3,
                api_key=api_key,
                timeout=60,
                max_retries=2
            )
            print("✅ LLM initialized")
        except Exception as e:
            print(f"⚠️ Could not initialize LLM: {e}")
            self.llm = None
        
    def chunk_report(self, report: str, metadata: Optional[Dict] = None) -> List[ChunkInfo]:
        """Split the research report into semantic chunks"""
        if not report:
            return []
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ".", " ", ""],
            add_start_index=True
        )
        
        chunks = text_splitter.create_documents(
            [report],
            metadatas=[metadata or {}]
        )
        
        chunk_infos = []
        for i, chunk in enumerate(chunks):
            chunk_info = ChunkInfo(
                id=hashlib.md5(chunk.page_content.encode()).hexdigest(),
                text=chunk.page_content,
                metadata={
                    "chunk_id": i,
                    "total_chunks": len(chunks),
                    "chunk_size": len(chunk.page_content),
                    **chunk.metadata
                },
                start_idx=chunk.metadata.get("start_index", 0),
                end_idx=chunk.metadata.get("end_index", len(chunk.page_content))
            )
            chunk_infos.append(chunk_info)
        
        return chunk_infos
    
    def create_vectorstore(self, report: str, metadata: Optional[Dict] = None) -> None:
        """Create a vector store from the chunked report"""
        if not report:
            raise ValueError("Report content is empty")
        
        print(f"📚 Creating vector store...")
        
        # Chunk the report
        chunks = self.chunk_report(report, metadata)
        print(f"✅ Created {len(chunks)} chunks (size: {self.chunk_size}, overlap: {self.chunk_overlap})")
        
        if len(chunks) == 0:
            raise ValueError("No chunks created from report")
        
        # ALWAYS store text_chunks regardless of mode
        self.text_chunks = [chunk.text for chunk in chunks]
        self.chunk_metadatas = [chunk.metadata for chunk in chunks]
        
        if self.use_fallback or not CHROMA_AVAILABLE:
            # Fallback mode: use in-memory storage
            print("🔧 Using in-memory storage (fallback mode)")
            self.vectorstore = None
        else:
            # Try to create vector store
            try:
                texts = [chunk.text for chunk in chunks]
                metadatas = [chunk.metadata for chunk in chunks]
                
                self.vectorstore = Chroma.from_texts(
                    texts=texts,
                    embedding=self.embeddings,
                    metadatas=metadatas,
                    persist_directory=self.persist_dir
                )
                print("✅ Chroma vector store created")
            except Exception as e:
                print(f"⚠️ Chroma failed: {e}, using fallback")
                self.vectorstore = None
        
        # Create QA function
        def simple_qa(question):
            # Simple keyword matching to find relevant chunks
            relevant_chunks = []
            question_words = set(question.lower().split())
            
            for chunk in self.text_chunks[:10]:  # Limit for performance
                chunk_words = set(chunk.lower().split())
                if len(question_words.intersection(chunk_words)) > 0:
                    relevant_chunks.append(chunk)
            
            context = "\n\n".join(relevant_chunks[:3]) if relevant_chunks else (self.text_chunks[0] if self.text_chunks else "")
            
            if not context:
                return {"result": "No relevant information found in the report.", "source_documents": []}
            
            prompt_template = """
            You are an AI assistant specialized in explaining research reports in easy-to-understand language.
            
            Context from the research report:
            {context}
            
            Question: {question}
            
            Instructions:
            1. Answer based ONLY on the provided context
            2. If the answer is not in the context, say "The research report doesn't contain information about this"
            3. Explain in simple, easy-to-understand language
            4. Keep answers concise but comprehensive
            
            Answer:
            """
            
            PROMPT = PromptTemplate(
                template=prompt_template,
                input_variables=["context", "question"]
            )
            
            try:
                response = self.llm.invoke(PROMPT.format(context=context[:3000], question=question))
                return {"result": response.content, "source_documents": relevant_chunks}
            except Exception as e:
                return {"result": f"Error generating answer: {str(e)}", "source_documents": []}
        
        self.qa_function = simple_qa
        self.is_initialized = True  # Mark as initialized
        print(f"✅ RAG system ready (mode: {'fallback' if self.use_fallback else 'full'})")
        
    def ask_question(self, question: str) -> Dict[str, Any]:
        """Ask a question about the research report with proper error handling"""
        # Check if RAG is initialized
        if not self.is_initialized:
            return {
                "answer": "⚠️ RAG system not initialized. Please click 'Initialize RAG' button first.",
                "sources": [],
                "confidence": 0,
                "question": question,
                "error": "not_initialized"
            }
        
        # Check if text_chunks exist
        if not hasattr(self, 'text_chunks') or not self.text_chunks:
            return {
                "answer": "⚠️ No report loaded. Please initialize RAG again.",
                "sources": [],
                "confidence": 0,
                "question": question,
                "error": "no_content"
            }
        
        if not question or not question.strip():
            return {
                "answer": "Please enter a valid question.",
                "sources": [],
                "confidence": 0,
                "question": question,
                "error": "empty_question"
            }
        
        print(f"❓ Answering: {question}")
        
        try:
            if hasattr(self, 'qa_function'):
                result = self.qa_function(question)
                sources = []
                for doc in result.get("source_documents", [])[:3]:
                    sources.append({
                        "text": doc[:300] + "..." if len(doc) > 300 else doc,
                        "metadata": {}
                    })
                confidence = 0.7 if sources else 0.3
                return {
                    "answer": result["result"],
                    "sources": sources,
                    "confidence": confidence,
                    "question": question
                }
            else:
                return {
                    "answer": "⚠️ RAG not properly initialized. Please re-initialize by clicking the button again.",
                    "sources": [],
                    "confidence": 0,
                    "question": question,
                    "error": "no_qa_function"
                }
        except Exception as e:
            print(f"Error answering question: {e}")
            return {
                "answer": f"Error: {str(e)}. Please try re-initializing RAG.",
                "sources": [],
                "confidence": 0,
                "question": question,
                "error": str(e)
            }
    
    def get_summary(self, max_chunks: int = 3) -> str:
        """Get a quick summary of the report using top chunks"""
        if hasattr(self, 'text_chunks') and self.text_chunks:
            summary = "\n\n".join(self.text_chunks[:max_chunks])
            return summary[:1000] + "..." if len(summary) > 1000 else summary
        
        return ""
        
    
    def get_chunk_statistics(self) -> Dict[str, Any]:
        """Get statistics about the chunks"""
        if not self.is_initialized:
            return {
                "error": "RAG not initialized. Please initialize RAG first.",
                "total_chunks": 0,
                "status": "not_initialized"
            }
        
        if not hasattr(self, 'text_chunks') or not self.text_chunks:
            return {
                "error": "No report loaded",
                "total_chunks": 0,
                "status": "empty"
            }
        
        return {
            "total_chunks": len(self.text_chunks),
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap,
            "embedding_model": "Fallback (keyword matching)" if self.use_fallback else "all-MiniLM-L6-v2",
            "mode": "Render optimized" if IS_RENDER else "Local",
            "status": "ready",
            "is_initialized": self.is_initialized
        }
    
    def reset(self):
        """Reset the RAG engine"""
        self.vectorstore = None
        self.qa_chain = None
        self.qa_function = None
        self.text_chunks = []
        self.chunk_metadatas = []
        self.is_initialized = False
        print("🔄 RAG engine reset")

class SimpleExplainer:
    """Helper class for explaining complex concepts simply"""
    
    @staticmethod
    def explain_simply(text: str, concept: str) -> str:
        """Explain a concept from the report in simple terms"""
        prompt = f"""
        Explain this concept from the research report in simple terms (like explaining to a 12-year-old):
        
        Concept: {concept}
        
        Related text: {text[:500]}
        
        Provide a simple explanation with:
        1. What it means in everyday language
        2. A real-world example
        3. Why it's important (1 sentence)
        """
        
        return prompt