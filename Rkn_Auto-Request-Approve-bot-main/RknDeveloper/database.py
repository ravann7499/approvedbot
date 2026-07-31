# database imports
import motor.motor_asyncio
from configs import rkn1


class Database:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.user
        self.chat = self.db.chat

    def new_user(self, user_id):
        return {"_id": int(user_id)}

    async def is_user_exist(self, user_id):
        return await self.col.find_one({"_id": int(user_id)}) is not None

    async def add_user(self, bot, message):
        user = message.from_user
        if not user:
            return

        try:
            if not await self.is_user_exist(user.id):
                await self.col.insert_one(self.new_user(user.id))
                await self.send_user_log(bot, user)
        except Exception as e:
            print(f"Add User Error: {e}")

    # NEW FUNCTION (Use this after auto approve)
    async def add_user_by_id(self, user_id):
        try:
            if not await self.is_user_exist(user_id):
                await self.col.insert_one({"_id": int(user_id)})
                return True
        except Exception as e:
            print(f"Add User By ID Error: {e}")
        return False

    async def total_users_count(self):
        return await self.col.count_documents({})

    async def get_all_users(self):
        return self.col.find({})

    async def delete_user(self, user_id):
        await self.col.delete_one({"_id": int(user_id)})

    async def send_user_log(self, bot, user):
        if rkn1.LOG_CHANNEL:
            try:
                username = f"@{user.username}" if user.username else "No Username"

                await bot.send_message(
                    rkn1.LOG_CHANNEL,
                    f"🆕 New User\n\n"
                    f"👤 {user.mention}\n"
                    f"🆔 `{user.id}`\n"
                    f"🌐 {username}"
                )
            except Exception as e:
                print(e)

    # ---------------- CHAT ---------------- #

    async def is_chat_exist(self, chat_id):
        return await self.chat.find_one({"_id": int(chat_id)}) is not None

    async def add_chat(self, bot, message):
        chat = message.chat

        try:
            if not await self.is_chat_exist(chat.id):
                await self.chat.insert_one({"_id": int(chat.id)})
                await self.send_chat_log(bot, message)
        except Exception as e:
            print(f"Add Chat Error: {e}")

    async def total_chats_count(self):
        return await self.chat.count_documents({})

    async def get_all_chats(self):
        return self.chat.find({})

    async def delete_chat(self, chat_id):
        await self.chat.delete_one({"_id": int(chat_id)})

    async def send_chat_log(self, bot, message):
        if rkn1.LOG_CHANNEL:
            try:
                username = (
                    f"@{message.chat.username}"
                    if message.chat.username
                    else "No Username"
                )

                await bot.send_message(
                    rkn1.LOG_CHANNEL,
                    f"🆕 New Chat\n\n"
                    f"📢 {message.chat.title}\n"
                    f"🆔 `{message.chat.id}`\n"
                    f"🌐 {username}"
                )
            except Exception as e:
                print(e)


rkn_botz = Database(rkn1.DB_URL, rkn1.DB_NAME)# Update Channel @Digital_Botz & @DigitalBotz_Support
