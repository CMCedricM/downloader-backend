import asyncio, json
from prisma import Prisma


async def main() -> None: 
    prisma = Prisma()
    await prisma.connect()
    # Delete All Data
    await prisma.userplaylist.delete_many()
    print("Deleted User PlayLists")
    await prisma.dataownership.delete_many()
    print("Deleted Data Ownership")
    await prisma.user.delete_many()
    print("Deleted User Data")
    await prisma.userpreferences.delete_many()
    print("Deleted User Preferences")
    
    user = await prisma.user.create(
        data={
            'email' : 'c.m.cedricm17@gmail.com', 
            'userFullName': 'Cedric'
        }
    )
    print("Created User")
    ownership = await prisma.dataownership.create(
        data={
            'userId': user.id  
        }
    )
    print("Created Ownership Record")
    playlist = await prisma.userplaylist.create(
        data={
            'PlayListURL': 'PLwnRU_LD0h-vPfaupYzw5L4AVGB-vj_Kf', 
            'PlayListTitle': "Synced Liked",
            'Status': 'Active',
            'dataOwnershipId': ownership.id
        }
    )
    print("Created Playlist")
    musicPreferences = json.dumps({
        'format': 'm4a/bestaudio/best',
        'postprocessors': {
             'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }
    })
    userPreferences = await prisma.userpreferences.create(data={
        'DataOwnershipId': ownership.id,
        'userEmail': user.email, 
        'DestinationFolder': '/Users/cedric-personal/Documents/Programming/downloader-backend/test_out',
        'DownloadType' : 'AudioOnly',
        'MusicPreferences': musicPreferences 
    })
    print("Created User Preferences")
    
if __name__ == '__main__': 
    asyncio.run(main())