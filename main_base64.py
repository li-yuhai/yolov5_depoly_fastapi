import base64
from io import BytesIO
from PIL import Image
from fastapi import FastAPI, UploadFile,File
import det_api_base64
import uvicorn
from tool import generate_unique_id
from fastapi import Request

app = FastAPI()

# ======= 静态资源写法
from fastapi.staticfiles import StaticFiles
app.mount("/static/det_img", StaticFiles(directory="det_img"), name="det_img")  # 目标检测的检测图
app.mount("/static/det_origin_img", StaticFiles(directory="det_origin_img"), name="det_origin_img") # 目标检测的原图
app.mount("/static/det_json", StaticFiles(directory="det_json"), name="det_json") # 目标检测后的json文件

'''
    {
      "data": [
        "<base64-encoded-image-data-1>",
        "<base64-encoded-image-data-2>",
        "<base64-encoded-image-data-3>",
        ...
      ]
    }
    返回的图片是base64编码
'''
@app.post('/predict/')
async def predict( request: Request ):
    # 从请求中检索出Base64编码的图像数据
    json_data = await request.json()
    data = json_data['data']
    # 初始化一个空数组以存储每个图像的预测结果
    predictions = []
    for item in data:
        img_name = item['name']
        image_data = item['img']
        # 将base64编码进行解码，然后保存在本地,det_img文件夹下面, 保存在jpg_path路径
        jpg_path = 'det_origin_img_base64/' + generate_unique_id() + '.jpg'
        decoded_data = base64.b64decode(image_data)
        image = Image.open(BytesIO(decoded_data))
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        image.save(jpg_path)

        # 调用det_api_base64文件方法来进行检测，返回det信息和检测后图像的base64编码
        yolo = det_api_base64
        image_pred, image_pred_base64 = yolo.run(source=jpg_path, project='det_img_base64',name='')  # 设置参数，进行检测
        predictions.append({'imgname': img_name, 'pred_info': image_pred, 'image': image_pred_base64})
    return predictions


# 上传一张图像进行操作
@app.post("/detect/")
async def create_upload_file(file:UploadFile = File(...)):
    file_name = file.filename
    id = generate_unique_id()  # 获取唯一id数值，图片明
    img_name_path ='det_origin_img/' +  id + '.jpg' # 保存的图像路径
    contents = await file.read()
    with open(img_name_path, 'wb') as f:
        f.write(contents)
    yolo = det_api_base64
    image_pred, image_pred_base64 =  yolo.run(source=img_name_path, project='det_img', name='')  # 设置参数，进行检测，调用detect.py的run函数
    return {'imgname': file_name, 'pred_info': image_pred, 'image': image_pred_base64}


if __name__ == '__main__':
    uvicorn.run(app =app, host = '0.0.0.0', port=8000)

