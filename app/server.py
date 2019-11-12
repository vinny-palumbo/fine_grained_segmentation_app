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

    # get image bytes from form
    img_data = await request.form()
    img_bytes = await (img_data['file'].read())
    
    # save image as input.png
    with open('input.png', 'wb') as input:
        input.write(img_bytes)
    
    # run segmentation and save as result.png
    subprocess.call(['fashion-segmentator', '--image', 'input.png'])
    
    return JSONResponse({'status': 'Done!'})


if __name__ == '__main__':
    if 'serve' in sys.argv:
        uvicorn.run(app=app, host='127.0.0.1', port=5000, log_level="info")
