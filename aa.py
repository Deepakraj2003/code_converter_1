# import boto3
# import json

# # Initialize the Bedrock client
# bedrock = boto3.client(service_name="bedrock-runtime", region_name='ap-south-1')

# # Define the prompt
# prompt = """
# <s>[INST]You are code converting system. Now write the code for checking if a number is a palindrome or not in JS.[/INST]"""

# # Define the body of the request
# body = json.dumps({
#     "prompt": prompt,
#     "max_tokens": 512,
#     "top_p": 0.8,
#     "temperature": 0.5,
# })

# # Model ID
# modelId = "mistral.mistral-large-2402-v1:0"

# # Define accept and contentType
# accept = "application/json"
# contentType = "application/json"

# # Invoke the model
# response = bedrock.invoke_model(
#     body=body,
#     modelId=modelId,
#     accept=accept,
#     contentType=contentType
# )

# # Read and decode the response body
# response_body_str = response['body'].read().decode('utf-8')

# # Parse the JSON content
# response_body = json.loads(response_body_str)

# # Extract the text
# output_text = response_body['outputs'][0]['text']

# # Extract and print only the code from the output
# start_index = output_text.find("```javascript\n") + len("```javascript\n")
# end_index = output_text.find("\n```", start_index)
# code = output_text[start_index:end_index]

# print(code)

import boto3
import json
import os

# Initialize the Bedrock client
bedrock = boto3.client(service_name="bedrock-runtime", region_name='ap-south-1')

def translate_code(input_code: str) -> str:
    # Define the prompt with the input code
    prompt = f"""
    <s>[INST]You are code converting system. Convert the following  code to JavaScript or its revelent frame work that possible only at extent case:\n\n{input_code}.use the most revelent package or module available in specified programing laguage to perform actions[/INST]"""

    # Define the body of the request
    body = json.dumps({
        "prompt": prompt,
        "max_tokens": 1024,
        "top_p": 0.8,
        "temperature": 0.5,
    })

    # Model ID
    modelId = "mistral.mistral-large-2402-v1:0"

    # Define accept and contentType
    accept = "application/json"
    contentType = "application/json"

    # Invoke the model
    response = bedrock.invoke_model(
        body=body,
        modelId=modelId,
        accept=accept,
        contentType=contentType
    )

    # Read and decode the response body
    response_body_str = response['body'].read().decode('utf-8')

    # Parse the JSON content
    response_body = json.loads(response_body_str)

    # Extract the text
    output_text = response_body['outputs'][0]['text']

    # Extract the code from the output text
    start_index = output_text.find("```javascript\n") + len("```javascript\n")
    end_index = output_text.find("\n```", start_index)
    code = output_text[start_index:end_index]

    return code

def convert_files_in_folder(input_folder: str, output_folder: str):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate over all files in the input folder
    for filename in os.listdir(input_folder):
        input_file_path = os.path.join(input_folder, filename)
        if os.path.isfile(input_file_path):
            # Read the input file
            with open(input_file_path, 'r') as input_file:
                input_code = input_file.read()

            # Translate the code to JavaScript
            javascript_code = translate_code(input_code)

            # Define the output file path
            output_filename = os.path.splitext(filename)[0] + '.js'
            output_file_path = os.path.join(output_folder, output_filename)

            # Write the translated code to the output file
            with open(output_file_path, 'w') as output_file:
                output_file.write(javascript_code)

# Example usage
input_folder = 'exe'
output_folder = 'converted_js'
convert_files_in_folder(input_folder, output_folder)
