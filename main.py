from dotenv import load_dotenv
import googleapiclient.discovery as gAPI
from prisma import Prisma, Client
from prisma.models import User, UserPlaylist, DataOwnership, Video
import json, os, argparse, asyncio

load_dotenv()


LOGS_LOCATION = os.path.join(os.path.dirname(__file__), "Logs")

api_service_name = os.getenv("GOOGLE_API_SERVICE")
api_version = os.getenv("GOOGLE_API_VERSION")
DEVELOPER_KEY = os.getenv("GOOGLE_API_KEY")
YOUTUBE_PREFIX = os.getenv('YOUTUBE_PREFIX')

youtube = gAPI.build(api_service_name, api_version, developerKey=DEVELOPER_KEY)

prisma = Prisma()

parser = argparse.ArgumentParser(description="A Program to Grab Information from a Youtube Playlist")
parser.add_argument('--userId', type=str, default=None, help="User id from postrgres database")
parser.add_argument('--print_response', type=bool, default=False, help="Log the response data from the youtube api")
args = parser.parse_args()
USER_ID: int = args.userId
LOG_RESPONSE: bool = args.print_response

def getVideoURLs(videoData: list) -> list[dict[str, str]]: 
    videoTags: list[dict[str,str]] = []
    for i in range(len(videoData)):
        if("contentDetails" in videoData[i] and "videoId" in videoData[i]["contentDetails"]): 
            videoTags.append({"VideoTag": videoData[i]["contentDetails"]["videoId"], "VideoTitle" : videoData[i]["snippet"]["title"]})
    return videoTags     


async def fetchUserPlaylist(UserID: int) -> User | None: 
    userInfo = await prisma.user.find_unique(where={'id' : int(UserID)}, include={'DataOwnership': True})
    return userInfo

async def main():
    await prisma.connect()
    
    if(not USER_ID): 
       print("Error USER_ID ==> No USER_ID provided in args\n Proper usage: python3 ./main.py --userId  <userID>")
       exit(-1)
       
    userData = await fetchUserPlaylist(USER_ID)
    if(not userData): 
        print(f"Error ==> User with ID {USER_ID} could not be found.")
        exit(-1)
   
    PLAYLIST_IDS = await prisma.userplaylist.find_many(where={'dataOwnershipId': int(userData.DataOwnership.id)})
    
    for i in range(len(PLAYLIST_IDS)):
        current_playlist = PLAYLIST_IDS[i].PlayListURL
        videoTagsData: list[object[int, str]] = []
        playlists = youtube.playlistItems().list(part=['id','status', "contentDetails", "snippet"],playlistId=current_playlist)
        data = playlists.execute()
        videoTagsData.extend(getVideoURLs(data["items"]))


        nextPageData = data["nextPageToken"] if "nextPageToken" in data else None
        while(nextPageData): 
            dataRequest = youtube.playlistItems().list(part=['id','status', "contentDetails", "snippet"],playlistId=current_playlist, pageToken=nextPageData)
            dataResponse = dataRequest.execute()
            if "nextPageToken" in dataResponse: 
                nextPageData = dataResponse["nextPageToken"] 
            else: nextPageData = None
            videoTagsData.extend(getVideoURLs(dataResponse['items']))
            
        # print("Video Tags: ", videoTagsData)
 
    batcher = prisma.batch_()
    for dataItem in videoTagsData: 
        batcher.video.create(data={'dataOwnershipId': userData.DataOwnership.id, 'YT_Identifier': dataItem["VideoTag"], 'VideoURL': YOUTUBE_PREFIX + dataItem["VideoTag"], "Video_Title": dataItem["VideoTitle"] })
    if(len(videoTagsData) > 1):
        await batcher.commit()    
    
    
if __name__ == "__main__": 
    asyncio.run(main())


