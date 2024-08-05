import boto3
import os
import json
from botocore.exceptions import ClientError

# Create a Bedrock Runtime client in the AWS Region you want to use.
client = boto3.client("bedrock-runtime", region_name="ap-south-1")

# Set the model ID.
model_id = "mistral.mistral-7b-instruct-v0:2"

def convert_code(source_code, target_language):
    # Construct the message for the API call
    user_message = f"""[INST]Read and understand the provided code. Then translate the code into {target_language} without changing its logic or functionality."[/INST]
    [INST]Note: Provide only the code without any description or additional text.[/INST][INST]Do not print the code as a string.[/INST]"""

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
            try:
                with open(file_path, 'r', errors='ignore') as file:
                    code_files.append((filename, file.read()))
            except Exception as e:
                print(f"ERROR: Could not read file '{filename}'. Reason: {e}")
    return code_files

def write_converted_files(output_folder_path, converted_files):
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)
    for filename, code_json in converted_files:
        base_filename, _ = os.path.splitext(filename)
        new_filename = base_filename + '.js'
        code = code_json["converted_code"]
        try:
            with open(os.path.join(output_folder_path, new_filename), 'w') as file:
                file.write(code)
        except Exception as e:
            print(f"ERROR: Could not write file '{new_filename}'. Reason: {e}")

        # Write the JSON response to a file for reference
        json_filename = base_filename + '.json'
        try:
            with open(os.path.join(output_folder_path, json_filename), 'w') as file:
                json.dump(code_json, file, indent=4)
        except Exception as e:
            print(f"ERROR: Could not write JSON file '{json_filename}'. Reason: {e}")

def main():
    input_folder_path = 'test'
    output_folder_path = 'test1'  # Updated output folder path
    target_language = 'JavaScript'
    
    code_files = read_files_from_folder(input_folder_path)
    converted_files = []

    for filename, code in code_files:
        print(f"Converting {filename}...")
        converted_code_json = convert_code(code, target_language)
        if converted_code_json is not None:
            converted_files.append((filename, converted_code_json))
        else:
            print(f"Failed to convert {filename}")

    write_converted_files(output_folder_path, converted_files)

if __name__ == "__main__":
    main()
