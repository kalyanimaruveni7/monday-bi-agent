import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("MONDAY_API_TOKEN")
API_URL = "https://api.monday.com/v2"

headers = {
    "Authorization": API_TOKEN,
    "Content-Type": "application/json"
}


def get_boards():
    query = """
    {
      boards {
        id
        name
      }
    }
    """

    response = requests.post(
        API_URL,
        json={"query": query},
        headers=headers
    )

    return response.json()


def get_board_items(board_id):
    query = f"""
    {{
      boards(ids:{board_id}) {{
        id
        name
        items_page {{
          items {{
            id
            name
            column_values {{
              column {{
                title
              }}
              text
            }}
          }}
        }}
      }}
    }}
    """

    response = requests.post(
        API_URL,
        json={"query": query},
        headers=headers
    )

    return response.json()