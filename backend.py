# File: backend_marketing_analytics.py
import psycopg2

def create_connection():
    """Establishes a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="Marketing Analytics Tracker",
            user="postgres",
            password="1234"
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def create_tables():
    """Creates the necessary tables for the application."""
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS campaigns (
                    campaign_id SERIAL PRIMARY KEY,
                    campaign_name VARCHAR(255) NOT NULL,
                    start_date DATE,
                    end_date DATE,
                    budget DECIMAL,
                    description TEXT
                );
                CREATE TABLE IF NOT EXISTS customers (
                    customer_id SERIAL PRIMARY KEY,
                    customer_name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    demographics TEXT,
                    source_of_acquisition VARCHAR(255)
                );
                CREATE TABLE IF NOT EXISTS leads (
                    lead_id SERIAL PRIMARY KEY,
                    campaign_id INTEGER REFERENCES campaigns(campaign_id),
                    contact_info VARCHAR(255),
                    lead_source VARCHAR(255),
                    status VARCHAR(50),
                    lead_score INTEGER
                );
                CREATE TABLE IF NOT EXISTS assets (
                    asset_id SERIAL PRIMARY KEY,
                    asset_name VARCHAR(255),
                    description TEXT,
                    file_type VARCHAR(50),
                    file_path VARCHAR(255)
                );
            """)
            conn.commit()
            print("Tables created successfully.")
        except psycopg2.Error as e:
            print(f"Error creating tables: {e}")
        finally:
            cursor.close()
            conn.close()

# --- CRUD Functions for Campaigns ---

def create_campaign(name, start_date, end_date, budget, description):
    """Adds a new campaign to the database."""
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO campaigns (campaign_name, start_date, end_date, budget, description) VALUES (%s, %s, %s, %s, %s);",
                (name, start_date, end_date, budget, description)
            )
            conn.commit()
            return True
        except psycopg2.Error as e:
            print(f"Error creating campaign: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

def read_campaigns():
    """Retrieves all campaigns from the database."""
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM campaigns;")
            campaigns = cursor.fetchall()
            return campaigns
        except psycopg2.Error as e:
            print(f"Error reading campaigns: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

def update_campaign(campaign_id, name, start_date, end_date, budget, description):
    """Updates an existing campaign."""
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE campaigns SET campaign_name = %s, start_date = %s, end_date = %s, budget = %s, description = %s WHERE campaign_id = %s;",
                (name, start_date, end_date, budget, description, campaign_id)
            )
            conn.commit()
            return True
        except psycopg2.Error as e:
            print(f"Error updating campaign: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

def delete_campaign(campaign_id):
    """Deletes a campaign from the database."""
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM campaigns WHERE campaign_id = %s;", (campaign_id,))
            conn.commit()
            return True
        except psycopg2.Error as e:
            print(f"Error deleting campaign: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

# --- Business Insights Functions ---

def get_campaign_insights():
    """Calculates and returns key business insights."""
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT
                    COUNT(campaign_id) AS total_campaigns,
                    SUM(budget) AS total_budget_sum,
                    AVG(budget) AS avg_budget,
                    MIN(budget) AS min_budget,
                    MAX(budget) AS max_budget
                FROM campaigns;
            """)
            insights = cursor.fetchone()
            return {
                "total_campaigns": insights[0],
                "total_budget_sum": insights[1],
                "avg_budget": insights[2],
                "min_budget": insights[3],
                "max_budget": insights[4]
            }
        except psycopg2.Error as e:
            print(f"Error getting insights: {e}")
            return {}
        finally:
            cursor.close()
            conn.close()
