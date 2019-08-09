# Photo_GPS
利用Python脚本读取照片GPS信息，通过地图API查到拍摄者

需要安装 `exifread` `requests`

请通过 `pip3 install exifread,requests` 安装这两个模块

请在第 48 行修改下面代码：http://api.map.baidu.com/reverse_geocoding/v3/?ak=你的百度地图AK密钥&output=json&coordtype=wgs84ll&location={0},{1}

AK这个参数改为你在百度地图申请的AK密钥

运行 `python3 photo_gps.py 1.jpg`

配合这个辅助定位 简直完美 http://map.yanue.net/gps.html
