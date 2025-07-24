import streamlit as st
from qa_system import VoiceQASystem
from evaluation.evaluator import QAEvaluator
import pandas as pd

def main():
    st.title("Comparative Study: Voice-Based Document QA Systems")
    st.markdown("### Foundation vs Indic vs International Language Models")
    
    # Initialize system
    if 'qa_system' not in st.session_state:
        st.session_state.qa_system = VoiceQASystem()
        st.session_state.evaluator = QAEvaluator()
    
    # File upload section
    st.header("1. Upload Documents")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("English Document")
        english_pdf = st.file_uploader("Upload English PDF", type="pdf", key="en")
        
    with col2:
        st.subheader("Hindi Document")
        hindi_pdf = st.file_uploader("Upload Hindi PDF", type="pdf", key="hi")
        
    with col3:
        st.subheader("French Document")
        french_pdf = st.file_uploader("Upload French PDF", type="pdf", key="fr")
    
    # Questions section
    st.header("2. Sample Questions")
    
    sample_questions = {
        "foundation": [
            "What is the main topic of this document?",
            "Can you summarize the key findings?",
            "What are the conclusions mentioned?"
        ],
        "indic": [
            "इस दस्तावेज़ का मुख्य विषय क्या है?",
            "मुख्य निष्कर्ष क्या हैं?",
            "क्या सिफारिशें दी गई हैं?"
        ],
        "international": [
            "Quel est le sujet principal de ce document?",
            "Quelles sont les principales conclusions?",
            "Quelles recommandations sont faites?"
        ]
    }
    
    for model, questions in sample_questions.items():
        st.subheader(f"{model.title()} Model Questions")
        for i, q in enumerate(questions, 1):
            st.write(f"{i}. {q}")
    
    # Results section
    if st.button("Run Comparative Analysis"):
        if all([english_pdf, hindi_pdf, french_pdf]):
            # Save uploaded files temporarily
            pdf_paths = {
                "foundation": "temp_english.pdf",
                "indic": "temp_hindi.pdf", 
                "international": "temp_french.pdf"
            }
            
            # Process and display results
            st.header("3. Results")
            
            with st.spinner("Processing documents and generating answers..."):
                results = st.session_state.qa_system.run_qa_session(
                    pdf_paths, sample_questions
                )
                
            # Display results for each model
            for model_name, model_results in results.items():
                st.subheader(f"{model_name.title()} Model Results")
                
                for i, result in enumerate(model_results, 1):
                    with st.expander(f"Q{i}: {result['question'][:50]}..."):
                        st.write("**Answer:**", result['answer'])
                        st.write("**Context:**", result['context'])
                        
            # Comparison table
            st.header("4. Comparison Table")
            comparison_data = st.session_state.evaluator.generate_comparison_table(results)
            df = pd.DataFrame(comparison_data)
            st.dataframe(df)
            
        else:
            st.error("Please upload all three PDF documents")

if __name__ == "__main__":
    main()