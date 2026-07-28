# (c) @RavanDeveloperr
# Rkn Developer 
# Don't Remove Credit 😔
# Telegram Channel @RavanDeveloper & @Rkn_Bots
# Developer @RavanDeveloperr
# Special Thanks To (https://github.com/JayMahakal98)
# Update Channel @Digital_Botz & @DigitalBotz_Support

"""
Apache License 2.0
Copyright (c) 2022 @RavanDeveloper

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Telegram Link : https://t.me/RknDeveloper
Repo Link : https://github.com/RknDeveloper/Rkn_Auto-Request-Approve-bot
License Link : https://github.com/RknDeveloper/Rkn_Auto-Request-Approve-bot/blob/main/LICENSE
"""

# database imports
import motor.motor_asyncio, datetime, pytz

# bots imports
from configs import rkn1

class Database:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.user
        self.chat = self.db.chat
        
    def new_user(self, id):
        return dict(_id=int(id))
            
            
    async def add_user(self, b, m):
        u = m.from_user
        if not await self.is_user_exist(u.id):
            user = self.new_user(u.id)
            try:
                await self.col.insert_one(user)            
                await self.send_user_log(b, u)
            except Exception as e:
                if "duplicate key" not in str(e):
                    raise

    async def is_user_exist(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return bool(user)

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        all_users = self.col.find({})
        return all_users

    async def delete_user(self, user_id):
        await self.col.delete_many({'_id': int(user_id)})
    
    async def send_user_log(self, b, u):
        if rkn1.LOG_CHANNEL is not None:
            await b.send_message(
            rkn1.LOG_CHANNEL,
            f"**--Nᴇᴡ Uꜱᴇʀ Sᴛᴀʀᴛᴇᴅ Tʜᴇ Bᴏᴛ--**\n\nUꜱᴇʀ: {u.mention}\nIᴅ: `{u.id}`\nUɴ: @{u.username}\n\nBy: {b.mention}"
        )
        
    async def add_chat(self, b, m):
        if not await self.is_chat_exist(m.chat.id):
            user = self.new_user(m.chat.id)
            try:
                await self.chat.insert_one(user)            
                await self.send_chat_log(b, m)
            except Exception as e:
                if "duplicate key" not in str(e):
                    raise

    async def is_chat_exist(self, id):
        user = await self.chat.find_one({'_id': int(id)})
        return bool(user)

    async def total_chats_count(self):
        count = await self.chat.count_documents({})
        return count

    async def get_all_chats(self):
        all_users = self.chat.find({})
        return all_users

    async def delete_chat(self, user_id):
        await self.chat.delete_many({'_id': int(user_id)})
    
    async def send_chat_log(self, b, m):
        if rkn1.LOG_CHANNEL is not None:
            await b.send_message(
            rkn1.LOG_CHANNEL,
            f"**--Nᴇᴡ Uꜱᴇʀ Sᴛᴀʀᴛᴇᴅ Tʜᴇ Bᴏᴛ--**\n\nUꜱᴇʀ: {m.chat.title}\nIᴅ: `{m.chat.id}`\nUɴ: @{m.chat.username}\n\nBy: {m.from_user.mention} & {b.mention}"
        )
        
rkn_botz = Database(rkn1.DB_URL, rkn1.DB_NAME)

# Rkn Developer 
# Don't Remove Credit 😔
# Telegram Channel @RavanDeveloper & @Rkn_Bots
# Developer @RavanDeveloperr
# Update Channel @Digital_Botz & @DigitalBotz_Support