from flask import Flask, render_template, Response
import cam
import os
import cv2

app = Flask(__name__, template_folder='templates')

overlay_image = []
header_img = "Images"

# Check if 'Images' folder exists
if not os.path.exists(header_img):
    print(f"[ERROR] Folder '{header_img}' not found!")
else:
    header_img_list = os.listdir(header_img)
    for i in header_img_list:
        image_path = os.path.join(header_img, i)
        image = cv2.imread(image_path)
        if image is not None:
            overlay_image.append(image)
            print(f"[INFO] Loaded image: {image_path}")
        else:
            print(f"[WARNING] Could not read image: {image_path}")

@app.route('/')
def index():
    return render_template('index.html')

def gen():
    cam1 = cam.VideoCamera(overlay_image=overlay_image)

    while True:
        frame = cam1.get_frame(overlay_image=overlay_image)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # Turn on debug during development
    app.run(host='0.0.0.0', port=5000, debug=True)
