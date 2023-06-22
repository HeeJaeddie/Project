import os, pymongo
from pymongo import MongoClient

# MongoDB 연결 설정
URI = "mongodb+srv://jhjheejae:wonsoju23@cluster4.gbabl9b.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(URI)

DATABASE = 'mydb'
db = client[DATABASE]

COLLECTION = 'musinsa-collection'
collection = db[COLLECTION]

# 이미지 파일 경로 목록
image_folder = '/Users/DE/project4/CATEGORY_PIC'
image_paths = [os.path.join(image_folder, filename) for filename in os.listdir(image_folder)]

# 이미지 파일 경로를 MongoDB에 저장
for image_path in image_paths:
    document = {'image_path': image_path}
    collection.insert_one(document)

# 연결 종료
client.close()
