import streamlit as st
from rag import process_urls,generate_answer


st.set_page_config(page_title="Real Estate Research Tool",
                   layout='wide')

st.title("Real Estate Research Tool")

st.sidebar.header("Data Sources")

url1 = st.sidebar.text_input("URL 1")
url2 = st.sidebar.text_input("URL 2")
url3 = st.sidebar.text_input("URL 3")

placeholder = st.empty()

process_url_button = st.sidebar.button("🚀 Process URLs", type="primary")

if process_url_button:
    urls = [url for url in (url1, url2, url3) if url != '']
    
    if len(urls) == 0:
        placeholder.error("⚠️ You must provide at least one valid URL")
    else:
        # Show processing status
        with placeholder.container():
            for status in process_urls(urls):
                st.info(status)

# Question input
query = st.text_input("💬 Ask a question about the content:", placeholder="e.g., What is the 30-year fixed mortgage rate?")

if query:
    try:
        with st.spinner("🤔 Generating answer..."):
            answer, sources = generate_answer(query)
        
        # Display answer
        st.markdown("### 📝 Answer:")
        st.write(answer)

        # Display sources
        if sources:
            st.markdown("### 🔗 Sources:")
            for source in sources.split("\n"):
                st.markdown(f"- [{source}]({source})")
                
    except RuntimeError as e:
        st.error("⚠️ You must process URLs first. Please add URLs in the sidebar and click 'Process URLs'.")

