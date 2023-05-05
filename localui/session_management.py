from flask import Flask, request, make_response

app = Flask(__name__)
app.secret_key = 'my_secret_key' # Set a secret key for the app

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    # Authenticate user and set a session cookie
    if authenticate(username, password):
        response = make_response('Logged in successfully!')
        response.set_cookie('username', username)
        return response
    
    # Return an error message if authentication fails
    else:
        return 'Invalid username or password'
    
@app.route('/profile')
def profile():
    # Check if the user is logged in by verifying the session cookie
    if 'username' in request.cookies:
        username = request.cookies['username']
        return f'Welcome, {username}!'
    
    # Redirect to login page if the user is not logged in
    else:
        return redirect('/login')

if __name__ == '__main__':
    app.run()
