import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Student AI Assistant Usage Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
        .metric-card {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        .main {
            padding: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# ==================== LOAD DATA ====================
try:
    df = pd.read_csv("ai_assistant_usage_student_life.csv")
    df['SessionDate'] = pd.to_datetime(df['SessionDate'])
except FileNotFoundError:
    st.error("❌ CSV file not found. Please check the file name.")
    st.stop()
except Exception as e:
    st.error(f"❌ Error loading data: {e}")
    st.stop()

# ==================== HEADER ====================
st.title("📊 Student AI Assistant Usage Analytics")
st.markdown("*Real-time insights into student interactions with AI assistance*")
st.divider()

# ==================== KEY METRICS ====================
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("📚 Total Sessions", f"{len(df):,}")
with col2:
    st.metric("👥 Student Levels", df['StudentLevel'].nunique())
with col3:
    st.metric("🎓 Disciplines", df['Discipline'].nunique())
with col4:
    avg_satisfaction = df['SatisfactionRating'].mean()
    st.metric("⭐ Avg Satisfaction", f"{avg_satisfaction:.2f}/5")
with col5:
    reuse_rate = (df['UsedAgain'].sum() / len(df) * 100)
    st.metric("🔄 Reuse Rate", f"{reuse_rate:.1f}%")

st.divider()

# ==================== INITIALIZE SESSION STATE ====================
if 'selected_level' not in st.session_state:
    st.session_state.selected_level = sorted(df['StudentLevel'].unique())
if 'selected_discipline' not in st.session_state:
    st.session_state.selected_discipline = sorted(df['Discipline'].unique())
if 'selected_task' not in st.session_state:
    st.session_state.selected_task = sorted(df['TaskType'].unique())
if 'selected_outcome' not in st.session_state:
    st.session_state.selected_outcome = sorted(df['FinalOutcome'].unique())
if 'selected_assistance' not in st.session_state:
    st.session_state.selected_assistance = sorted(df['AI_AssistanceLevel'].unique())
if 'session_length_range' not in st.session_state:
    st.session_state.session_length_range = (int(df['SessionLengthMin'].min()), int(df['SessionLengthMin'].max()))
if 'satisfaction_range' not in st.session_state:
    st.session_state.satisfaction_range = (0.0, 5.0)
if 'date_filter' not in st.session_state:
    st.session_state.date_filter = False
if 'date_range' not in st.session_state:
    st.session_state.date_range = (df['SessionDate'].min().date(), df['SessionDate'].max().date())

st.divider()

# ==================== ADVANCED SIDEBAR FILTERS ====================
with st.sidebar:
    st.markdown("### 🎛️ Advanced Filters")
    
    # Filter Tabs
    filter_tab1, filter_tab2 = st.tabs(["Quick Filters", "Advanced"])
    
    with filter_tab1:
        st.markdown("**Preset Filters**")
        col_preset1, col_preset2 = st.columns(2)
        
        with col_preset1:
            if st.button("🔄 Reset All", key="reset_all", use_container_width=True):
                st.session_state.selected_level = sorted(df['StudentLevel'].unique())
                st.session_state.selected_discipline = sorted(df['Discipline'].unique())
                st.session_state.selected_task = sorted(df['TaskType'].unique())
                st.session_state.selected_outcome = sorted(df['FinalOutcome'].unique())
                st.session_state.selected_assistance = sorted(df['AI_AssistanceLevel'].unique())
                st.session_state.session_length_range = (int(df['SessionLengthMin'].min()), int(df['SessionLengthMin'].max()))
                st.session_state.satisfaction_range = (0.0, 5.0)
                st.session_state.date_filter = False
                st.rerun()
        
        with col_preset2:
            if st.button("⭐ High Satisfaction", key="high_sat", use_container_width=True):
                st.session_state.selected_outcome = sorted(df['FinalOutcome'].unique())
                st.session_state.satisfaction_range = (4.0, 5.0)
                st.session_state.selected_level = sorted(df['StudentLevel'].unique())
                st.session_state.selected_discipline = sorted(df['Discipline'].unique())
                st.session_state.selected_task = sorted(df['TaskType'].unique())
                st.session_state.selected_assistance = sorted(df['AI_AssistanceLevel'].unique())
                st.session_state.session_length_range = (int(df['SessionLengthMin'].min()), int(df['SessionLengthMin'].max()))
                st.session_state.date_filter = False
                st.rerun()
        
        col_preset3, col_preset4 = st.columns(2)
        with col_preset3:
            if st.button("✅ Completed Tasks", key="completed", use_container_width=True):
                st.session_state.selected_outcome = ['Assignment Completed']
                st.session_state.satisfaction_range = (0.0, 5.0)
                st.session_state.selected_level = sorted(df['StudentLevel'].unique())
                st.session_state.selected_discipline = sorted(df['Discipline'].unique())
                st.session_state.selected_task = sorted(df['TaskType'].unique())
                st.session_state.selected_assistance = sorted(df['AI_AssistanceLevel'].unique())
                st.session_state.session_length_range = (int(df['SessionLengthMin'].min()), int(df['SessionLengthMin'].max()))
                st.session_state.date_filter = False
                st.rerun()
        
        with col_preset4:
            if st.button("🔄 Used Again", key="reused", use_container_width=True):
                st.session_state.selected_outcome = sorted(df['FinalOutcome'].unique())
                st.session_state.satisfaction_range = (0.0, 5.0)
                st.session_state.selected_level = sorted(df['StudentLevel'].unique())
                st.session_state.selected_discipline = sorted(df['Discipline'].unique())
                st.session_state.selected_task = sorted(df['TaskType'].unique())
                st.session_state.selected_assistance = sorted(df['AI_AssistanceLevel'].unique())
                st.session_state.session_length_range = (int(df['SessionLengthMin'].min()), int(df['SessionLengthMin'].max()))
                st.session_state.date_filter = False
                st.rerun()
        
        st.divider()
    
    with filter_tab2:
        st.markdown("**Custom Filters**")
        
        # Date Range Filter
        st.session_state.date_filter = st.checkbox("📅 Filter by Date Range", value=st.session_state.date_filter)
        if st.session_state.date_filter:
            st.session_state.date_range = st.date_input(
                "Select date range",
                value=st.session_state.date_range,
                min_value=df['SessionDate'].min().date(),
                max_value=df['SessionDate'].max().date()
            )
        
        st.markdown("**Demographic Filters**")
        
        # Student Level Filter
        st.session_state.selected_level = st.multiselect(
            "Student Level",
            sorted(df['StudentLevel'].unique()),
            default=st.session_state.selected_level,
            help="Select one or multiple student levels"
        )
        
        # Discipline Filter
        st.session_state.selected_discipline = st.multiselect(
            "Discipline",
            sorted(df['Discipline'].unique()),
            default=st.session_state.selected_discipline,
            help="Select one or multiple disciplines"
        )
        
        st.markdown("**Activity Filters**")
        
        # Task Type Filter
        st.session_state.selected_task = st.multiselect(
            "Task Type",
            sorted(df['TaskType'].unique()),
            default=st.session_state.selected_task,
            help="Select one or multiple task types"
        )
        
        # Final Outcome Filter
        st.session_state.selected_outcome = st.multiselect(
            "Final Outcome",
            sorted(df['FinalOutcome'].unique()),
            default=st.session_state.selected_outcome,
            help="Select one or multiple outcomes"
        )
        
        st.markdown("**Performance Filters**")
        
        # Session Length Filter
        st.session_state.session_length_range = st.slider(
            "Session Length (minutes)",
            min_value=int(df['SessionLengthMin'].min()),
            max_value=int(df['SessionLengthMin'].max()),
            value=st.session_state.session_length_range,
            help="Filter sessions by duration"
        )
        
        # Satisfaction Rating Filter
        st.session_state.satisfaction_range = st.slider(
            "Satisfaction Rating",
            min_value=0.0,
            max_value=5.0,
            value=st.session_state.satisfaction_range,
            step=0.1,
            help="Filter by satisfaction score"
        )
        
        # AI Assistance Level Filter
        st.session_state.selected_assistance = st.multiselect(
            "AI Assistance Level",
            sorted(df['AI_AssistanceLevel'].unique()),
            default=st.session_state.selected_assistance,
            help="Select one or multiple assistance levels"
        )

# Apply Custom Filters
filtered_df = df[
    (df['StudentLevel'].isin(st.session_state.selected_level)) &
    (df['Discipline'].isin(st.session_state.selected_discipline)) &
    (df['TaskType'].isin(st.session_state.selected_task)) &
    (df['FinalOutcome'].isin(st.session_state.selected_outcome)) &
    (df['SessionLengthMin'].between(st.session_state.session_length_range[0], st.session_state.session_length_range[1])) &
    (df['SatisfactionRating'].between(st.session_state.satisfaction_range[0], st.session_state.satisfaction_range[1])) &
    (df['AI_AssistanceLevel'].isin(st.session_state.selected_assistance))
].copy()

if st.session_state.date_filter:
    filtered_df = filtered_df[
        (filtered_df['SessionDate'].dt.date >= st.session_state.date_range[0]) &
        (filtered_df['SessionDate'].dt.date <= st.session_state.date_range[1])
    ]

# Show filter status
with st.sidebar:
    st.divider()
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.metric("📊 Records", f"{len(filtered_df):,}")
    with col_info2:
        filter_pct = (len(filtered_df) / len(df) * 100)
        st.metric("📈 Coverage", f"{filter_pct:.1f}%")

# ==================== SECTION 1: OVERVIEW CHARTS ====================
st.subheader("📈 Overview Metrics")
col1, col2 = st.columns(2)

with col1:
    # Sessions by Student Level
    level_counts = filtered_df['StudentLevel'].value_counts()
    fig_level = px.pie(
        values=level_counts.values,
        names=level_counts.index,
        title="Sessions by Student Level",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_level.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_level, use_container_width=True)

with col2:
    # Sessions by Discipline
    discipline_counts = filtered_df['Discipline'].value_counts().head(8)
    fig_disc = px.bar(
        x=discipline_counts.values,
        y=discipline_counts.index,
        orientation='h',
        title="Top Disciplines by Session Count",
        color=discipline_counts.values,
        color_continuous_scale='Viridis'
    )
    fig_disc.update_xaxes(title_text="Session Count")
    fig_disc.update_yaxes(title_text="")
    st.plotly_chart(fig_disc, use_container_width=True)

# ==================== SECTION 2: PERFORMANCE ANALYSIS ====================
st.subheader("🎯 Performance Analysis")
col1, col2 = st.columns(2)

with col1:
    # Task Type Distribution
    task_counts = filtered_df['TaskType'].value_counts()
    fig_task = px.bar(
        x=task_counts.index,
        y=task_counts.values,
        title="Session Distribution by Task Type",
        color=task_counts.values,
        color_continuous_scale='Blues'
    )
    fig_task.update_xaxes(title_text="Task Type")
    fig_task.update_yaxes(title_text="Count")
    st.plotly_chart(fig_task, use_container_width=True)

with col2:
    # Final Outcome Distribution
    outcome_counts = filtered_df['FinalOutcome'].value_counts()
    fig_outcome = px.pie(
        values=outcome_counts.values,
        names=outcome_counts.index,
        title="Final Outcomes Distribution",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_outcome.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_outcome, use_container_width=True)

# ==================== SECTION 3: SATISFACTION & SESSION ANALYSIS ====================
st.subheader("⭐ Satisfaction & Session Metrics")
col1, col2 = st.columns(2)

with col1:
    # Satisfaction by Assistance Level
    satisfaction_by_level = filtered_df.groupby('AI_AssistanceLevel')['SatisfactionRating'].mean().sort_index()
    fig_sat = px.bar(
        x=satisfaction_by_level.index,
        y=satisfaction_by_level.values,
        title="Average Satisfaction by AI Assistance Level",
        color=satisfaction_by_level.values,
        color_continuous_scale='RdYlGn',
        range_color=[0, 5]
    )
    fig_sat.update_xaxes(title_text="AI Assistance Level")
    fig_sat.update_yaxes(title_text="Avg Satisfaction Rating")
    st.plotly_chart(fig_sat, use_container_width=True)

with col2:
    # Session Length Distribution
    fig_length = px.histogram(
        filtered_df,
        x='SessionLengthMin',
        nbins=30,
        title="Session Duration Distribution",
        color_discrete_sequence=['#636EFA']
    )
    fig_length.update_xaxes(title_text="Session Length (Minutes)")
    fig_length.update_yaxes(title_text="Frequency")
    st.plotly_chart(fig_length, use_container_width=True)

# ==================== SECTION 4: DETAILED TRENDS ====================
st.subheader("📊 Time-Series Analysis")
col1, col2 = st.columns(2)

with col1:
    # Sessions Over Time
    sessions_by_date = filtered_df.groupby(filtered_df['SessionDate'].dt.date).size()
    fig_time = px.line(
        x=sessions_by_date.index,
        y=sessions_by_date.values,
        title="Sessions Over Time",
        markers=True,
        color_discrete_sequence=['#EF553B']
    )
    fig_time.update_xaxes(title_text="Date")
    fig_time.update_yaxes(title_text="Session Count")
    st.plotly_chart(fig_time, use_container_width=True)

with col2:
    # Prompts vs Satisfaction
    fig_scatter = px.scatter(
        filtered_df,
        x='TotalPrompts',
        y='SatisfactionRating',
        color='StudentLevel',
        title="Total Prompts vs Satisfaction Rating",
        hover_data=['Discipline', 'TaskType'],
        color_discrete_sequence=px.colors.qualitative.Set1
    )
    fig_scatter.update_xaxes(title_text="Total Prompts")
    fig_scatter.update_yaxes(title_text="Satisfaction Rating")
    st.plotly_chart(fig_scatter, use_container_width=True)

# ==================== SECTION 5: DATA TABLE ====================
st.subheader("📋 Detailed Data")
st.dataframe(
    filtered_df.sort_values('SessionDate', ascending=False).head(100),
    use_container_width=True,
    height=400
)

# ==================== SECTION 6: STATISTICS SUMMARY ====================
st.subheader("📊 Summary Statistics")
col1, col2 = st.columns(2)

with col1:
    st.write("**Dataset Overview**")
    stats_summary = {
        "Total Records": len(filtered_df),
        "Date Range": f"{filtered_df['SessionDate'].min().date()} to {filtered_df['SessionDate'].max().date()}",
        "Avg Session Length": f"{filtered_df['SessionLengthMin'].mean():.2f} min",
        "Avg Total Prompts": f"{filtered_df['TotalPrompts'].mean():.1f}",
    }
    for key, value in stats_summary.items():
        st.write(f"• {key}: {value}")

with col2:
    st.write("**Outcome Analysis**")
    outcome_stats = filtered_df['FinalOutcome'].value_counts().to_dict()
    for outcome, count in outcome_stats.items():
        percentage = (count / len(filtered_df)) * 100
        st.write(f"• {outcome}: {count} ({percentage:.1f}%)")
