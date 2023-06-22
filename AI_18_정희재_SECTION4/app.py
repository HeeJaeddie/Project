from flask import Flask, request, render_template, send_from_directory
import os
from keras.models import Model, load_model
from keras.preprocessing import image
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

app = Flask(__name__)
app.config["IMAGE_UPLOADS"] = "/Users/DE/project4/CATEGORY_PIC"
app.config["IMAGE_UPLOAD_NAME"] = 'input.jpg'

# Load the pre-trained model
model = load_model('my_model.h5')
# Create a new model that outputs the feature vectors
feature_model = Model(inputs=model.input, outputs=model.get_layer('flatten_1').output)


base_dir = '/Users/DE/project4/CATEGORY_PIC' 
all_img_paths = []

# os.walk를 사용하여 base_dir부터 시작하는 모든 파일 경로를 가져옵니다.
for subdir, dirs, files in os.walk(base_dir):
    for filename in files:
        filepath = subdir + os.sep + filename

        # 파일 확장자를 확인하여 이미지 파일만 추가합니다. 
        # 여기서는 jpg와 png 파일만 사용합니다. 필요에 따라 추가/삭제하세요.
        if filepath.endswith(".jpg") or filepath.endswith(".png"):
            all_img_paths.append(filepath)


# 데이터셋에 있는 모든 이미지의 특징 벡터를 추출합니다.
feature_vectors = {}
for img_path in all_img_paths:  # all_img_paths는 데이터셋에 있는 모든 이미지의 경로 리스트입니다.
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    features = feature_model.predict(x)
    feature_vectors[img_path] = features[0]

# Define the function to search for similar images
def search_similar_images(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    features = feature_model.predict(x)
    similarities = {}
    for path, feature_vector in feature_vectors.items():
        sim = cosine_similarity(features, np.array([feature_vector]))[0][0]
        similarities[path] = sim
    sorted_similarities = sorted(similarities.items(), key=lambda x: x[1], reverse=True)
    similar_images = [os.path.relpath(item[0], start=base_dir) for item in sorted_similarities[:6]]
    return similar_images

@app.route('/upload-image', methods=['GET', 'POST'])
def upload_image():
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            image.save(os.path.join(app.config["IMAGE_UPLOADS"], app.config["IMAGE_UPLOAD_NAME"]))
            return render_template("upload_image.html", uploaded_image=app.config["IMAGE_UPLOAD_NAME"])
    return render_template("upload_image.html") 

@app.route('/uploads/<path:filename>')
def send_uploaded_file(filename=''):
    return send_from_directory(app.config["IMAGE_UPLOADS"], filename)

@app.route('/predict-image', methods=['POST'])
def predict_images():
    img_path = os.path.join(app.config["IMAGE_UPLOADS"], app.config["IMAGE_UPLOAD_NAME"])
    similar_img_paths = search_similar_images(img_path)
    return render_template('result.html', similar_images=similar_img_paths)

if __name__ == '__main__':
    app.run(debug=False)