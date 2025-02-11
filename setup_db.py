import sqlite3

# SQLite Database File
DB_FILE = "memories.db"

# Function to create the database and store the API key
def setup_database():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Create memories table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                memory_text TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Create API key storage table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS api_keys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service TEXT UNIQUE NOT NULL,
                api_key TEXT NOT NULL
            );
        """)

        # Check if an OpenAI API key already exists
        cursor.execute("SELECT COUNT(*) FROM api_keys WHERE service = 'openai'")
        count = cursor.fetchone()[0]

        if count == 0:
            # Insert OpenAI API Key (Replace with your actual key)
            cursor.execute("INSERT INTO api_keys (service, api_key) VALUES (?, ?)", 
                           ("openai", "your_actual_openai_api_key_here"))
            print("Inserted OpenAI API Key into the database.")

        conn.commit()
        conn.close()
        print("✅ Database setup complete.")

    except Exception as e:
        print("❌ Error setting up database:", e)

# Run the setup
setup_database()

