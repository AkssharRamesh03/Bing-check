
import json
import os

def create_assistant(client):
  assistant_file_path = 'assistant.json'

  if os.path.exists(assistant_file_path):
    with open(assistant_file_path, 'r') as file:
      assistant_data = json.load(file)
      assistant_id = assistant_data['assistant_id']
      print("Loaded existing assistant ID.")
  else:
    file = client.files.create(file=open("products.txt", "rb"),
                               purpose='assistants')

    assistant = client.beta.assistants.create(instructions="""
          You are an expert retail chat bot for the XEcommerce store. Use you knowledge base to answer questions about products and services.
          """,
                                              model="gpt-4-turbo",
                                              tools=[{
                                                  "type": "retrieval"
                                              }],
                                              file=[file.id])

    with open(assistant_file_path, 'w') as file:
      json.dump({'assistant_id': assistant.id}, file)
      print("Created a new assistant and saved the ID.")

  return assistant