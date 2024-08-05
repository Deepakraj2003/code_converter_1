# # Use the Converse API to send a text message to Mistral 7B Instruct.

# import boto3
# from botocore.exceptions import ClientError

# # Create a Bedrock Runtime client in the AWS Region you want to use.
# client = boto3.client("bedrock-runtime", region_name="ap-south-1")

# # Set the model ID, e.g., Titan Text Premier.
# model_id = "mistral.mistral-7b-instruct-v0:2"

# # Start a conversation with the user message.
# user_message = """<s>[INST]write python code to check a number  is plandrome number[/INST]"""
# conversation = [
#     {
#         "role": "user",
#         "content": [{"text": user_message}],
#     }
# ]

# try:
#     # Send the message to the model, using a basic inference configuration.
#     response = client.converse(
#         modelId="mistral.mistral-7b-instruct-v0:2",
#         messages=conversation,
#         inferenceConfig={"maxTokens":400,"temperature":0.1,"topP":0.7},
#         additionalModelRequestFields={"top_k":50}
#     )

#     # Extract and print the response text.
#     response_text = response["output"]["message"]["content"][0]["text"]
#     print(response_text)

# except (ClientError, Exception) as e:
#     print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
#     exit(1)


import boto3
import os
import json
from botocore.exceptions import ClientError

# Create a Bedrock Runtime client in the AWS Region you want to use.
client = boto3.client("bedrock-runtime", region_name="ap-south-1")

# Set the model ID.
model_id = "mistral.mistral-7b-instruct-v0:2"

def convert_code(source_code, source_language, target_language):
    # Construct the message for the API call
    user_message = f"""[INST]First understand the whole {source_code} in {source_language} and find what function is it doing.After understanging the{source_code} write in the {target_language} which replicates the same functionality with correct output[/INST]
    [INST]give only the code without the description or any extra strings[/INST]
    [INST]write the code not in string formate or not with enclosed by '''[/INST] 
    [INST]follow the above rules for all the files in the folder[/INST]"""
    conversation = [
        {
            "role": "user",
            "content": [{"text": user_message}],
        }
    ]

    try:
        # Send the message to the model
        response = client.converse(
            modelId=model_id,
            messages=conversation,
            inferenceConfig={"maxTokens": 400, "temperature": 0.5, "topP": 0.5},
            additionalModelRequestFields={"top_k": 50}
        )

        # Extract and return the response text
        response_text = response["output"]["message"]["content"][0]["text"]
        response_json = {
            "source_language": source_language,
            "target_language": target_language,
            "source_code": source_code,
            "converted_code": response_text
        }
        return response_json

    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
        return None

def read_files_from_folder(folder_path):
    code_files = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                code_files.append((filename, file.read()))
    return code_files

def write_converted_files(output_folder_path, converted_files, target_extension):
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)
    for filename, code_json in converted_files:
        base_filename, _ = os.path.splitext(filename)
        new_filename = base_filename + target_extension
        code = code_json["converted_code"]
        with open(os.path.join(output_folder_path, new_filename), 'w') as file:
            file.write(code)

        # Write the JSON response to a file for reference
        json_filename = base_filename + '.json'
        with open(os.path.join(output_folder_path, json_filename), 'w') as file:
            json.dump(code_json, file, indent=4)

def main():
    input_folder_path = 'test'
    output_folder_path = 'test1'
    source_language = 'Python'
    target_language = 'JavaScript'
    target_extension = '.js'  # Adjust the extension based on the target language

    code_files = read_files_from_folder(input_folder_path)
    converted_files = []

    for filename, code in code_files:
        print(f"Converting {filename}...")
        converted_code_json = convert_code(code, source_language, target_language)
        if converted_code_json is not None:
            converted_files.append((filename, converted_code_json))
        else:
            print(f"Failed to convert {filename}")

    write_converted_files(output_folder_path, converted_files, target_extension)

if __name__ == "__main__":
    main()
