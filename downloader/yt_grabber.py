import yt_dlp
import json
from prisma import Prisma, Client
from prisma.models import User as PrismaUser, DataOwnership, Video as PrismaVideo


class Downloader: 
    def __init__(self, prisma: Prisma , user: PrismaUser, ownership: DataOwnership): 
        self.prisma: Prisma = prisma
        self.user = user
        self.dataOwnership = ownership
        
        self.data : PrismaVideo = None
    
    async def parseForDownload(self):
        self.data : PrismaVideo = await self.prisma.video.find_many(where={'dataOwnershipId': self.dataOwnership.id})
        if(not self.data): print("No Videos Detected for the current user")
        print(self.data)
    
        



    
        