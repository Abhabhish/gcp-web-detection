import os
from google.cloud import vision
import concurrent.futures
import json

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]='./harsh.json'
client = vision.ImageAnnotatorClient()

urls = []
for tuple in os.walk('img'):
    for file_name in tuple[2]:
        # if file_name.endswith('.jpg'):
           file_path = tuple[0]+'/'+file_name
           urls.append(file_path)

full_match_json = {}
partial_match_json = {}
n=0
def main(url):
    global n
    try:
        with open(url, "rb") as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        web_detection = client.web_detection(image=image).web_detection

        if web_detection.full_matching_images:
            full_matches = []
            for img in web_detection.full_matching_images:
                full_matches.append(img.url)
            full_match_json[url] = full_matches
        elif web_detection.partial_matching_images:
            partial_matches = []
            for img in web_detection.partial_matching_images:
                partial_matches.append(img.url)
            partial_match_json[url] = partial_matches
    except:
      try:
        with open(url, "rb") as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        web_detection = client.web_detection(image=image).web_detection

        if web_detection.full_matching_images:
            full_matches = []
            for img in web_detection.full_matching_images:
                full_matches.append(img.url)
            full_match_json[url] = full_matches
        elif web_detection.partial_matching_images:
            partial_matches = []
            for img in web_detection.partial_matching_images:
                partial_matches.append(img.url)
            partial_match_json[url] = partial_matches
      except Exception as e:
          print(e)
    with open('done.txt','a',encoding='utf-8') as fr:
        fr.write(url+'\n')
    n+=1 
    print(n)

def main2():
    with concurrent.futures.ThreadPoolExecutor(max_workers=200) as Executor:
        future_to_url = {Executor.submit(
            main, url=url): url for url in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
            except Exception as e:
                raise(e)
if __name__ == '__main__':
    main2()

with open('full_match_json.json','w',encoding='utf-8') as f:
    json.dump(full_match_json,f,indent=4)

with open('partial_match_json.json','w',encoding='utf-8') as f:
    json.dump(partial_match_json,f,indent=4)

print(f'full match: {len(full_match_json)}')
print(f'partial match: {len(partial_match_json)}')
