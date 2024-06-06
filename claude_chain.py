# claude_chain.py
import boto3
import json
from langchain.memory import ConversationBufferMemory

class ClaudeChain:
    def __init__(self, memory: ConversationBufferMemory):
        self.client = boto3.client('bedrock-runtime', region_name='eu-west-3')  # Specify your AWS region
        self.memory = memory

    def call_api(self, user_input):
        # Collect the conversation history
        messages = self.memory.chat_memory.messages
        chat_history = [{"role": "user" if msg.type == "human" else "assistant", "content": msg.content} for msg in messages]
        
        # Add the current user input to the chat history
        chat_history.append({"role": "user", "content": user_input})

        response = self.client.invoke_model(
            modelId="anthropic.claude-3-sonnet-20240229-v1:0",
            contentType="application/json",
            accept="application/json",
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "messages": chat_history
            })
        )

        response_body = json.loads(response['body'].read().decode())
        try:
            completion = self.extract_text_content(response_body)
            self.memory.save_context({"input": user_input}, {"output": completion})
            return completion
        except (KeyError, ValueError) as e:
            raise ValueError(f"Error calling Claude API: {response_body}") from e

    def extract_text_content(self, response_body):
        try:
            content = response_body['content']
            text_parts = [part['text'] for part in content if part['type'] == 'text']
            return ''.join(text_parts)
        except KeyError:
            raise ValueError(f"Error extracting text content from response: {response_body}")

    def clear_memory(self):
        self.memory.clear()
