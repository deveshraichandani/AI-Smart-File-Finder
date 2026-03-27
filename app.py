#to activate venv this command after cd : venv\Scripts\Activate

import streamlit as st
import os
import subprocess

from scanner import scan_folder
from extractor import extract_text
from utils import clean_text
from embeddings import create_embedding
from search import search
from indexer import save_index, load_index


st.set_page_config(page_title="Smart File Finder", page_icon="🔎", layout="wide")


st.markdown("""
<style>

.block-container{
padding-top:30px;
}

.main-title{
font-size:44px;
font-weight:700;
margin-bottom:4px;
}

.subtitle{
font-size:18px;
color:#6b7280;
margin-bottom:25px;
}

.stTextInput > div > div > input{
font-size:17px;
padding:12px;
}

.stButton > button{
font-size:15px;
padding:8px 16px;
border-radius:8px;
}

.result-card{
padding:18px;
border-radius:12px;
background:#f8fafc;
margin-top:14px;
border:1px solid #e5e7eb;
}

.result-title{
font-size:22px;
font-weight:600;
margin-bottom:6px;
}

.result-label{
font-size:14px;
margin-top:2px;
}

.file-path{
font-size:14px;
color:#4b5563;
}

.match-score{
font-size:15px;
margin-top:6px;
}

</style>
""", unsafe_allow_html=True)


st.markdown('<div class="main-title">🔎 Smart File Finder</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Search files on your computer using AI semantic understanding</div>', unsafe_allow_html=True)


index_file = "file_index.pkl"


col1, col2 = st.columns([5,1])

with col1:
    folder = st.text_input("📁 Enter folder path")

with col2:
    top_k = st.number_input("Results",1,20,5)


st.caption("Tip: Drag a folder from Windows Explorer into the input box above.")


if st.button("Prepare Files for Search"):

    if not folder:
        st.warning("Please enter a folder path")

    else:

        files = scan_folder(folder)

        index = []

        progress = st.progress(0)

        for i,f in enumerate(files):

            text = extract_text(f)
            text = clean_text(text)

            filename = os.path.basename(f)
            filename = filename.replace("_"," ").replace("-"," ")
            filename = filename.replace("."," ")
            filename = filename.lower()

            if len(text) > 20:
                content = filename + " " + text
            else:
                content = filename

            emb = create_embedding(content)

            index.append({
                "path":f,
                "embedding":emb
            })

            progress.progress((i+1)/len(files))


        save_index(index,index_file)

        st.session_state.index = index

        st.success(f"{len(index)} files analyzed and ready for search")


if os.path.exists(index_file) and "index" not in st.session_state:
    st.session_state.index = load_index(index_file)


query = st.text_input("🔍 Search your files")


if query and "index" in st.session_state:

    query_text = query + " file document role description job report notes assignment"

    q_emb = create_embedding(query_text)

    results = search(q_emb, st.session_state.index, top_k)

    if len(results)==0:
        st.info("No relevant files found")

    for path,score in results:

        percent = int(score*100)

        ext = os.path.splitext(path)[1].replace(".","").upper()

        icon="📄"
        if ext=="PDF":
            icon="📕"
        if ext=="DOCX":
            icon="📝"
        if ext=="TXT":
            icon="📃"


        st.markdown('<div class="result-card">', unsafe_allow_html=True)

        st.markdown(
            f'<div class="result-title">{icon} {os.path.basename(path)}</div>',
            unsafe_allow_html=True
        )


        st.markdown('<div class="result-label">📂 File Location:</div>', unsafe_allow_html=True)

        st.markdown(f'<div class="file-path">{path}</div>', unsafe_allow_html=True)


        st.markdown(
            f'<div class="match-score">Relevance: {percent}%</div>',
            unsafe_allow_html=True
        )


        col1,col2,col3 = st.columns([1,1,6])

        with col1:
            if st.button("Open File", key=path):
                subprocess.Popen(f'explorer "{path}"')

        with col2:
            if st.button("Open Folder", key=path+"folder"):
                subprocess.Popen(f'explorer /select,"{path}"')

        st.markdown('</div>', unsafe_allow_html=True)