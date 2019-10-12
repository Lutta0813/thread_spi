import requests
import json
import os
import time
import progressbar

def proxySet():
    proxies = {
        'http': '000',
        'https': '000'
    }
    return proxies


def getPostId(typeChoose):   
    postIdContents = []
    print('爬蟲開始')
    
    if typeChoose == '0':
        url = 'xxx/xxx/xxx/xxx' # 熱門post的url
    elif typeChoose == '1':
        url = 'xxx/xxx/xxx/xxx' # 七天top 30
    elif typeChoose == '2':
        keyWord = str(input('Enter your key word to searching data: '))
        url = 'xxx/xxx/xxx/xxx' + keyWord # 關鍵字搜尋
        
    headers = {
        'user-agent': 'xxx',
        }

    result = requests.Session()
    r = result.get(url, headers=headers, allow_redirects=False)
    json_datas = json.loads(r.text)
    
    for d in json_datas:
#         print(d)
        postIdContents.append(d['post_id']) # 取得頁面上的post id
    
    if typeChoose == '2':
        while True:
            last_id = postIdContents[len(postIdContents) - 1]
            print(last_id)
            url = 'xxx/xxx/xxx/xxxsearchPosts?keyword=' + str(keyWord) + '&post_id=' + str(last_id)
            r = result.get(url, headers=headers, allow_redirects=False)
            json_datas = json.loads(r.text)
            if r.text == '[]': # 傳回空set
                break
            for d in json_datas:
                postIdContents.append(d['post_id'])
    
    
    return postIdContents


def getPostContent(postIds):
    
    pw_urls = []
    image_urls = []
    record = open('./darkka.txt', 'w', encoding='UTF-8')
    imgCount = 0
    pptCount = 0
    tkkttCount = 0
    videoCount = 0
    
    for pId in postIds: # 爬每個在list中的po文
        url = 'xxx/xxx/xxx/xxx' + str(pId)
        
        # cookie使用自己登入後的cookie，若無效要記得更新
        logined_headers = {
                'user-agent': 'xxx',
                'cookie': 'xxx'
            }
        result = requests.Session()
        r = result.get(url, headers=logined_headers, allow_redirects=False)
        j_datas = json.loads(r.text)
        
        # 新版api from xxx/xxx/xxx/xxxgetV2Post?post_id=
        for data in j_datas['floors']:
            if data['sex'] == 1:
                for d in data['images']: # 取得一般imgur的圖片
                    imgCount += 1
                    print( str(imgCount) + '. General Image from: ' + 'https://imgur.com/' + d['image_name'])
                    image_urls.append('https://imgur.com/' + d['image_name'])                
                if data['link'] != None: # link欄位不為None，表示有備份的圖片或影片
                    for d in data['link']['link_results']:
                        if '.jpg' in d['file_name']: # 表示為圖片
                            if 'ppt.cc' in d['link_url']: # 來自ppt.cc的圖片
                                pptCount += 1
                                pw_urls.append('xxxxxxxxx/ppt/' + d['file_name'])
                                print(str(pptCount) + '. 來自ppt.cc的圖片：' + d['file_name'])
                            else: # 來自tkktt的圖片
                                tkkttCount += 1
                                pw_urls.append('xxxxxxxxx/tkktt/' + d['file_name'])
                                print(str(tkkttCount) + '. 來自tkktt的圖片：' + d['file_name'])
                        else: # 表示為圖片
                            videoCount += 1
                            print(str(videoCount) + '. Video: ' + d['link_url'] + ' Password: ' + d['file_name'])
                            record.write(d['link_url'] + ' ' + d['file_name'] + '\n') # 影片額外存在darkka.txt                       

#         # 舊版api，已經無效
#         # 取出備份的ppt.cc圖片url
#         if j_datas['sex'] == 1:
#             for d in j_datas['links']:
#                 if d['sex'] == 1:
#                     for d in d['link_results']:
#                         if '.jpg' in d['file_name']:
#                             if 'ppt' in d['link_url']:
#                                 pptCount += 1
#                                 pw_urls.append('xxxxxxxxx/ppt/' + d['file_name'])
#                                 print(str(pptCount) + '. 來自ppt.cc的圖片：' + d['file_name'])
#                             else:
#                                 tkkttCount += 1
#                                 pw_urls.append('xxxxxxxxx/tkktt/' + d['file_name'])
#                                 print(str(tkkttCount) + '. 來自tkktt的圖片：' + d['file_name'])
#                         else:
#                             videoCount += 1
#                             print(str(videoCount) + '. Video: ' + d['link_url'] + ' Password: ' + d['file_name'])
#                             record.write(d['link_url'] + ' ' + d['file_name'] + '\n') # 影片額外存在darkka.txt
                            
#         # 取出general圖片的url                    
#         for d in j_datas['images']:
#             if d['sex'] == 1:
#                 imgCount += 1
#                 print( str(imgCount) + '. General Image from: ' + 'https:imgur.com/' + d['image_name'])
#                 image_urls.append('https://imgur.com/' + d['image_name'])
            
        
        time.sleep(1)

    print('Already got all image URLs')
    record.close()
    
    return image_urls, pw_urls


def dwPic(imgUrls, pwUrls):
    imageCount = 0
    niceImageCount = 0
        
    # 確認目標資料夾
    picName = input('Enter pic folder name:')
    if not os.path.exists(f'./{picName}/'):
        os.makedirs(f'./{picName}/')

    record = open(f'./{picName}/record.txt', 'w', encoding = 'UTF-8')
    result = requests.Session()
    print('Image Downloading')
    start = time.time()
    
    # 建立Progress bar
    widgets = [
        progressbar.SimpleProgress(), # 內容數量
        progressbar.Bar(), # 顯示bar
        progressbar.Percentage(), # 顯示percent
        ' (',progressbar.Timer(), ')' # 計算經過時間
    ]
    bar = progressbar.ProgressBar(widgets=widgets, max_value=len(imgUrls)+len(pwUrls)).start() #初始化
    progressCount = 0 #用來計算imgUrls與pwUrls兩者數量相加，由於兩者是放在不同的for loop所以以此相加才能顯示連續計算的結果
    
    # 開始下載general pic
    for n, i in enumerate(imgUrls):
        try:
            imageCount += 1
            pic = result.get(i)
            img_by_txt = pic.content
            img_save = open('./' + picName + '/g' + str(imageCount) + '.png', 'wb')
            img_save.write(img_by_txt)
            record.write(f'g{imageCount}:{i}\n')
            img_save.close()
            bar.update(n + 1)
            progressCount = n + 1
            
        except:
            print(f'general pic download faild, the problem url is {i}')
    
    # 開始下載protected pic
    for n, i in enumerate(pwUrls):
        try:
            niceImageCount += 1
            pic = result.get(i)
            img_by_txt = pic.content
            img_save = open('./' + picName + '/pt' + str(niceImageCount) + '.png', 'wb')
            img_save.write(img_by_txt)
            record.write(f'pt{niceImageCount}:{i}\n')
            img_save.close()
            bar.update(progressCount + n + 1)
        except:
            print(f'limit pic download faild, the problem url is {i}')
    
    record.close()
    
    end = time.time()
    
    totalTime = round(end - start, 2)
    
    print(f'Picture is downloaded, total cost {totalTime}s')
    

    
def main():
    whatType = str(input('0:熱門回覆\n1:7 days top 30\n2:key word search\n'))
    if whatType == '0':
        pIds = getPostId(whatType) # 熱門回覆的post id
    elif whatType == '1':
        pIds = getPostId(whatType) # 7天top30的post id
    elif whatType == '2':
        pIds = getPostId(whatType) # key word search的post id

    imgUrls, pwUrls = getPostContent(pIds)
    dwPic(imgUrls, pwUrls)
        

main()