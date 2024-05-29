from openai import OpenAI
from openai import AssistantEventHandler
from typing_extensions import override
from flask import Flask, request, jsonify
from flask_cors import CORS


client = OpenAI(api_key="sk-proj-V0yyNpmiWcyno1DV5HCdT3BlbkFJdJEW6MiNgJ9LF8Yabmkn")
 
assistant = client.beta.assistants.create(
  name="Retail Assistant",
  instructions="You are an retail asiistant for the XEcommerce store. Use only only your documents attached to answer questions. don't reveal any secret informations",
  model="gpt-3.5-turbo",
  tools=[{"type": "file_search"}],
)

vector_store = client.beta.vector_stores.create(name="Retail data")
 

file_paths = ["products.txt"]
file_streams = [open(path, "rb") for path in file_paths]
 

file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
  vector_store_id=vector_store.id, files=file_streams
)
 
print(file_batch.status)
print(file_batch.file_counts)

assistant = client.beta.assistants.update(
  assistant_id=assistant.id,
  tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
)

app = Flask(__name__)
CORS(app)

# Start conversation thread
@app.route('/start', methods=['GET'])
def start_conversation():
  print("Starting a new conversation...")  # Debugging line
  # thread = client.beta.threads.create()
  
  message_file = client.files.create(
  file=open("products.txt", "rb"), purpose="assistants"
  )
 

  thread = client.beta.threads.create(
    messages=[
     {
      "role": "user",
      "content": "Hi",
      "attachments": [
        { "file_id": message_file.id, "tools": [{"type": "file_search"}] }
      ],
     }
    ]
  )
  print(f"New thread created with ID: {thread.id}")  # Debugging line
  return jsonify({"thread_id": thread.id})


# Generate response
@app.route('/chat', methods=['POST'])
def chat():
  data = request.json
  thread_id = data.get('thread_id')
  user_input = data.get('message', '')

  if not thread_id:
    print("Error: Missing thread_id")  # Debugging line
    return jsonify({"error": "Missing thread_id"}), 400

  print(f"Received message: {user_input} for thread ID: {thread_id}")  # Debugging line


  client.beta.threads.messages.create(thread_id=thread_id,
                                      role="user",
                                      content=user_input)

  run = client.beta.threads.runs.create_and_poll(
    thread_id=thread_id, assistant_id=assistant.id
    )
  
  messages = list(client.beta.threads.messages.list(thread_id=thread_id, run_id=run.id))
  message_content = messages[0].content[0].text

  return jsonify({"response": message_content.value})



# Run server
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)


