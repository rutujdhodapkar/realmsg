import streamlit as st
import pandas as pd
import os

# Function to initialize and read messages
def get_messages():
    # Check if the CSV exists and has data
    if os.path.exists('msg.csv') and os.stat('msg.csv').st_size > 0:
        try:
            df = pd.read_csv('msg.csv')
            return df
        except pd.errors.EmptyDataError:
            # If there's an error reading due to empty file, return an empty DataFrame
            return pd.DataFrame(columns=["username", "message"])
    else:
        # If the file doesn't exist or is empty, return an empty DataFrame
        return pd.DataFrame(columns=["username", "message"])

# Function to update the CSV with new messages
def update_messages(message, username):
    # Get current messages
    df = get_messages()
    
    # Create new message as a DataFrame
    new_message = pd.DataFrame({"username": [username], "message": [message]})
    
    # Concatenate the new message with the existing DataFrame
    df = pd.concat([df, new_message], ignore_index=True)
    
    # Keep only the last 10 messages
    df = df.tail(10)
    
    # Save the updated messages to the CSV
    df.to_csv('msg.csv', index=False)

# Streamlit UI components
st.title("Message Board")

# User input for username
username = st.text_input("Enter your username:", "")

# Proceed if the username is entered
if username:
    # Show message input box when username is provided
    message = st.text_input("Enter your message:", "")
    send_button = st.button("Send")

    if send_button and message:
        update_messages(message, username)
        st.success("Message sent!")

# Display the last 10 messages from the CSV
st.subheader("Last 10 messages:")

# Show content of the CSV file below the messages
st.subheader("Content of the 'msg.csv' file:")
df = get_messages()  # Get the current messages from CSV
if not df.empty:
    st.write(df)  # Show the DataFrame in the UI
else:
    st.write("No messages in the file yet.")

# Container to display messages
message_container = st.empty()

# Display the last 10 messages
if not df.empty:
    # Display messages from the CSV file
    message_container.empty()
    for i, row in df.iterrows():
        message_container.write(f"{row['username']}: {row['message']}")
else:
    message_container.write("No messages yet.")
