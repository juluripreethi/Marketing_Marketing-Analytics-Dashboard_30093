# File: frontend_marketing_analytics.py
import streamlit as st
import pandas as pd
from backend import (
    create_tables, create_campaign, read_campaigns,
    update_campaign, delete_campaign, get_campaign_insights
)
import datetime

st.set_page_config(layout="wide")
st.title("📊 Marketing Analytics Dashboard")

# Initialize the database and tables on first run
create_tables()

# Helper function to display data
def display_campaigns():
    """Displays campaigns in a table format."""
    st.subheader("Current Campaigns")
    campaign_data = read_campaigns()
    if campaign_data:
        df = pd.DataFrame(
            campaign_data,
            columns=['ID', 'Campaign Name', 'Start Date', 'End Date', 'Budget', 'Description']
        )
        st.dataframe(df)
    else:
        st.info("No campaigns found. Start by creating one!")

# Use tabs for a clean UI
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Campaign Management",
    "Customer Profiles",
    "Lead Tracking",
    "Marketing Asset Library",
    "Reporting & Analytics"
])

# --- Tab 1: Campaign Management (CRUD) ---
with tab1:
    st.header("Campaign Management 🚀")
    
    # Use columns to organize the CRUD operations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Add a New Campaign")
        with st.form("create_campaign_form"):
            name = st.text_input("Campaign Name")
            start_date = st.date_input("Start Date", datetime.date.today())
            end_date = st.date_input("End Date", datetime.date.today())
            budget = st.number_input("Budget", min_value=0.0, format="%.2f")
            description = st.text_area("Description")
            submit_button = st.form_submit_button("Create Campaign")
            if submit_button:
                if create_campaign(name, start_date, end_date, budget, description):
                    st.success("✅ Campaign created successfully!")
                else:
                    st.error("❌ Failed to create campaign.")

    with col2:
        st.subheader("Update or Delete Campaign")
        campaigns = read_campaigns()
        if campaigns:
            campaign_df = pd.DataFrame(campaigns, columns=['ID', 'Name', 'Start', 'End', 'Budget', 'Desc'])
            campaign_list = campaign_df.set_index('ID')['Name'].to_dict()
            selected_id = st.selectbox("Select a Campaign to Update/Delete", options=campaign_list.keys(), format_func=lambda x: campaign_list[x])

            if selected_id:
                # Find the current data for the selected campaign
                current_data = next((c for c in campaigns if c[0] == selected_id), None)
                if current_data:
                    with st.form("update_campaign_form"):
                        new_name = st.text_input("New Campaign Name", value=current_data[1])
                        new_start_date = st.date_input("New Start Date", value=current_data[2])
                        new_end_date = st.date_input("New End Date", value=current_data[3])
                        new_budget = st.number_input("New Budget", value=float(current_data[4]), format="%.2f")
                        new_description = st.text_area("New Description", value=current_data[5])
                        
                        update_col, delete_col = st.columns(2)
                        with update_col:
                            update_button = st.form_submit_button("Update Campaign")
                            if update_button:
                                if update_campaign(selected_id, new_name, new_start_date, new_end_date, new_budget, new_description):
                                    st.success("✅ Campaign updated successfully!")
                                else:
                                    st.error("❌ Failed to update campaign.")
                        with delete_col:
                            delete_button = st.form_submit_button("Delete Campaign")
                            if delete_button:
                                if st.button("Confirm Deletion"):
                                    if delete_campaign(selected_id):
                                        st.warning("⚠️ Campaign deleted.")
                                    else:
                                        st.error("❌ Failed to delete campaign.")
    
    st.markdown("---")
    display_campaigns()

# --- Tab 2-4: Placeholder tabs for other CRUD sections ---
with tab2:
    st.header("Customer Profile Management 👥")
    st.info("💡 Implement **CRUD** for Customer Profiles here, calling functions from the backend.")
    # Add forms and display logic for Customers

with tab3:
    st.header("Lead Tracking and Nurturing 🎯")
    st.info("💡 Implement **CRUD** for Leads here, including lead scoring logic.")
    # Add forms and display logic for Leads

with tab4:
    st.header("Marketing Asset Library 🗃️")
    st.info("💡 Implement **CRUD** for Marketing Assets here, allowing file uploads.")
    # Add forms and display logic for Assets

# --- Tab 5: Reporting & Analytics (Business Insights) ---
with tab5:
    st.header("Reporting & Analytics 📈")
    st.subheader("Campaign Performance Insights")
    
    insights = get_campaign_insights()
    
    if insights:
        total_campaigns = insights.get('total_campaigns')
        total_budget = insights.get('total_budget_sum')
        avg_budget = insights.get('avg_budget')
        min_budget = insights.get('min_budget')
        max_budget = insights.get('max_budget')

        col_count, col_sum, col_avg, col_min, col_max = st.columns(5)
        
        with col_count:
            st.metric(label="Total Campaigns", value=f"{total_campaigns}")
        
        with col_sum:
            st.metric(label="Total Budget Sum", value=f"${total_budget:,.2f}" if total_budget else "$0.00")
            
        with col_avg:
            st.metric(label="Average Budget", value=f"${avg_budget:,.2f}" if avg_budget else "$0.00")
            
        with col_min:
            st.metric(label="Minimum Budget", value=f"${min_budget:,.2f}" if min_budget else "$0.00")
            
        with col_max:
            st.metric(label="Maximum Budget", value=f"${max_budget:,.2f}" if max_budget else "$0.00")
            
    else:
        st.warning("No data available for insights. Please add campaigns.")
    
    # Placeholder for other reports
    st.markdown("---")
    st.subheader("Other Reports")
    st.info("Campaign Performance Report, Customer Segmentation Report, and data export features can be implemented here.")
