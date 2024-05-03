import random
import string
import json
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
import uvicorn

app = FastAPI()

class LinkShortener:
    def __init__(self):
        self.url_mapping = {}
        self.load_from_file()

    def load_from_file(self):
        try:
            with open('urls.json', 'r') as file:
                data = file.read()
                if data:
                    self.url_mapping = json.loads(data)
                else:
                    self.url_mapping = {}
        except FileNotFoundError:
            self.url_mapping = {}

    def save_to_file(self):
        with open('urls.json', 'w') as file:
            json.dump(self.url_mapping, file)

    def shorten_url(self, original_url: str, host_url: str):
        short_key = self.generate_unique_id()
        self.url_mapping[short_key] = {'original_url': original_url, 'shortened_url': f"{host_url}{short_key}"}
        self.save_to_file()
        return short_key

    def expand_url(self, short_key: str):
        return self.url_mapping.get(short_key, {}).get('original_url', None)

    def generate_unique_id(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

shortener = LinkShortener()

# CSS styles for the home route
home_css = '''
    body {
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 0;
        background-color: #f0f0f0;
    }
    .container {
        width: 80%;
        margin: 0 auto;
        padding: 20px;
        background-color: #fff;
        border-radius: 8px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        margin-top: 50px;
    }
    h1, h2 {
        text-align: center;
        margin-bottom: 20px;
    }
    p {
        text-align: center;
        margin-top: 10px;
    }
    a {
        color: #4CAF50;
    }
'''

# CSS styles for the shorten route (GET request)
shorten_get_css = '''
    form {
        text-align: center;
    }
    input[type="text"] {
        width: 70%;
        padding: 10px;
        font-size: 16px;
        border-radius: 4px;
        border: 1px solid #ccc;
        margin-bottom: 10px;
    }
    input[type="submit"] {
        background-color: #4CAF50;
        color: white;
        padding: 14px 20px;
        margin: 8px 0;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 16px;
    }
    input[type="submit"]:hover {
        background-color: #45a049;
    }
'''

# CSS styles for the shorten route (POST request)
shorten_post_css = '''
    p {
        text-align: center;
        margin-top: 10px;
    }
'''

# CSS styles for the expand route
expand_css = '''
    body {
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 0;
        background-color: #f0f0f0;
    }
    .container {
        width: 80%;
        margin: 0 auto;
        padding: 20px;
        background-color: #fff;
        border-radius: 8px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        margin-top: 50px;
        text-align: center;
    }
'''

@app.get("/api/health-check")
def health_check():
    return {"status": "ok"}

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>URL Shortener</title>
        <style>{home_css}</style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to the URL Shortener!</h1>
            <p><a href="/shorten">Click here to Shorten a URL</a></p>
        </div>
    </body>
    </html>
    """

@app.get("/shorten", response_class=HTMLResponse)
def get_shorten(request: Request):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>URL Shortener</title>
        <style>{home_css} {shorten_get_css}</style>
    </head>
    <body>
        <div class="container">
            <h2>Shorten a URL</h2>
            <form method="post">
                <input type="text" id="url" name="url" placeholder="Enter your URL to shorten...">
                <input type="submit" value="Shorten">
            </form>
        </div>
    </body>
    </html>
    """

@app.post("/shorten", response_class=HTMLResponse)
def post_shorten(request: Request, url: str = Form(...)):
    original_url = url
    host_url = str(request.url)
    for short_key, value in shortener.url_mapping.items():
        if value['original_url'] == original_url:
            return f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>URL Shortener</title>
                <style>{home_css}</style>
            </head>
            <body>
                <div class="container">
                    <h2>Shortened URL:</h2>
                    <p>{request.url.scheme}://{request.url.netloc}/{short_key}</p>
                    <p><a href="/{short_key}">Click here to open the shortened URL</a></p>
                    <p><a href="/shorten">Click here to shorten another URL</a></p>
                </div>
            </body>
            </html>
            """
    short_key = shortener.shorten_url(original_url, host_url)
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>URL Shortener</title>
        <style>{home_css}</style>
    </head>
    <body>
        <div class="container">
            <h2>Shortened URL:</h2>
            <p>{request.url.scheme}://{request.url.netloc}/{short_key}</p>
            <p><a href="/{short_key}">Click here to open the shortened URL</a></p>
            <p><a href="/shorten">Click here to shorten another URL</a></p>
        </div>
    </body>
    </html>
    """

@app.get("/api/{short_key}", response_class=RedirectResponse)
def expand(short_key: str):
    original_url = shortener.expand_url(short_key)
    if original_url:
        return RedirectResponse(url=original_url)
    else:
        raise HTTPException(status_code=404, detail="Shortened URL not found.")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")


