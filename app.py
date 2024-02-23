from flask import Flask, render_template, request, jsonify, request, redirect, url_for
from user_auth import SimpleLoginSystem
import json
import boto3

# app = Flask(__name__, static_url_path='/static')
app = Flask(__name__)
login_system = SimpleLoginSystem()

def get_secret():

    secret_name = "SecretKeys"
    region_name = "eu-west-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    
    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )
    secret_dict = json.loads(get_secret_value_response['SecretString'])
    return secret_dict

    # Decrypts secret using the associated KMS key.
    # secret = get_secret_value_response['SecretString']


secret_credentials = get_secret()
# awsAccessKey = 'AKIARHS7T7WLGENB5V4B' #this can be done with secrets manager later, to hide my secrets
# awsSecretAccessKey = '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'
awsRegion = 'eu-west-1'
lambdaFunctionName = 'TranslateFun'

# lambdaClient = boto3.client('lambda',
#                             aws_access_key_id = awsAccessKey,
#                             aws_secret_access_key = awsSecretAccessKey,
#                             region_name=awsRegion)

lambdaClient = boto3.client('lambda', 
                            aws_access_key_id=secret_credentials.get('access_key'),
                            aws_secret_access_key=secret_credentials.get('secret_access_key'),
                            region_name='eu-west-1')


# Loginclient = boto3.client('cognito-idp', region_name='eu-west-1')

# # Example: Sign up a new user
# response = Loginclient.sign_up(
#     ClientId='5q8ghnbpfv860cnd579eqtkf23',
#     Username='username',
#     Password='password',
#     UserAttributes=[
#         {'Name': 'email', 'Value': 'user@example.com'},
#     ]
# )

@app.route('/')
def index():
    return render_template('index.html')

# @app.route("/getSourceLanguage", methods=['POST','GET'])
#additional functions, like adding languages, can be achieved by adding them
#to the /translate method. All the relevant info, from input text to language choice
#will be posted when the translate button is pushed




@app.route('/translate', methods=['POST', 'GET'])
#when the translate button is pressed, call the lambda function
  
def translate():
    
    input_text = request.form['text']
    #grabs the text from the input box form

    # srcLanguage = request.form['sourceLanguages']
    sourceLanguage = request.form.get('sourceLanguages')
    print(sourceLanguage)

    destLanguage = request.form.get('destLanguages')

    print("destLanguage " + str(destLanguage))
    print("input found")
    print(input_text)

    try:#exception handling
            print("hi2")
            

            payload = {
                  "text":input_text,
                  "sourceLanguageCode":sourceLanguage,
                  "destLanguageCode":destLanguage
            }

            response = lambdaClient.invoke(
                FunctionName=lambdaFunctionName, #the lambda function to be called
                InvocationType='RequestResponse',
                Payload=json.dumps(payload).encode('utf-8')
                            #the payload is the json response.
                #f is an f-string, which lets us format it like json
                #f string replaced with json.dumps to format the payload into json
                #this lets us configure the payload with languages as well as text
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
    
    
    
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if login_system.login(username, password):
        # Redirect to a new page or perform additional actions on successful login
        return redirect(url_for('dashboard'))
    else:
        return render_template('index.html', error="Login failed.")


   
if __name__ == '__main__':
    app.run(debug=True)
