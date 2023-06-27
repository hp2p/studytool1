import json
import boto3
from time import gmtime, strftime
import openai

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('StudyTool1Database')
now = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

def lambda_handler(event, context):
    newWord = event['newWord']

    openai.api_key = get_api_key()
    prompt = f'''Create a short, elegant English sentence with '%s' and translate it into Korean''' % newWord
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[ {"role": "user", "content": prompt} ]
    )
    openai_answer = completion['choices'][0]['message']['content']
    
    ki = openai_answer.find('Korean: ')
    english = openai_answer[len('English: '): ki-1]
    korean = openai_answer[ki + len('Korean: '):]
    response = table.put_item(
        Item={
            'ID': newWord,
            'LatestGreetingTime':now,
            'english': english,
            'korean' : korean,
            })

    return {
        'statusCode': 200,
        'body': json.dumps({ 'english': english, 'korean': korean })
    }
    
    
def get_api_key():
    lambda_client = boto3.client('lambda')
    response = lambda_client.invoke(
            FunctionName = 'arn:aws:lambda:us-east-2:481478219070:function:openai_get_api_key',
            InvocationType = 'RequestResponse'
        )

    openai_api_key = json.load(response['Payload'])['body']['api_key']
    return openai_api_key    
