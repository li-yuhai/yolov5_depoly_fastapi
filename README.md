## <div align="center">Quick Start Examples</div>

<details open>
<summary>Install</summary>
Clone repo and install requirements.txt in a
[**Python>=3.7.0**](https://www.python.org/) environment, including
[**PyTorch>=1.7**](https://pytorch.org/get-started/locally/)

```bash
git clone https://github.com/luosaidage/yolov5_server.git  # clone
pip install fastapi
pip install uvicorn[standard]
pip install python-multipart   # install
```

</details>

<details open>
<summary>RunServer</summary>

```bash
uvicorn main:app --reload --host 0.0.0.0
# visit 127.0.0.1:8000/docs(try it out)
```

</details>

## Chaneg weights file
```bash
vi ./det_api.py
# find def(run)
# change weight default path in this def.
```

## option(change pip origin)
```bash
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```



## 操作

在文件夹根目录root下建立 4个文件夹，这四个文件是静态资源，分别是det_img(检测后的效果图)、det_origin_img(检测的原图)、det_json(检测后的结果存为json文件)、det_txt(检测后的txt文件)，文件命名使用的时间戳作为不重名的方式。上传图片检测后的返回json结果如下所示：
此外，我将模型加载设置为全局变量，不用每次检测都要加载模型。
好用的工具：https://curlconverter.com/
```json
{
  "filename": "girl.png",
  "result": [
    {
      "img_shape": [ 406, 549,3],
      "label": "sports ball ",
      "position": [ 341, 262.5],
      "rect_size": [36,35],
      "conf": "0.47"
    },
    {
      "img_shape": [ 406,549,3],
      "label": "person ",
      "position": [212,203.5],
      "rect_size": [234,389],
      "conf": "0.60"
    }
  ],
  "det_img_path": "det_img/20231204092154184.jpg",
  "det_origin_img": "det_origin_img/20231204092154184.jpg",
  "det_json": "det_json/20231204092154184.json"
}
```



## 感谢原作者

感谢原作者提供的代码，本代码是在此https://github.com/luosaidage/yolov5_server.git基础上进行修改的。作者提供的方式，可以自定义检测的置信度阈值，我之前使用的是如下操作，我不清楚如何调整置信度。

```python
 #加载你的pt文件
 model = YOLO('checkpoint/test.pt')
 #把图片存到一个路径
 img_bgr.save("before.jpg")
 img_path = "before.jpg"
 results = model(img_path)
```

## 遇到问题
1:我用的mac系统解决OMP: Error #15: Initializing libiomp5.dylib, but found libomp.dylib already initialized.
```python
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
```

2:解决export PYTORCH_ENABLE_MPS_FALLBACK=1，使用的cpu，把cpu变量写死或者命令行如下：
```bash
export PYTORCH_ENABLE_MPS_FALLBACK=1
```


