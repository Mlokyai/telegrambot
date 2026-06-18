import os
import re
from telethon import TelegramClient, events
import requests
from bs4 import BeautifulSoup

# إعدادات الحساب والبوت (يتم جلبها من بيئة التشغيل بأمان)
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
TARGET_CHANNEL = os.environ.get("TARGET_CHANNEL", "") # قناتك الخاصة

# مصفوفة مؤقتة في الذاكرة لحفظ بصمات الأخبار الأخيرة (منع التكرار)
processed_news = []

# كلمات مفتاحية لتصفية المواهب الصاعدة
SCOUT_KEYWORDS = ["موهبة", "لاعب صاعد", "جوهرة", "Wonderkid", "شاب", "بالغ من العمر"]

client = TelegramClient('news_scout_session', API_ID, API_HASH)

def is_duplicate(text):
    # تنظيف النص الأساسي لمقارنة المضمون وإهمال الروابط والاختلافات الطفيفة
    clean_text = re.sub(r'http\S+|@\S+|[^а-яА-Яa-zA-Z0-aligned0-9\s\u0600-\u06FF]', '', text).strip()
    # نأخذ أول 50 حرف كبصمة تقريبية للخبر
    fingerprint = clean_text[:50]
    
    if fingerprint in processed_news:
        return True
    
    processed_news.append(fingerprint)
    if len(processed_news) > 200: # الحفاظ على حجم الذاكرة خفيفاً
        processed_news.pop(0)
    return False

@client.on(events.NewMessage)
async def handler(event):
    # جلب المعرف الرقمي للقناة المصدر
    chat_id = event.chat_id
    text = event.raw_text
    
    if not text or is_duplicate(text):
        return

    # نظام كشاف المواهب
    is_scout_news = any(keyword in text for keyword in SCOUT_KEYWORDS)
    
    if is_scout_news:
        # إضافة إيموجي وتنسيق خاص بأخبار المواهب
        formatted_text = f"🕵️‍♂️ **[رادار المواهب الصاعدة]**\n\n{text}"
    else:
        formatted_text = f"📢 **[خبر جديد]**\n\n{text}"
        
    # إعادة توجيه النص المنسق والمصفى إلى قناتك
    await client.send_message(TARGET_CHANNEL, formatted_text)

print("النظام يعمل الآن ويتسمع للقنوات الإخبارية...")
client.start()
client.run_until_disconnected()
