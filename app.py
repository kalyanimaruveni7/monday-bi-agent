import streamlit as st
import pandas as pd
from monday_api import get_boards, get_board_items
from gemini_agent import ask_gemini

st.set_page_config(page_title="Monday BI Agent", layout="wide")

st.title("📊 Monday.com Business Intelligence Agent")
st.write("Ask founder-level business questions about your Monday.com boards.")

try:
    boards_data = get_boards()

    if "data" not in boards_data:
        st.error("Unable to connect to Monday API")
        st.write(boards_data)
        st.stop()

    boards = boards_data["data"]["boards"]

    board_dict = {}

    for board in boards:
        if board["name"] in ["Work Orders", "Deals"]:
            board_dict[board["name"]] = board["id"]

    st.sidebar.header("Connected Boards")
    st.sidebar.write(board_dict)

    question = st.text_input(
        "Ask a business question",
        placeholder="Example: Give me a summary of work orders and deals."
    )

    if st.button("Analyze"):

        result = []
        board_data = ""

        for board_name, board_id in board_dict.items():

            data = get_board_items(board_id)

            try:
                items = data["data"]["boards"][0]["items_page"]["items"]

                result.append({
                    "Board": board_name,
                    "Items": len(items)
                })

                board_data += f"\n===== {board_name} =====\n"

                for item in items:

                    board_data += f"Item: {item['name']}\n"

                    for col in item["column_values"]:
                        title = col["column"]["title"]
                        value = col["text"]

                        if value is None or value == "":
                            value = "Not Available"

                        board_data += f"{title}: {value}\n"

                    board_data += "\n"

            except Exception as e:
                st.warning(f"Unable to read {board_name}: {e}")

        df = pd.DataFrame(result)

        st.subheader("Board Summary")
        st.dataframe(df)

        st.subheader("🤖 AI Business Intelligence")

        with st.spinner("Analyzing your Monday.com data..."):

            try:

                prompt = f"""
You are an expert Business Intelligence Analyst.

Below is data exported from Monday.com.

{board_data}

User Question:
{question}

Instructions:
- Answer only from the provided data.
- If information is missing, clearly say so.
- Provide business insights.
- Mention trends if visible.
- Give a concise founder-level summary.
"""

                answer = ask_gemini(prompt, board_data)

                st.success(answer)

            except Exception as e:
                st.error(f"Gemini Error: {e}")

except Exception as e:
    st.error(e)