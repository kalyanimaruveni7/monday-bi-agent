# Decision Log

## Project Overview
Built a Business Intelligence Agent using Python and Streamlit that connects to Monday.com and answers business questions using Google Gemini.

## Design Decisions

### Python
Chosen for rapid development and API integration.

### Streamlit
Used to quickly build an interactive web application.

### Monday.com GraphQL API
Selected as the primary data source for retrieving Work Orders and Deals.

### Google Gemini
Used to generate AI-powered business insights from Monday.com data.

### Pandas
Used for processing and summarizing board data.

## Assumptions

- The application works with Work Orders and Deals boards.
- Missing values are handled gracefully.
- The system provides read-only access to Monday.com.

## Future Improvements

- Interactive charts and dashboards
- Export reports to Excel/PDF
- Authentication and user roles
- Advanced analytics and KPIs
