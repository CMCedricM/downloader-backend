import asyncio
from prisma import Prisma


async def main() -> None: 
    prisma = Prisma()
    await prisma.connect()
    
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
    
if __name__ == '__main__': 
    asyncio.run(main())