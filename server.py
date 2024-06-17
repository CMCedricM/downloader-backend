from quart import Quart, request
from main import fetchUserInformation

app = Quart(__name__)


@app.route("/user", methods=['POST'])
async def user():
    data = await request.get_json()
    if(data):
       userId = data.get("user")
       user = await fetchUserInformation(userId)
       return user
    return {"Message" : "No Data"}




if(__name__) == "__main__": 
    app.run(debug=True)