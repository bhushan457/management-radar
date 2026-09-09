import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

from retrieve import retrieve_documents


load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:

    st.error(
        "GEMINI_API_KEY was not found. "
        "Please check your .env file."
    )

    st.stop()


client = genai.Client(
    api_key=API_KEY
)



st.set_page_config(
    page_title="HDFC AMC RAG Assistant",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)



st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 17px;
        color: #777777;
        margin-bottom: 25px;
    }

    .answer-box {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #dddddd;
        margin-top: 10px;
        margin-bottom: 20px;
    }

    .source-box {
        padding: 12px;
        border-radius: 10px;
        border: 1px solid #dddddd;
        margin-bottom: 8px;
    }

    .small-text {
        font-size: 13px;
        color: #777777;
    }

    </style>
    """,
    unsafe_allow_html=True
)




with st.sidebar:

    st.header(
        "📊 HDFC AMC RAG"
    )

    st.write(
        "Retrieval-Augmented Generation "
        "assistant for company research."
    )

    st.divider()

    st.subheader(
        "📚 Companies"
    )

    st.write(
        "🏢 Infosys"
    )

    st.write(
        "🚗 Maruti Suzuki"
    )

    st.divider()

    st.subheader(
        "📄 Data Sources"
    )

    st.write(
        "• Financial results"
    )

    st.write(
        "• Company announcements"
    )

    st.write(
        "• Earnings call transcripts"
    )

    st.write(
        "• Management interviews"
    )

    st.divider()

    st.subheader(
        "⚙️ Technology"
    )

    st.write(
        "• Python"
    )

    st.write(
        "• Streamlit"
    )

    st.write(
        "• Gemini"
    )

    st.write(
        "• SQLite"
    )

    st.write(
        "• Vector embeddings"
    )

    st.divider()

    st.caption(
        "HDFC AMC Assessment"
    )


st.markdown(
    '<div class="main-title">'
    '📊 HDFC AMC RAG Assistant'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
    AI-powered research assistant for Infosys and
    Maruti Suzuki company documents.
    </div>
    """,
    unsafe_allow_html=True
)



# 7. Dashboard metrics


# col1, col2, col3, col4 = st.columns(4)

# with col1:

#     st.metric(
#         "Companies",
#         "2"
#     )

# with col2:

#     st.metric(
#         "Sources",
#         "9"
#     )

# with col3:

#     st.metric(
#         "Indexed Chunks",
#         "231"
#     )

# with col4:

#     st.metric(
#         "Vector Database",
#         "SQLite"
#     )


# st.divider()



# 8. Suggested questions


st.subheader(
    "💡 Suggested Questions"
)

suggested_questions = [

    "What was Infosys revenue growth in Q1 FY27?",

    "What was Infosys operating margin in Q1 FY27?",

    "What percentage of Infosys revenue came from AI services?",

    "Who is the successor to Salil Parekh as Infosys CEO?",

    "What was Maruti Suzuki's total production in August 2026?",

    "What was the introductory price of the e VITARA under BaaS?",

    "Compare Infosys Q1 FY27 performance with Maruti Suzuki August 2026 production."

]


question_option = st.selectbox(

    "Select a question or enter your own below:",

    [
        "Select a suggested question"
    ] + suggested_questions

)



# 9. User question


question = st.text_input(

    "🔎 Ask your question",

    value=(
        ""
        if question_option
        == "Select a suggested question"
        else question_option
    ),

    placeholder=(
        "Example: What was Infosys revenue growth in Q1 FY27?"
    )

)



# 10. Company-aware retrieval


def get_relevant_documents(question):

    """
    Retrieve relevant documents.

    Normal question:
        Search the complete database.

    Infosys + Maruti comparison:
        Search Infosys documents separately.
        Search Maruti documents separately.
    """

    question_lower = question.lower()


    mentions_infosys = (
        "infosys" in question_lower
    )


    mentions_maruti = (

        "maruti" in question_lower

        or "e-vitara" in question_lower

        or "vitara" in question_lower

    )


    
    # Comparison question
    

    if (
        mentions_infosys
        and mentions_maruti
    ):

       
        # Retrieve Infosys-only evidence
       

        infosys_results = retrieve_documents(

            question,

            top_k=3,

            source_keyword="Infosys"

        )


       
        # Retrieve Maruti-only evidence
       

        maruti_results = retrieve_documents(

            question,

            top_k=3,

            source_keyword="Maruti"

        )


       
        # Combine results
       

        combined_results = (

            infosys_results
            +
            maruti_results

        )


       
        # Remove duplicate chunks
       

        unique_results = {}


        for result in combined_results:

            key = (

                result["source"],

                result["chunk_text"]

            )


            if key not in unique_results:

                unique_results[key] = result


            else:

                if (
                    result["score"]
                    >
                    unique_results[key]["score"]
                ):

                    unique_results[key] = result


        results = list(
            unique_results.values()
        )


       
        # Sort by relevance
       

        results.sort(

            key=lambda x: x["score"],

            reverse=True

        )


        return results


    
    # Normal question
    

    return retrieve_documents(

        question,

        top_k=5

    )



# 11. Ask button


ask_button = st.button(

    "🔍 Ask HDFC AMC Assistant",

    type="primary",

    use_container_width=True

)



# 12. Process question


if ask_button:

    if not question.strip():

        st.warning(
            "Please enter a question first."
        )

    else:

        try:

           
            # Retrieve evidence
           

            with st.spinner(
                "🔎 Searching company documents..."
            ):

                results = get_relevant_documents(
                    question
                )


            if not results:

                st.warning(
                    "No relevant information was found "
                    "in the provided documents."
                )

                st.stop()


           
            # Build context
           

            context_parts = []


            for result in results:

                context_parts.append(

                    f"""
SOURCE: {result['source']}

DOCUMENT CONTENT:
{result['chunk_text']}
"""

                )


            context = "\n\n".join(
                context_parts
            )


           
            # RAG prompt
           

            prompt = f"""
You are an AI financial research assistant
for HDFC Asset Management Company (HDFC AMC).

Answer the user's question using ONLY the
retrieved company documents.

IMPORTANT RULES:

1. Do not use outside knowledge.

2. Do not invent facts, numbers, dates,
   names, or explanations.

3. If information is unavailable, say:
   "I could not find this information in
   the provided documents."

4. For numerical questions, provide exact
   numbers from the documents.

5. For comparison questions involving
   Infosys and Maruti Suzuki, ALWAYS provide
   separate sections for BOTH companies.

6. For comparison questions, use all relevant
   evidence available for each company.

7. Do not compare unrelated units directly.
   For example, do not say that revenue growth
   is greater or smaller than production units.

8. Instead, explain the performance metrics
   separately and provide a useful qualitative
   comparison.

9. Clearly mention the relevant period.

10. Keep the answer concise, factual,
    and professional for an investment
    research audience.

USER QUESTION:
{question}

RETRIEVED DOCUMENTS:
{context}

FINAL ANSWER:
"""


           
            # Generate answer
           

            with st.spinner(
                "🤖 Generating grounded answer..."
            ):

                response = client.models.generate_content(

                    model="gemini-3.5-flash-lite",

                    contents=prompt

                )


                answer = response.text


           
            # Display answer
           

            st.divider()

            st.subheader(
                "💡 Answer"
            )

            st.markdown(

                f"""
                <div class="answer-box">
                {answer}
                </div>
                """,

                unsafe_allow_html=True

            )


           
            # Display sources
           

            st.subheader(
                "📚 Sources"
            )


            displayed_sources = set()


            for result in results:

                source = result["source"]


                if source not in displayed_sources:

                    st.markdown(

                        f"""
                        <div class="source-box">

                        📄 <b>{source}</b>

                        <br>

                        <span class="small-text">

                        Relevance score:
                        {result['score']:.4f}

                        </span>

                        </div>
                        """,

                        unsafe_allow_html=True

                    )


                    displayed_sources.add(
                        source
                    )


           
            # Retrieved evidence
           

            with st.expander(
                "🔎 View Retrieved Evidence"
            ):

                st.write(
                    "These document chunks were retrieved "
                    "before generating the answer."
                )


                for index, result in enumerate(

                    results,

                    start=1

                ):

                    st.markdown(

                        f"### Result {index}"

                    )


                    st.write(

                        f"**Source:** "
                        f"{result['source']}"

                    )


                    st.write(

                        f"**File Type:** "
                        f"{result['file_type']}"

                    )


                    st.write(

                        f"**Relevance Score:** "
                        f"{result['score']:.4f}"

                    )


                    st.write(
                        result["chunk_text"]
                    )


                    st.divider()


        except Exception as error:

            st.error(

                "An error occurred while "
                "processing your question."

            )

            st.code(
                str(error)
            )



# 13. About section


st.divider()


with st.expander(
    "ℹ️ About this RAG Application"
):

    st.write(

        """
        This application implements a
        Retrieval-Augmented Generation (RAG)
        pipeline.

        Workflow:

        Documents
        →
        Text Extraction
        →
        Chunking
        →
        Gemini Embeddings
        →
        SQLite Vector Database
        →
        Company-Aware Similarity Retrieval
        →
        Gemini LLM
        →
        Grounded Answer

        For comparison questions involving
        Infosys and Maruti Suzuki, evidence is
        retrieved separately for each company
        before generating the final answer.
        """

    )



# 14. Footer


st.divider()


st.caption(

    "HDFC AMC RAG Assessment | "
    "Python • Streamlit • Gemini • SQLite"

)