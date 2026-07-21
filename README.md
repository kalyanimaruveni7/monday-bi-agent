# Monday.com Business Intelligence Agent

## Overview
This project is a Business Intelligence Agent built using Python and Streamlit. It connects to Monday.com using the Monday GraphQL API, retrieves data from Work Orders and Deals boards, and provides business insights using Google Gemini.

## Features
- Connects to Monday.com API
- Reads Work Orders and Deals boards
- Displays board summaries
- AI-powered business insights using Google Gemini
- Streamlit web interface
- Handles missing values gracefully

## Tech Stack
- Python
- Streamlit
- Monday.com GraphQL API
- Google Gemini API
- Pandas

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python -m streamlit run app.py
```

## Project Structure

- app.py
- monday_api.py
- gemini_agent.py
- analytics.py
- utils.py
- requirements.txt
