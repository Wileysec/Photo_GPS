import exifread
import re
import json
import requests
import sys

def latitude_and_longitude_convert_to_decimal_system(*arg):
    return float(arg[0]) + ((float(arg[1]) + (float(arg[2].split('/')[0]) / float(arg[2].split('/')[-1]) / 60)) / 60)

def find_GPS_image(pic_path):
    GPS = {}
    date = ''
    with open(pic_path, 'rb') as f:
        tags = exifread.process_file(f)
        for tag, value in tags.items():
            if re.match('GPS GPSLatitudeRef', tag):
                GPS['GPSLatitudeRef'] = str(value)
            elif re.match('GPS GPSLongitudeRef', tag):
                GPS['GPSLongitudeRef'] = str(value)
            elif re.match('GPS GPSAltitudeRef', tag):
                GPS['GPSAltitudeRef'] = str(value)
            elif re.match('GPS GPSLatitude', tag):
                try:
                    match_result = re.match('\[(\w*),(\w*),(\w.*)/(\w.*)\]', str(value)).groups()
                    print(match_result)
                    GPS['GPSLatitude'] = int(match_result[0]), int(match_result[1]), int(match_result[2])
                except:
                    deg, min, sec = [x.replace(' ', '') for x in str(value)[1:-1].split(',')]
                    GPS['GPSLatitude'] = latitude_and_longitude_convert_to_decimal_system(deg, min, sec)
            elif re.match('GPS GPSLongitude', tag):
                try:
                    match_result = re.match('\[(\w*),(\w*),(\w.*)/(\w.*)\]', str(value)).groups()
                    GPS['GPSLongitude'] = int(match_result[0]), int(match_result[1]), int(match_result[2])
                except:
                    deg, min, sec = [x.replace(' ', '') for x in str(value)[1:-1].split(',')]
                    GPS['GPSLongitude'] = latitude_and_longitude_convert_to_decimal_system(deg, min, sec)
            elif re.match('GPS GPSAltitude', tag):
                GPS['GPSAltitude'] = str(value)
            elif re.match('.*Date.*', tag):
                date = str(value)
    return {'GPS_information': GPS, 'date_information': date}

def ImageInfo():
    try:
        information = {}
        with open(pic_path, 'rb') as f:
            tags = exifread.process_file(f)

        information['Image Make'] = tags['Image Make']
        information['Image Model'] = tags['Image Model']
        information['Image DateTime'] = tags['Image DateTime']

        return information
    except:
        pass

def find_address_from_GPS(GPS):
    if not GPS['GPS_information']:
        return '该照片无GPS信息'
    else:
        lat, lng = GPS['GPS_information']['GPSLatitude'], GPS['GPS_information']['GPSLongitude']
        access = "http://map.yanue.net/gpsapi.php?lat={0}&lng={1}".format(lat, lng)
        accres = requests.get(access)
        accres = accres.text
        accres = json.loads(accres)
        if accres['error'] == 0:
            api = "http://api.map.baidu.com/reverse_geocoding/v3/?ak=你的百度地图AK密钥&output=json&coordtype=wgs84ll&location={0},{1}".format(accres['baidu']['lat'],accres['baidu']['lng'])
            response = requests.get(api)
            content = response.text
            address = json.loads(content)
        else:
            api = "http://api.map.baidu.com/reverse_geocoding/v3/?ak=你的百度地图AK密钥&output=json&coordtype=wgs84ll&location={0},{1}".format(lat, lng)
            response = requests.get(api)
            content = response.text
            address = json.loads(content)

        if address['status'] == 0:
            add = address['result']['formatted_address']
            business = address['result']['business']
            country = address['result']['addressComponent']['country']

            text = country + add + business + " 经度(lng):" + str(lng) + " 纬度(lat):" + str(lat)

            return text

        else:
            return "地址查询失败 经度(lng):" + str(lng) + " 纬度(lat):" + str(lat)

def main(pic_path):
    pic_path = sys.argv[1]
    GPS_info = find_GPS_image(pic_path)
    address = find_address_from_GPS(GPS=GPS_info)
    information = ImageInfo()

    try:
        info = "手机厂商：" + str(information['Image Make']) + " 手机型号：" + str(information['Image Model']) + " 拍摄时间：" + str(
            information['Image DateTime']) + " " + address
        print(info)
    except:
        pass

if __name__ == "__main__":
    pic_path = sys.argv[1]
    main(pic_path)