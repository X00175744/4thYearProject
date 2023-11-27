from flask import Flask, render_template, request, jsonify
import json
import boto3

app = Flask(__name__)

awsAccessKey = 'AKIARHS7T7WLGENB5V4B' #this can be done with Cognito later, to hide my secrets
awsSecretAccessKey = '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'
awsRegion = 'eu-west-1'
lambdaFunctionName = 'TranslateFun'

lambdaClient = boto3.client('lambda',
                            aws_access_key_id = awsAccessKey,
                            aws_secret_access_key = awsSecretAccessKey,
                            region_name=awsRegion)

# lambdaClient = boto3.client('lambda', region_name='your_region')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST', 'GET'])
#when the translate button is pressed, call the lambda function
def translate():
    input_text = request.form['text']
    print("input found")
    print(input_text)

    try:#exception handling
            print("hi2")
            response = lambdaClient.invoke(
                FunctionName=lambdaFunctionName, #the lambda function to be called
                InvocationType='RequestResponse',
                Payload=f'{{"text": "{input_text}"}}'.encode('utf-8')
                #the payload is the json response.
                #f is an f-string, which lets us format it like json
            )
            print("input found2")

            print("hi3")
            # Thr response needs to be decoded from the utf it was travelling in
            result = response['Payload'].read().decode('utf-8')
            print("hi4")
            jsonResult = json.loads(result)
            print(jsonResult)
            translated_text = jsonResult.get("body", "No Translation")

            # translated_text = result

            return render_template('index.html', input_text=input_text, translated_text=translated_text)

    except Exception as e:
            # Handle exceptions
            return render_template('index.html', input_text=input_text, error_message=str(e))

   
if __name__ == '__main__':
    app.run(debug=True)
