import json
import openai
import boto3

def lambda_handler(event, context):
    
    model_to_use = "gpt-3.5-turbo"
    input_prompt="Write an email to Elon Musk asking him why he bought Twitter for such a huge amount"
    
    openai.api_key = get_api_key()
    response = openai.Completion.create(
      model=model_to_use,
      prompt=input_prompt,
      temperature=0,
      max_tokens=100,
      top_p=1,
      frequency_penalty=0.0,
      presence_penalty=0.0
    )
    #print(response)
    text_response = response['choices'][0]['text'].strip()
    
    return {
        'statusCode':200,
        'body': {
            'response' : text_response
        }
    }
    
def get_api_key():
    lambda_client = boto3.client('lambda')
    response = lambda_client.invoke(
            FunctionName = 'arn:aws:lambda:us-east-2:481478219070:function:openai_get_api_key',
            InvocationType = 'RequestResponse'
        )

    openai_api_key = json.load(response['Payload'])['body']['api_key']
    return openai_api_key
