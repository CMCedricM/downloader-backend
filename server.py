from quart import Quart, request
from main import YT_Main

app = Quart(__name__)


@app.route("/user", methods=['POST'])
async def user():
    data = await request.get_json()
    if(data):
       userId = data.get("user")
       yt =  YT_Main(userId)
       await yt.connect()
       user = await yt.fetchUserInformation(userId)
       print(user.id)
       return  {"Data": str(user)}
    return {"Message" : "No Data"}




if(__name__) == "__main__": 
    app.run(debug=True)