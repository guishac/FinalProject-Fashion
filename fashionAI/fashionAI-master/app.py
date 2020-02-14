from flask import Flask, render_template, request, redirect, url_for, flash ,Response, jsonify
from flask_bootstrap import Bootstrap
import boto3
from config import S3_BUCKET,S3_KEY,S3_SECRET
from filters import datetimeformat, file_type
from scraper import scrape_info
import json
# import ast
from ai_model import predict

app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'secret'
app.jinja_env.filters['datetimeformat'] = datetimeformat
app.jinja_env.filters['file_type'] = file_type

s3 = boto3.resource(
   "s3",
   aws_access_key_id=S3_KEY,
   aws_secret_access_key=S3_SECRET
)

#list all the buckets currently available
for bucket in s3.buckets.all():
    print(bucket.name)

# print(predict('https://mushroommushroomboomboom.s3.us-east-2.amazonaws.com/shirt.jfif'))

file_content = list()

@app.route('/')
def index():

    card_display = []
    for f in file_content:
        card_display.append(f)

    s3_resource = boto3.resource('s3')
    # my_bucket = s3_resource.Bucket(S3_BUCKET)
    my_bucket = s3_resource.Bucket('mushroommushroomboomboom')
    summaries = my_bucket.objects.all()

    
    return render_template("index.html", my_bucket=my_bucket, files=summaries, sdata = card_display)
    # return 'Hello There'

    


@app.route('/files')
def files():
    s3_resource = boto3.resource('s3')
    # my_bucket = s3_resource.Bucket(S3_BUCKET)
    my_bucket = s3_resource.Bucket('mushroommushroomboomboom')
    summaries = my_bucket.objects.all()

    return render_template('files.html', my_bucket=my_bucket, files=summaries)


@app.route("/jsonData")
def jsonData():
    s3 = boto3.resource('s3')
    content_object = s3.Object('mushroommushroomboomboom', 'data.json')
    file_content = content_object.get()['Body'].read().decode('utf-8')
    json_content = json.loads(file_content)
    # print(json_content)
    return jsonify(json_content)



@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']

    s3_resource = boto3.resource('s3')
    # my_bucket = s3_resource.Bucket(S3_BUCKET)
    my_bucket = s3_resource.Bucket('mushroommushroomboomboom')
    my_bucket.Object(file.filename).put(Body=file)

    #run the AI model
    pipi = predict('https://mushroommushroomboomboom.s3.us-east-2.amazonaws.com/'+file.filename)

    #Carry out the scrape
    scrape_pi = scrape_info(pipi['Predicted'][0])

    file_content.append(scrape_pi)

    #Save data to file
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(file_content, f, ensure_ascii=False, indent=4,sort_keys=True)
    
    #Save to AWS S3
    s3.Object('mushroommushroomboomboom', 'data.json').put(Body=open('data.json', 'rb'))

    for i in range(len(file_content)):
        print(file_content[i]['Item_Name'])
 
    flash('File uploaded successfully')
    return redirect(url_for('index'))





@app.route('/delete', methods=['POST'])
def delete():
    key = request.form['key']

    s3_resource = boto3.resource('s3')
    # my_bucket = s3_resource.Bucket(S3_BUCKET)
    my_bucket = s3_resource.Bucket('mushroommushroomboomboom')
    my_bucket.Object(key).delete()

    flash('File deleted successfully')
    return redirect(url_for('files'))


@app.route('/download', methods=['POST'])
def download():
    key = request.form['key']

    s3_resource = boto3.resource('s3')
    # my_bucket = s3_resource.Bucket(S3_BUCKET)
    my_bucket = s3_resource.Bucket('mushroommushroomboomboom')

    file_obj = my_bucket.Object(key).get()

    return Response(
        file_obj['Body'].read(),
        mimetype='text/plain',
        headers={"Content-Disposition": "attachment;filename={}".format(key)}
    )

if __name__ == "__main__":
    app.run()