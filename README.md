# 📊 Student AI Assistant Usage Analytics Dashboard

A professional Streamlit dashboard for analyzing student interactions with AI assistance tools.

## Features

- 📈 **Real-time Analytics** - Live data visualization and metrics
- 🎯 **Advanced Filtering** - Filter by student level, discipline, task type, satisfaction, and more
- 📊 **Rich Visualizations** - Interactive charts, graphs, and time-series analysis
- ⭐ **Performance Metrics** - Satisfaction ratings, completion rates, and session analytics
- 🔍 **Data Exploration** - Detailed data tables and statistical summaries

## Installation

### Local Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd "Streamlit 0.1"
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the app:
```bash
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`

## Streamlit Cloud Deployment

1. Push this repository to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Click "New app"
4. Connect your GitHub repository
5. Select this repository and `app.py` as the main file
6. Click "Deploy"

## Requirements

- Python 3.10+
- See `requirements.txt` for full dependencies

## Key Libraries

- **streamlit** - Web dashboard framework
- **pandas** - Data manipulation
- **plotly** - Interactive visualizations
- **numpy** - Numerical computing

## Data Format

The app expects a CSV file with the following columns:
- SessionID
- StudentLevel
- Discipline
- SessionDate
- SessionLengthMin
- TotalPrompts
- TaskType
- AI_AssistanceLevel
- FinalOutcome
- UsedAgain
- SatisfactionRating

## Author

Created with ❤️ for Student AI Analytics

## License

MIT License
