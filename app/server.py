import sys
from pathlib import Path
import uvicorn
import subprocess

from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles

path = Path(__file__).parent

app = Starlette()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['X-Requested-With', 'Content-Type'])
app.mount('/static', StaticFiles(directory='app/static'))


@app.route('/')
async def homepage(request):
    html_file = path / 'view' / 'index.html'
    return HTMLResponse(html_file.open(encoding="utf-8").read())


@app.route('/analyze', methods=['POST'])
async def analyze(request):
    subprocess.call(['fashion-segmentator','--image', 'https://s2.thcdn.com/productimg/300/300/12226182-5974707987048405.jpg'])
    return JSONResponse({'result': 'test'})


if __name__ == '__main__':
    if 'serve' in sys.argv:
        uvicorn.run(app=app, host='127.0.0.1', port=5000, log_level="info")
