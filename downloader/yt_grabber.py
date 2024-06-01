import yt_dlp
import json
from prisma import Prisma, Client
from prisma.models import User as PrismaUser, DataOwnership, Video as PrismaVideo, UserPreferences


class Downloader: 
    def __init__(self, prisma: Prisma , user: PrismaUser, ownership: DataOwnership): 
        self.prisma: Prisma = prisma
        self.user = user
        self.dataOwnership = ownership
        
        self.data : PrismaVideo = None
        self.USER_PREFERENCES: UserPreferences = None
        self.DESTINATION_FOLDER: str = None 
    
    async def parseForDownload(self):
        # Grab the user destination folder first
        self.USER_PREFERENCES = await self.prisma.userpreferences.find_first(where={'DataOwnershipId': self.dataOwnership.id})
        if(not self.USER_PREFERENCES): 
            print("No User Preferences Found, cannot continue")
            return False
        self.DESTINATION_FOLDER = self.USER_PREFERENCES.DestinationFolder
        self.data = await self.prisma.video.find_many(where={'dataOwnershipId': self.dataOwnership.id})
        if(not self.data): 
            print("No Videos Detected for the current user")
            return False
        return True
    
    async def runDownloader(self): 
        ydl_opts = self.USER_PREFERENCES.MusicPreferences if self.USER_PREFERENCES.DownloadType == 'AudioOnly' else self.USER_PREFERENCES.VideoPreferences
        if(not ydl_opts): ydl_opts = {}
        
        output_template = self.DESTINATION_FOLDER + '/' + '%(title)s.%(ext)s'
        ydl_opts["outtmpl"] = output_template
        
        urls_test = self.data[0:4]
        with yt_dlp.YoutubeDL(ydl_opts) as ydl: 
            error_code = ydl.download(urls_test)
        
        
        
    
        



    
        