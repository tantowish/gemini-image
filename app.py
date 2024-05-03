"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""

from pathlib import Path
import hashlib
import google.generativeai as genai

genai.configure(api_key="")

# Set up the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

uploaded_files = []
def upload_if_needed(pathname: str) -> list[str]:
  path = Path(pathname)
  hash_id = hashlib.sha256(path.read_bytes()).hexdigest()
  try:
    existing_file = genai.get_file(name=hash_id)
    return [existing_file.uri]
  except:
    pass
  uploaded_files.append(genai.upload_file(path=path, display_name=hash_id))
  print(uploaded_files[-1].uri)
  return [uploaded_files[-1].uri]

convo = model.start_chat(history=[
  {
    "role": "user",
    "parts": ["File \"C:\\Users\\tanto\\AppData\\Local\\Programs\\Python\\Python310\\lib\\site-packages\\google\\api_core\\grpc_helpers.py\", line 76, in error_remapped_callable\n    return callable_(*args, **kwargs)\n  File \"C:\\Users\\tanto\\AppData\\Local\\Programs\\Python\\Python310\\lib\\site-packages\\grpc\\_channel.py\", line 1181, in __call__\n    return _end_unary_response_blocking(state, call, False, None)\n  File \"C:\\Users\\tanto\\AppData\\Local\\Programs\\Python\\Python310\\lib\\site-packages\\grpc\\_channel.py\", line 1006, in _end_unary_response_blocking    \n    raise _InactiveRpcError(state)  # pytype: disable=not-instantiable\ngrpc._channel._InactiveRpcError: <_InactiveRpcError of RPC that terminated with:\n        status = StatusCode.INVALID_ARGUMENT\n        details = \"* GetFileRequest.name: File ID (name excluding 'files/') cannot be more than 40 characters.\n\"\n        debug_error_string = \"UNKNOWN:Error received from peer ipv4:142.250.4.95:443 {grpc_message:\"* GetFileRequest.name: File ID (name excluding \\'files/\\') cannot be more than 40 characters.\\n\", grpc_status:3, created_time:\"2024-05-03T02:18:16.0127492+00:00\"}\"\n>\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File \"C:\\Users\\tanto\\AppData\\Local\\Programs\\Python\\Python310\\lib\\site-packages\\flask\\app.py\", line 1478, in __call__\n    return self.wsgi_app(environ, start_response)\n  File \"C:\\Users\\tanto\\AppData\\Local\\Programs\\Python\\Python310\\lib\\site-packages\\flask\\app.py\", line 1458, in wsgi_app\n    response = self.handle_exception(e)\n  File \"C:\\Users\\tanto\\AppData\\Local\\Programs\\Python\\Python310\\lib\\site-packages\\flask\\app.py\", line 1455, in wsgi_app\n    response = self.full_dispatch_request()\n  File \"C:\\Users\\tanto\\AppData\\Local\\Programs\\Python\\Python310\\lib\\site-packages\\flask\\app.py\", line 869, in full_dispatch_request\n    rv = self.handle_user_exception(e)\n  File \"C:\\Users\\tanto\\AppData\\Local\\Programs\\Python\\Python310\\lib\\site-packages\\flask\\app.py\", line 867, in full_dispatch_request\n    rv = self.dispatch_request()\n  File \"C:\\Users\\tanto\\AppData\\Local\\Programs\\Python\\Python310\\lib\\site-packages\\flask\\app.py\", line 852, in dispatch_request\n    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)\n  File \"d:\\Code\\Carigi\\dental-AI\\app.py\", line 418, in classify_route\n    \"parts\": [genai.get_file(name=file_path)]\n  File \"C:\\Users\\tanto\\AppData\\Local\\Programs\\Python\\Python310\\lib\\site-packages\\google\\generativeai\\files.py\", line 68, in get_file\n    return file_types.File(client.get_file(name=name))\n  File \"C:\\Users\\tanto\\AppData\\Local\\Programs\\Python\\Python310\\lib\\site-packages\\google\\ai\\generativelanguage_v1beta\\services\\file_service\\client.py\", line 914, in get_file\n    response = rpc(\n  File \"C:\\Users\\tanto\\AppData\\Local\\Programs\\Python\\Python310\\lib\\site-packages\\google\\api_core\\gapic_v1\\method.py\", line 131, in __call__       \n    return wrapped_func(*args, **kwargs)\n  File \"C:\\Users\\tanto\\AppData\\Local\\Programs\\Python\\Python310\\lib\\site-packages\\google\\api_core\\grpc_helpers.py\", line 78, in error_remapped_callable\n    raise exceptions.from_grpc_error(exc) from exc\ngoogle.api_core.exceptions.InvalidArgument: 400 * GetFileRequest.name: File ID (name excluding 'files/') cannot be more than 40 characters.       \n\nim using s3 bucker fot the image for genai"]
  },
  {
    "role": "model",
    "parts": ["## Troubleshooting `google.api_core.exceptions.InvalidArgument` Error with Generative AI and S3\n\nThe error message indicates that the file ID you're using with Generative AI exceeds the allowed 40-character limit. This is likely due to how you're referencing files from your S3 bucket. Let's break down the issue and explore potential solutions:\n\n**Problem:**\n\n* You are using Generative AI to process images stored in an S3 bucket. \n* The file IDs (names excluding the `files/` prefix) in your S3 bucket are longer than 40 characters.\n* When Generative AI attempts to access these files using the `get_file` method, it encounters the `InvalidArgument` error due to the length restriction.\n\n**Potential Solutions:**\n\n1. **Shorten File IDs:**\n    * **Rename files in your S3 bucket:**  If feasible, rename the files in your S3 bucket to have shorter IDs that comply with the 40-character limit. This is the most straightforward solution but might not be practical if you have a large number of files or if the file names are used elsewhere in your system.\n    * **Create a mapping:**  Maintain a separate mapping between short IDs and the actual S3 file paths. Use the short IDs when interacting with Generative AI and translate them to the actual S3 paths when needed.\n\n2. **Utilize Pre-signed URLs:**\n    * Instead of directly using file IDs, generate pre-signed URLs for the S3 objects. These URLs provide temporary access to the files and can be used with Generative AI without exceeding the character limit.\n    * Libraries like `boto3` (for AWS SDK) can help you generate pre-signed URLs.\n\n3. **Alternative Storage:**\n    * If shortening file IDs or using pre-signed URLs is not suitable, consider storing the files in a different location that allows longer IDs, such as Google Cloud Storage, and then access them from Generative AI. \n\n**Implementation Tips:**\n\n* **Review your S3 file naming convention:**  Analyze your current naming strategy and identify ways to shorten file IDs while still maintaining clarity and uniqueness.\n* **Use a UUID generator:** Consider using universally unique identifiers (UUIDs) to generate shorter and unique IDs for your files.\n* **Handle errors gracefully:** Implement error handling in your code to catch potential `InvalidArgument` exceptions and provide informative messages to the user.\n\n**Additional Considerations:**\n\n* **Security:**  If using pre-signed URLs, ensure they have appropriate expiration times and access controls to prevent unauthorized access to your S3 files.\n* **Cost:**  Evaluate the cost implications of different storage solutions and choose the most cost-effective option for your needs.\n* **Performance:**  Consider the performance implications of different approaches, particularly if you are dealing with large files or high-volume processing.\n\nBy implementing one or a combination of these solutions, you should be able to resolve the `InvalidArgument` error and successfully use Generative AI with your S3 files."]
  },
  {
    "role": "user",
    "parts": ["File \"C:\\Users\\tanto\\AppData\\Local\\Programs\\Python\\Python310\\lib\\site-packages\\google\\api_core\\grpc_helpers.py\", line 76, in error_remapped_callable\n    return callable_(*args, **kwargs)\n  File \"C:\\Users\\tanto\\AppData\\Local\\Programs\\Python\\Python310\\lib\\site-packages\\grpc\\_channel.py\", line 1181, in __call__\n    return _end_unary_response_blocking(state, call, False, None)\n  File \"C:\\Users\\tanto\\AppData\\Local\\Programs\\Python\\Python310\\lib\\site-packages\\grpc\\_channel.py\", line 1006, in _end_unary_response_blocking    \n    raise _InactiveRpcError(state)  # pytype: disable=not-instantiable\ngrpc._channel._InactiveRpcError: <_InactiveRpcError of RPC that terminated with:\n        status = StatusCode.INVALID_ARGUMENT\n        details = \"* GetFileRequest.name: File ID (name excluding 'files/') cannot be more than 40 characters.\n\"\n        debug_error_string = \"UNKNOWN:Error received from peer ipv4:74.125.200.95:443 {grpc_message:\"* GetFileRequest.name: File ID (name excluding \\'files/\\') cannot be more than 40 characters.\\n\", grpc_status:3, created_time:\"2024-05-03T02:25:09.6694011+00:00\"}\"\n>\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File \"C:\\Users\\tanto\\AppData\\Local\\Programs\\Python\\Python310\\lib\\site-packages\\flask\\app.py\", line 1478, in __call__\n    return self.wsgi_app(environ, start_response)\n  File \"C:\\Users\\tanto\\AppData\\Local\\Programs\\Python\\Python310\\lib\\site-packages\\flask\\app.py\", line 1458, in wsgi_app\n    response = self.handle_exception(e)\n  File \"C:\\Users\\tanto\\AppData\\Local\\Programs\\Python\\Python310\\lib\\site-packages\\flask\\app.py\", line 1455, in wsgi_app\n    response = self.full_dispatch_request()\n  File \"C:\\Users\\tanto\\AppData\\Local\\Programs\\Python\\Python310\\lib\\site-packages\\flask\\app.py\", line 869, in full_dispatch_request\n    rv = self.handle_user_exception(e)\n  File \"C:\\Users\\tanto\\AppData\\Local\\Programs\\Python\\Python310\\lib\\site-packages\\flask\\app.py\", line 867, in full_dispatch_request\n    rv = self.dispatch_request()\n  File \"C:\\Users\\tanto\\AppData\\Local\\Programs\\Python\\Python310\\lib\\site-packages\\flask\\app.py\", line 852, in dispatch_request\n    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)\n  File \"d:\\Code\\Carigi\\dental-AI\\app.py\", line 419, in classify_route\n    parts.append(genai.get_file(name=file_path))\n  File \"C:\\Users\\tanto\\AppData\\Local\\Programs\\Python\\Python310\\lib\\site-packages\\google\\generativeai\\files.py\", line 68, in get_file\n    return file_types.File(client.get_file(name=name))\n  File \"C:\\Users\\tanto\\AppData\\Local\\Programs\\Python\\Python310\\lib\\site-packages\\google\\ai\\generativelanguage_v1beta\\services\\file_service\\client.py\", line 914, in get_file\n    response = rpc(\n  File \"C:\\Users\\tanto\\AppData\\Local\\Programs\\Python\\Python310\\lib\\site-packages\\google\\api_core\\gapic_v1\\method.py\", line 131, in __call__       \n    return wrapped_func(*args, **kwargs)\n  File \"C:\\Users\\tanto\\AppData\\Local\\Programs\\Python\\Python310\\lib\\site-packages\\google\\api_core\\grpc_helpers.py\", line 78, in error_remapped_callable\n    raise exceptions.from_grpc_error(exc) from exc\ngoogle.api_core.exceptions.InvalidArgument: 400 * GetFileRequest.name: File ID (name excluding 'files/') cannot be more than 40 characters.       \n\nstill error"]
  },
  {
    "role": "model",
    "parts": ["## Persistent `InvalidArgument` Error with Generative AI and S3\n\nI understand that you're still encountering the `InvalidArgument` error despite attempting to address the file ID length issue. Let's delve deeper and explore other potential causes and solutions:\n\n**Further Investigation:**\n\n1. **Verify File Path:**\n    * **Double-check the `file_path` variable:** Ensure it contains the correct path to the file within your S3 bucket, excluding the `files/` prefix.\n    * **Validate S3 bucket and object names:** Confirm that both your bucket name and object key (file name) adhere to S3's naming conventions and character limitations. \n    * **Check for special characters:** Ensure the file path doesn't contain any unsupported special characters that might interfere with the API call.\n\n2. **Review Generative AI Configuration:**\n    * **Authentication:** Verify that you have properly authenticated your Generative AI client with the necessary credentials and permissions to access your S3 bucket.\n    * **API version:** Check if you are using the correct version of the Generative AI API and that it supports accessing files from S3.\n    * **Region:** Ensure that you are using the appropriate region for both your S3 bucket and Generative AI service. \n\n3. **Inspect Network Connectivity:**\n    * **Firewall rules:** Verify that your firewall settings allow outbound connections to the Generative AI service and S3 endpoints.\n    * **Network restrictions:** Check if any network restrictions or proxy settings are interfering with the API calls.\n\n4. **Debugging Steps:**\n\n    * **Print the `file_path` variable:**  Print the value of `file_path` before calling `genai.get_file` to confirm its accuracy.\n    * **Use a debugger:** Employ a debugger to step through your code and inspect variables at each stage to pinpoint the exact location of the error.\n    * **Check Generative AI and S3 logs:** Review the logs for any additional error messages or clues that might shed light on the issue.\n\n**Additional Troubleshooting Tips:**\n\n* **Isolate the issue:** Try accessing the file directly using the AWS SDK or S3 CLI to rule out any issues specific to Generative AI.\n* **Test with a different file:** Attempt to access a different file in your S3 bucket to see if the problem persists.\n* **Consult documentation:** Refer to the official documentation for Generative AI and S3 for troubleshooting guidance and best practices.\n\nIf you've gone through these steps and the issue persists, please provide more details about your environment, code snippets, and any error messages you're encountering. This will help me assist you further in resolving the problem."]
  },
  {
    "role": "user",
    "parts": ["https://nos.jkt-1.neo.id/digman-ai/3a9277b7ca7d4aab8623df59adc93112.jpeg\n\nthis is my file path"]
  },
  {
    "role": "model",
    "parts": ["## Analyzing Your File Path and Potential Issues\n\nThank you for providing the file path. Let's analyze it and consider potential causes for the persistent error:\n\n**Observations:**\n\n* **URL format:** The file path you provided is a URL, suggesting that the file is publicly accessible via HTTP. \n* **Length:** The file path appears to be within the 40-character limit, assuming the file ID is the portion after the last slash (`3a9277b7ca7d4aab8623df59adc93112.jpeg`).\n* **File type:** The file extension indicates that it is a JPEG image.\n\n**Potential Causes and Solutions:**\n\n1. **Generative AI Compatibility:**\n\n    * **Direct URL Access:**  Generative AI's `get_file` method might not support directly accessing files through a URL. It is primarily designed to work with file IDs within the Generative AI ecosystem or integrated storage solutions. \n    * **Solution:** Download the image locally or to a supported storage service (e.g., Google Cloud Storage) and then use the appropriate file ID or path with `get_file`.\n\n2. **Authentication and Access Control:**\n\n    * **Public Access:**  While the URL suggests public access, there might be restrictions or authentication requirements in place. \n    * **Solution:** Verify if any authentication is needed to access the file. If so, provide the necessary credentials when making the request.\n\n3. **File Format and Content:**\n\n    * **Image Compatibility:**  Generative AI might have specific requirements or limitations regarding image formats and content. \n    * **Solution:** Ensure that the JPEG image adheres to any size, resolution, or content restrictions imposed by Generative AI. You might need to pre-process or convert the image if necessary.\n\n4. **Alternative Approach:**\n\n    * **Direct API Integration:**  Instead of using the `get_file` method, explore alternative methods within the Generative AI API that allow you to provide image data directly as input. This might involve encoding the image data or using streaming mechanisms.\n\n**Recommendations:**\n\n* **Test local file access:** Try using `get_file` with a local file path to verify if the issue is specific to accessing files via URL.\n* **Consult API documentation:** Review the Generative AI API documentation for supported file access methods and any requirements or limitations related to image processing.\n* **Explore SDK options:**  Investigate the available SDKs or libraries for Generative AI to see if they offer alternative methods for providing image input.\n\nBy understanding the nature of the file path and considering these potential causes, you can narrow down the source of the error and find an appropriate solution to successfully utilize the image with Generative AI."]
  },
  {
    "role": "user",
    "parts": upload_if_needed("./image0.jpeg")
  },
  {
    "role": "user",
    "parts": ["sadasd"]
  }
])

convo.send_message("YOUR_USER_INPUT")
print(convo.last.text)
for uploaded_file in uploaded_files:
  genai.delete_file(name=uploaded_file.name)