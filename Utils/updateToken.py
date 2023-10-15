from Utils.connection import *
from Utils.libraries import *

async def updateToken(message):
    message_str = str(message.content).split("\n")
    if len(message_str) == 2:
        amount =  int(message_str[1])
        guild_id = message.guild.id

        if message.attachments:
            attachment = message.attachments[0]
            if attachment.filename.endswith('.csv'):
                filename = attachment.filename
                await attachment.save(filename)
                response = await tatsuAPICall(guild_id, amount, filename)
                return response
            else:
                return {"message": "Please attach a **CSV** file", "success": False}
        else:
            return {"message": "Please attach a **CSV** file", "success": False}
    else:
        return {"message":"You forgot to mention **TOKEN_AMONUT**", "success": False}

async def tatsuAPICall(guild_id, amount, csv_filename):
    # check whether the event exists in the DB
    cluster = await get_connection()
    db = cluster["Events"]
    updated_user = []
    failed_user = []
    try:
        TATSU_API_TOKEN = config('TATSU_API_TOKEN')
        payload = {
            'action': 0,
            'amount': amount
        }
        headers = {'Authorization': TATSU_API_TOKEN}

        df = pd.read_csv(csv_filename)
        columns = [col for col in df.columns if 'discord id' in col.lower()]
        # Specify that the 'discord id' columns should be treated as strings to maintain precision
        column_dtype = {col: str for col in columns}

        df = pd.read_csv(csv_filename, dtype=column_dtype)

        columns = [col for col in df.columns if 'discord id' in col.lower()]
        df_columns = df[columns]

        for index, row in df_columns.iterrows():
            for col in columns:
                value = row[col]
                if not pd.isnull(value):
                    print(value)
                    endpoint_url = f'https://api.tatsu.gg/v1/guilds/{guild_id}/members/{value}/points'
                    response = requests.patch(endpoint_url, json=payload, headers=headers)

                    if response.status_code == 200:
                        modified_points_data = response.json()
                        updated_user.append(str(modified_points_data["user_id"]))
                        print(f'Successfully modified points: {modified_points_data}')

                    else:
                        failed_user.append(str(value))
                        print(f'Failed to modify points. Status code: {response.status_code}')
                        # print(response.text)

    except Exception as e:
        print(str(e))
        return {"message": "Something went wrong", "success": False}
    return {"message": "Tokens have been updated of eligible participants", "updated": updated_user, "failed": failed_user, "success": True}
