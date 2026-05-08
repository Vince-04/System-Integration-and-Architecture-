
1. Project Title & Description
** GitHub OAuth & API Security Lab **
- A Flask-based implementation demonstrating the OAuth 2.0 Authorization Code Flow using GitHub as the Identity Provider (IdP).

2. Prerequisites

- Python 3.14
- A GitHub account

3. Installation & Setup

- Clone the repo: git clone <your-repo-link>
- Install dependencies: pip install -r requirements.txt

Note: Mention that the SECRET_KEY is required for Flask sessions.

4. How to Run

- Bash python app.py
- visit http://localhost:5000 in your browser.

5. API Documentation (The Routes)

- GET /: The landing page.
- GET /login: Redirects the user to GitHub for authorization.
- GET /callback: Handles the response from GitHub and swaps the code for a token.
- GET /profile: [Protected] Displays JSON user data if a session exists.
- GET /logout: Clears the session.