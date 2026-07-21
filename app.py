import streamlit as st
import pandas as pd
from monday_api import get_boards, get_board_items
from gemini_agent import ask_gemini

st.set_page_config(
    page_title="Executive Insights AI",
    page_icon="📊",
    layout="wide",
)

# ---------- Custom CSS ----------
st.markdown("""
<style>

.main{
    background:#f4f7fb;
}

.big-title{
    font-size:42px;
    font-weight:700;
    color:white;
}

.subtitle{
    font-size:18px;
    color:#dbeafe;
}

.header-box{
    background:linear-gradient(90deg,#0f172a,#1e3a8a);
    padding:30px;
    border-radius:18px;
    margin-bottom:25px;
}

.metric-card{
    background:white;
    padding:20px;
    border-radius:15px;
    text-align:center;
    box-shadow:0px 3px 12px rgba(0,0,0,0.15);
}

.metric-title{
    font-size:18px;
    color:#555;
}

.metric-value{
    font-size:34px;
    color:#1e40af;
    font-weight:bold;
}

.ai-box{
    background:white;
    padding:25px;
    border-radius:15px;
    box-shadow:0px 3px 12px rgba(0,0,0,0.15);
}

.sidebar-title{
    font-size:20px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown("""
<div class="header-box">

<div class="big-title">
📊 Executive Insights AI
</div>

<div class="subtitle">
AI Powered Business Intelligence Agent for Monday.com
</div>

</div>
""", unsafe_allow_html=True)

# ---------- Sidebar ----------
st.sidebar.markdown("## 📊 Executive Insights")

st.sidebar.markdown("---")

st.sidebar.markdown("### 💡 Suggested Questions")

st.sidebar.info("How is our pipeline this quarter?")
st.sidebar.info("Which customers have active deals?")
st.sidebar.info("Show delayed work orders.")
st.sidebar.info("Give leadership summary.")
st.sidebar.info("Revenue insights.")

st.sidebar.markdown("---")

try:

    boards_data = get_boards()

    if "data" not in boards_data:
        st.error("Unable to connect to Monday.com")
        st.stop()

    boards = boards_data["data"]["boards"]

    board_dict = {}

    for board in boards:
        if board["name"] in ["Work Orders", "Deals"]:
            board_dict[board["name"]] = board["id"]

    result=[]
    board_data=""

    for board_name,board_id in board_dict.items():

        data=get_board_items(board_id)

        try:

            items=data["data"]["boards"][0]["items_page"]["items"]

            result.append({
                "Board":board_name,
                "Items":len(items)
            })

            board_data+=f"\n===== {board_name} =====\n"

            for item in items:

                board_data+=f"Item: {item['name']}\n"

                for col in item["column_values"]:

                    title=col["column"]["title"]
                    value=col["text"]

                    if value is None or value=="":
                        value="Not Available"

                    board_data+=f"{title}: {value}\n"

                board_data+="\n"

        except:
            pass

    df=pd.DataFrame(result)

    total_items=df["Items"].sum()

    col1,col2,col3,col4=st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
        <div class="metric-title">📋 Boards</div>
        <div class="metric-value">{len(board_dict)}</div>
        </div>
        """,unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
        <div class="metric-title">📦 Total Items</div>
        <div class="metric-value">{total_items}</div>
        </div>
        """,unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
        <div class="metric-title">💼 Work Orders</div>
        <div class="metric-value">{df.loc[df.Board=='Work Orders','Items'].sum()}</div>
        </div>
        """,unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
        <div class="metric-title">💰 Deals</div>
        <div class="metric-value">{df.loc[df.Board=='Deals','Items'].sum()}</div>
        </div>
        """,unsafe_allow_html=True)

    st.write("")
    st.write("")

    st.subheader("💬 Ask Executive Business Question")

    question=st.text_area(
        "",
        placeholder="Example: Give me a founder-level summary of work orders and deals.",
        height=120
    )
    if st.button("🚀 Analyze Business Data", use_container_width=True):

        st.markdown("---")

        col1, col2 = st.columns([2,1])

        with col1:

            st.subheader("📋 Board Summary")
            st.dataframe(df, use_container_width=True)

        with col2:

            st.subheader("📊 Items Distribution")

            if not df.empty:

                chart = df.set_index("Board")

                st.bar_chart(chart)

                st.line_chart(chart)

        st.markdown("---")

        st.subheader("🤖 AI Executive Insights")

        with st.spinner("Generating executive insights..."):

            try:

                prompt = f"""
You are an expert Business Intelligence Analyst.

Below is data exported from Monday.com.

{board_data}

User Question:
{question}

Instructions:

- Answer ONLY from the provided data.
- If information is unavailable, clearly mention it.
- Give founder-level business insights.
- Mention trends if visible.
- Mention risks if visible.
- Keep the answer concise and professional.
"""

                answer = ask_gemini(prompt, board_data)

                st.markdown(f"""
                <div class="ai-box">

                <h3>🤖 Executive Summary</h3>

                <hr>

                <p style="font-size:17px;line-height:1.8;">
                {answer}
                </p>

                </div>
                """, unsafe_allow_html=True)

            except Exception as e:

                st.error(f"Gemini Error : {e}")

    st.markdown("---")

    with st.expander("📄 View Raw Board Data"):

        st.text(board_data)

except Exception as e:

    st.error(e)
