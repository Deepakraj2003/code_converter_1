import boto3
from botocore.exceptions import ClientError

# Create a Bedrock Runtime client in the AWS Region you want to use.
# client = boto3.client("bedrock-runtime", region_name="ap-south-1")

# # Set the model ID, e.g., Titan Text Premier.
# model_id = "mistral.mistral-7b-instruct-v0:2"

# # Start a conversation with the user message.
# user_message = """[INST]python code to check if a number is a palindrome."[/INST][INST]only give the code without any description or words[/INST][INST]not give as string[/INST]"""
# conversation = [
#     {
#         "role": "user",
#         "content": [{"text": user_message}],
#     }
# ]

# try:
#     # Send the message to the model, using a basic inference configuration.
#     response = client.converse(
#         modelId=model_id,
#         messages=conversation,
#         inferenceConfig={"maxTokens":400, "temperature":0.1, "topP":0.7},
#         additionalModelRequestFields={"top_k":50}
#     )

#     # Extract and print the response text.
#     response_text = response.get("output", {}).get("message", {}).get("content", [{}])[0].get("text", "No text found")
#     print(response_text)

# except (ClientError, Exception) as e:
#     print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
#     exit(1)
import boto3

MISTRAL_LARGE_BEDROCK_ID = "mistral.mistral-large-2402-v1:0"
AWS_REGION = "ap-south-1"

bedrock_client = boto3.client(service_name='bedrock-runtime', region_name=AWS_REGION)

messages = [{"role": "user", "content": [{"text": """[INST]PYTHON code to check if a number is a palindrome.WITH TEST CASES"[/INST][INST]only give the code without any description or words[/INST][INST]print the code not as a string datatype[/INST]"""}]}]
temperature = 0.0
max_tokens = 1024

params = {"modelId": MISTRAL_LARGE_BEDROCK_ID,
          "messages": messages,
          "inferenceConfig": {"temperature": temperature,
                              "maxTokens": max_tokens}}

resp = bedrock_client.converse(**params)

print(resp["output"]["message"]["content"][0]["text"])