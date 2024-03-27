from dotenv import load_dotenv
import googleapiclient.discovery as gAPI
import json, os
load_dotenv()

api_service_name = os.getenv("GOOGLE_API_SERVICE")
api_version = os.getenv("GOOGLE_API_VERSION")
DEVELOPER_KEY = os.getenv("GOOGLE_API_KEY")

youtube = gAPI.build(api_service_name, api_version, developerKey=DEVELOPER_KEY)

def getVideoURLs(videoData: list) -> list[str]: 
    videoTags: list[str] = []
    for i in range(len(videoData)):
        if("contentDetails" in videoData[i] and "videoId" in videoData[i]["contentDetails"]): 
            videoTags.append(videoData[i]["contentDetails"]["videoId"])
    return videoTags     


def main():
    videoTagsData: list[str] = []
    playlists = youtube.playlistItems().list(part=['id','status', "contentDetails"],playlistId='PLwnRU_LD0h-vPfaupYzw5L4AVGB-vj_Kf')
    data = playlists.execute()
    videoTagsData.extend(getVideoURLs(data["items"]))


    nextPageData = data["nextPageToken"] if "nextPageToken" in data else None
    while(nextPageData): 
        dataRequest = youtube.playlistItems().list(part=['id','status', "contentDetails"],playlistId='PLwnRU_LD0h-vPfaupYzw5L4AVGB-vj_Kf', pageToken=nextPageData)
        dataResponse = dataRequest.execute()
        if "nextPageToken" in dataResponse: 
            nextPageData = dataResponse["nextPageToken"] 
        else: nextPageData = None
        videoTagsData.extend(getVideoURLs(dataResponse['items']))
        
    print("Video Tags: ", videoTagsData)
    
if __name__ == "__main__": 
    main()


