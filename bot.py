import discord
import aiohttp
import os
from config import token # Token'ı güvenli şekilde dışarıdan al

SAVE_DIR = "M6L3"
SAVE_PATH = os.path.join(SAVE_DIR, "pngegg (2).png")  # Dosya yolu güvenli hale getirildi

# Eğer kayıt klasörü yoksa oluştur
os.makedirs(SAVE_DIR, exist_ok=True)

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Mesaj içeriğini almak için gerekli

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Bot {client.user} olarak giriş yaptı!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    print(f"Mesaj geldi: {message.content}, Attachments: {message.attachments}")

    if message.content.lower() == "kaydet":
        if not message.attachments:
            await message.channel.send("Lütfen `kaydet` komutu ile birlikte bir görsel yükleyin!")
            return
        
        for attachment in message.attachments:
            if attachment.filename.lower().endswith(".png"):  # Sadece PNG dosyalarını kaydet
                print(f"Eklenen dosya: {attachment.filename}")
                
                async with aiohttp.ClientSession() as session:
                    async with session.get(attachment.url) as resp:
                        if resp.status == 200:
                            with open(SAVE_PATH, "wb") as f:
                                f.write(await resp.read())
                            
                            await message.channel.send(f"Görsel başarıyla kaydedildi: `{SAVE_PATH}`")
                            return  # İlk uygun resmi kaydettikten sonra çık
        
        await message.channel.send("Yalnızca `PNG` dosyalarını kaydedebilirim! İpucu: PNGEGG adlı uygulamadan png dosya türünden resimler alabilirsiniz.")

client.run(token)
