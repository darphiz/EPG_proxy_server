from flask import Flask

app = Flask(__name__)

"""
    This server mocks the xml file that is to be downloaded from the source url.
"""

@app.route("/downloadable/small")
def downloadable():
    
    data = None
    with open('mock.xml', 'r') as f:
        data =  f.read()    
    return data, 200, {
        'Content-Type': 'application/xml; charset=utf-8',
        'Content-Disposition': 'attachment; filename=small.xml'
        }
    

@app.route("/small/not-downloadable")
def not_downloadable():
    data = None
    with open('mock.xml', 'r') as f:
        data =  f.read()
    return data, 200, {
        'Content-Type': 'application/xml; charset=utf-8',
    }

@app.route("/downloadable/large")
def downloadable_large():
    data = None
    with open('mock_2.xml', 'r') as f:
        data =  f.read()    
    return data, 200, {
        'Content-Type': 'application/xml; charset=utf-8',
        'Content-Disposition': 'attachment; filename=small.xml'
        }
    
@app.route("/notdownloadable/large")
def not_downloadable_large():
    data = None
    with open('mock_2.xml', 'r') as f:
        data =  f.read()    
    return data, 200, {
        'Content-Type': 'application/xml; charset=utf-8',
        'Content-Disposition': 'attachment; filename=small.xml'
        }



if __name__ == "__main__":
    app.run(port=8080, debug=True)