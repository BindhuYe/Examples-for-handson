from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import boto3
from werkzeug.utils import secure_filename
import os
import base64

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database Configuration
app.config['MYSQL_HOST'] = 'RDS END POINT'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Admin-1234'
app.config['MYSQL_DB'] = 'ccituserdb'

# AWS S3 Configuration
S3_BUCKET = 'YOUR-S3-BUCKET'
S3_REGION = 'YOUR-REGION'
S3_ACCESS_KEY = 'YOUR-ACCESS-KEY'
S3_SECRET_KEY = 'YOUR-Sec-KEY'

# AWS KMS Configuration
KMS_KEY_ID = 'YOUR-KMS-KEYID'
kms_client = boto3.client(
    'kms',
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY,
    region_name=S3_REGION
)

# Initialize MySQL
mysql = MySQL(app)

# File upload configuration
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Helper Functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def encrypt_password(password):
    """Encrypts the password using AWS KMS."""
    response = kms_client.encrypt(
        KeyId=KMS_KEY_ID,
        Plaintext=password
    )
    return base64.b64encode(response['CiphertextBlob']).decode('utf-8')

def decrypt_password(encrypted_password):
    """Decrypts the password using AWS KMS."""
    encrypted_blob = base64.b64decode(encrypted_password)
    response = kms_client.decrypt(
        CiphertextBlob=encrypted_blob
    )
    return response['Plaintext'].decode('utf-8')

def upload_to_s3(file, bucket_name, object_name):
    """Uploads a file to S3 and returns the URL."""
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=S3_ACCESS_KEY,
            aws_secret_access_key=S3_SECRET_KEY,
            region_name=S3_REGION
        )
        s3_client.upload_fileobj(file, bucket_name, object_name)
        s3_url = f"https://{bucket_name}.s3.{S3_REGION}.amazonaws.com/{object_name}"
        return s3_url
    except Exception as e:
        flash(f"Failed to upload image: {e}")
        return None

@app.route('/')
def home():
    return redirect(url_for('signin'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        image_file = request.files['image_file']

        # Validate and upload the image file
        if image_file and allowed_file(image_file.filename):
            object_name = f"uploads/{image_file.filename}"
            image_url = upload_to_s3(image_file, S3_BUCKET, object_name)
            if not image_url:
                flash('Failed to upload image. Please try again.')
                return redirect(request.url)
        else:
            flash('Invalid image file selected.')
            return redirect(request.url)

        # Encrypt the password
        encrypted_password = encrypt_password(password)

        cursor = mysql.connection.cursor()
        cursor.execute(
            'INSERT INTO users (name, email, password, image_url) VALUES (%s, %s, %s, %s)',
            (name, email, encrypted_password, image_url)
        )
        mysql.connection.commit()
        cursor.close()

        flash('You have successfully registered!')
        return redirect(url_for('signin'))
    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        account = cursor.fetchone()

        if account:
            decrypted_password = decrypt_password(account['password'])
            if password == decrypted_password:
                session['loggedin'] = True
                session['id'] = account['Id']
                session['name'] = account['name']
                session['email'] = account['email']
                session['image_url'] = account['image_url']
                return redirect(url_for('welcome'))
        flash('Incorrect username or password')
    return render_template('signin.html')

@app.route('/welcome')
def welcome():
    if 'loggedin' in session:
        return render_template('welcome.html', name=session['name'], email=session['email'], image_url=session['image_url'])
    return redirect(url_for('signin'))

if __name__ == '__main__':
    app.run(debug=True)
