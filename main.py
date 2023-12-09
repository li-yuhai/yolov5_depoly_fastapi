from fastapi import FastAPI, UploadFile,File

from pathlib import Path
import det_api
import json
import os
import uvicorn
from tool import generate_unique_id

app = FastAPI()

# ======= 静态资源写法
from fastapi.staticfiles import StaticFiles
app.mount("/static/det_img", StaticFiles(directory="det_img"), name="det_img")  # 目标检测的检测图
app.mount("/static/det_origin_img", StaticFiles(directory="det_origin_img"), name="det_origin_img") # 目标检测的原图
app.mount("/static/det_json", StaticFiles(directory="det_json"), name="det_json") # 目标检测后的json文件

@app.post("/detect/")
async def create_upload_file(file:UploadFile = File(...)):
    # try:
    #     os.mkdir('./images')
    #     os.remove("./images/test.jpg")
    #     os.remove("det_json/test.jpg.json")
    # except:
    #     pass

    id = generate_unique_id()  # 获取唯一id数值，图片明
    img_name_path ='det_origin_img/' +  id + '.jpg' # 保存的图像路径

    contents = await file.read()
    with open(img_name_path, 'wb') as f:
        f.write(contents)

    yolo = det_api
    yolo.run(source=img_name_path, project='det_img', name='')  # 设置参数，进行检测，调用detect.py的run函数
    det_img_path = 'det_img/' + id + '.jpg'
    result = []

    json_file_path = 'det_json/' + id + '.json'

    if Path(json_file_path).exists():
        with open(json_file_path, 'r') as rf:
            # data = json.load(rf)
            j_list = rf.readlines()
            for i in j_list:
                result.append(json.loads(i))

    # if Path('det_json/test.jpg.json').exists():
    #     with open('det_json/test.jpg.json','r') as rf:
    #         # data = json.load(rf)
    #         j_list = rf.readlines()
    #         for i in j_list:
    #             result.append(json.loads(i))

    # 在det_json中创建json文件，并写如数据, 在yolo.run()中，会在det_json创建文件
    # 指定 JSON 文件路径
    # json_file_path = 'det_json/'+ id + '.json'
    # # 写入数据到 JSON 文件
    # with open(json_file_path, "w") as json_file:
    #     j_list = json_file.readlines()
    #     for i in j_list:
    #         result.append(json.loads(i))


    return {'filename':file.filename,
            'result':result,
            'det_img_path': det_img_path,
            'det_origin_img': img_name_path,
            'det_json': json_file_path}
    # return {'filename':file.filename,'result':result, }


if __name__ == '__main__':
    uvicorn.run(app =app, host = '0.0.0.0', port=8000)

