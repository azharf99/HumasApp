from typing import Any
import requests
import os
from django.conf import settings
from dotenv import load_dotenv

load_dotenv(os.path.join(settings.BASE_DIR, '.env'))
token = os.getenv("WA_AIS_TOKEN")
admin_phone = os.getenv("ADMIN_PHONE")
sender_albinaa_phone = os.getenv("SENDER_ALBINAA_PHONE")

def send_WA_create_update_delete(phone: str | None = admin_phone, action: str = "", messages: str = "", type: str = "", slug: str = "") -> requests.Response | None:        
    if not settings.DEBUG:
        message = f'''*[NOTIFIKASI HUMAS]*
Anda berhasil {action} {messages}.
Detail:
https://humas.albinaa.sch.id/{type}{slug}'''
        
        url = f"https://albinaa.sch.id/wp-content/wa/api.php?sender={sender_albinaa_phone}&no=62{phone[1:] if phone.startswith('0') and phone != '0' else admin_phone[1:]}&pesan={message}"

        try:
            data = requests.get(url, timeout=10)
            return data
        except:
            pass
    return None

def send_WA_general(phone: str | None = admin_phone, action: str = "", messages: str = "") -> requests.Response | None:        
    if not settings.DEBUG:
        message = f'''*[NOTIFIKASI HUMAS]*
Anda berhasil {action} {messages}.
Detail:
https://humas.albinaa.sch.id/'''
        
        url = f"https://albinaa.sch.id/wp-content/wa/api.php?sender={sender_albinaa_phone}&no=62{phone[1:] if phone.startswith('0') and phone != '0' else admin_phone[1:]}&pesan={message}"

        try:
            data = requests.get(url, timeout=10)
            return data
        except:
            pass
    return None