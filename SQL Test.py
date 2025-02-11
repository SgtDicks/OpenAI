import openai
import sqlite3

# SQLite Database File
DB_FILE = "memories.db"

# Function to retrieve the OpenAI API key from the database
def get_api_key():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute("SELECT api_key FROM api_keys WHERE service = 'openai'")
        result = cursor.fetchone()

        conn.close()

        if result:
            return result[0]  # Return the stored API key
        else:
            raise ValueError("❌ No OpenAI API key found in the database.")

    except Exception as e:
        print("❌ Error retrieving API key:", e)
        return None  # Handle errors gracefully

# Function to fetch relevant memory from SQLite
def fetch_memory_from_db():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Fetch all stored memories
        query = "SELECT memory_text FROM memories"
        cursor.execute(query)
        results = cursor.fetchall()

        conn.close()  # Close connection

        if results:
            memory_texts = "\n".join([row[0] for row in results])
            print("✅ All Memories Retrieved:\n", memory_texts)  # Debugging output
            return memory_texts
        else:
            print("❌ No memories found in the database.")
            return "No stored memories available."

    except Exception as e:
        print("SQL Error:", e)
        return "Memory lookup failed."

# Function to get AI response with the retrieved context
def get_ai_response(user_input):
    openai_api_key = get_api_key()  # Retrieve the API key from DB
    if not openai_api_key:
        return "❌ Error: OpenAI API key not found."

    client = openai.OpenAI(api_key=openai_api_key)  # Use the retrieved key

    memory_context = fetch_memory_from_db()  # Fetch all stored memories

    # Debugging: Print what system content is being sent
    system_message = f"Here are some predefined memories: {memory_context}"
    print("\n🟢 System Content Being Sent to OpenAI:\n", system_message, "\n")

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_message},  # Provide all stored memories
            {"role": "user", "content": user_input}
        ],
        temperature=0.7,
        max_tokens=200
    )

    return response.choices[0].message.content

# Example: Get AI response using SQL memory
user_input = input("Enter your question: ")
response = get_ai_response(user_input)
print("\nAI Response:", response)

