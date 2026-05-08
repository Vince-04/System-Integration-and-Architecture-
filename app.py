import os
from flask import render_template_string
from flask import Flask, redirect, url_for, session, jsonify
from authlib.integrations.flask_client import OAuth

# SECURITY FIX: Allow OAuth over HTTP (localhost) instead of requiring HTTPS
os.environ['AUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
app.secret_key = "abellano_secret_key_123"

# SESSION FIX: Ensure cookies work properly on localhost
app.config.update(
    SESSION_COOKIE_NAME='github_auth_session',
    SESSION_COOKIE_SAMESITE='Lax',
    SESSION_COOKIE_SECURE=False
)

oauth = OAuth(app)

# ii. Configure GitHub OAuth
github = oauth.register(
    name='github',
    client_id='Ov23liJoT6pIO6PI8qeD',
    client_secret='5b90a6ec1d7978b2e631d57a8d8de855ec3f2d1f',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)

@app.route('/')
def index():
    if 'user' in session:
        return f'Hello, {session["user"]["login"]}! <a href="/profile">View Profile</a> | <a href="/logout">Logout</a>'
    return 'Welcome! <a href="/login">Login with GitHub</a>'

# iii. Create Login Route
@app.route('/login')
def login():
    # Force the redirect_uri to match your GitHub settings exactly
    redirect_uri = "http://localhost:5000/callback"
    return github.authorize_redirect(redirect_uri)

# iv. Create Callback Route
@app.route('/callback')
def callback():
    try:
        token = github.authorize_access_token()
        resp = github.get('user')
        user = resp.json()
        
        session['user'] = user
        return redirect('/profile')
    except Exception as e:
        return f"Error during login: {str(e)}"

# v. Create Protected API
@app.route('/profile')
def profile():
    if 'user' not in session:
        return "Unauthorized: Please login first.", 401
    
    user_data = session['user']
    
    # HTML template with a link to the real GitHub profile
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>User Profile</title>
        <style>
            body { font-family: 'Segoe UI', sans-serif; background-color: #f4f4f9; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .card { background: white; padding: 2.5rem; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); text-align: center; width: 320px; }
            img { width: 120px; border-radius: 50%; border: 4px solid #2dba4e; margin-bottom: 15px; }
            h2 { margin: 0; color: #333; }
            p { color: #666; font-size: 14px; line-height: 1.5; }
            .links { display: flex; flex-direction: column; gap: 10px; margin-top: 20px; }
            .btn-github { text-decoration: none; background: #24292e; color: white; padding: 10px; border-radius: 6px; font-weight: bold; }
            .btn-logout { text-decoration: none; background: #f6f8fa; color: #d73a49; padding: 10px; border-radius: 6px; font-size: 13px; border: 1px solid #d73a49; }
            .btn-github:hover { background: #000; }
        </style>
    </head>
    <body>
        <div class="card">
            <img src="{{ data.avatar_url }}" alt="Avatar">
            <h2>{{ data.name or data.login }}</h2>
            <p>@{{ data.login }}</p>
            <p>{{ data.bio or 'This user has no bio.' }}</p>
            
            <div class="links">
                <a href="{{ data.html_url }}" target="_blank" class="btn-github">View GitHub Profile</a>
                <a href="/logout" class="btn-logout">Logout</a>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_template, data=user_data)

# vi. Logout Route
# vi. Logout Route
@app.route('/logout')
def logout():
    # Clear the user session
    session.pop('user', None)
    
    # Return a custom "Thanks" page
    html_thanks = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Logged Out</title>
        <style>
            body { font-family: 'Segoe UI', sans-serif; background-color: #f4f4f9; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .container { background: white; padding: 3rem; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); text-align: center; }
            h1 { color: #333; margin-bottom: 1rem; }
            p { color: #666; margin-bottom: 2rem; }
            .btn-home { text-decoration: none; background: #007bff; color: white; padding: 12px 24px; border-radius: 6px; font-weight: bold; }
            .btn-home:hover { background: #0056b3; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Thanks for using the App!</h1>
            <p>You have been successfully logged out of the System Integration Lab.</p>
            <a href="/" class="btn-home">Return to Home</a>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_thanks)

# vii. BONUS CHALLENGE: Secure Data API
@app.route('/api/secure-data')
def secure_data():
    if 'user' not in session:
        return jsonify({"error": "Access Denied"}), 403
    
    return jsonify({
        "status": "Success",
        "message": f"Hello {session['user']['login']}, access granted to secure data.",
        "lab_code": "SYS-INT-ARCH-2026"
    })

if __name__ == '__main__':
    # Ensure you access the app via http://localhost:5000
    app.run(host='localhost', port=5000, debug=True)