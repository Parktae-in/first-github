import requests
import json

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"}

#dict 형태인지 list형태인지 확인
def find_key(data, target_key):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == target_key:
                yield value
            else:
                yield from find_key(value, target_key)
    elif isinstance(data, list):
        for item in data:
            yield from find_key(item, target_key)


def search_youtube(keyword):
    #결과 리스트 변수 지정
    results = []

    #검색 URL
    url = f"https://www.youtube.com/results?search_query={keyword}"
    r = requests.get(url, headers=header)

    #검색하려는 초기 데이터 블록 시작/종료 부분
    p_start = "var ytInitialData = "
    p_end = "};"

    #초기 데이터 블록 시작/종료지점 검색
    index_start = r.text.find(p_start)
    index_end = r.text.find(p_end, index_start)
    #print(index_start, index_end)

    #검색값이 없을경우 (잘못된 검색)
    if index_end < index_start:
        return results
    
    #var ytInitialData = 부분 제외 / index_end 까지 포함시키기 위해 +1
    data = r.text[index_start + len(p_start) : index_end + 1]
    _json = json.loads(data)
    contents = _json.get("contents").get("twoColumnSearchResultsRenderer").get("primaryContents").get("sectionListRenderer").get("contents")
    video_renderer = list(find_key(contents, "videoRenderer"))

    for vr in video_renderer:
        vid = vr.get("videoId")
        vthumb = vr.get("thumbnail").get("thumbnails")[0].get("url")
        vlength = vr.get("lengthText")
        if vlength is None:
            continue
        vduration = vlength.get("simpleText")
        vcount = vr.get("viewCountText").get("simpleText")
        vtitle = vr.get("title").get("runs")[0].get("text")
        
        #결과 리스트 데이터 추가
        results.append({
            "vid": vid,
            "vtitle": vtitle,
            "vcount": vcount,
            "vthumb": vthumb,
            "vduration": vduration
        })
    return results
        


    #print(data[0:50])
    #print(data)

#파이썬 스크립트 실행 시작점
if __name__ == "__main__":
    results = search_youtube("일본")
    print("검색 결과를 출력합니다.")
    print("=================================================")
    for r in results:
        print(r)
        print("=================================================")
    