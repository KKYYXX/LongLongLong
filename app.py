from app import createApp
from flask import send_from_directory

app=createApp()

@app.route('/uploads/<path:filename>')
def serve_uploaded_file(filename):
    return send_from_directory('uploads', filename)

if __name__ == '__main__':

    app.run(debug=True)