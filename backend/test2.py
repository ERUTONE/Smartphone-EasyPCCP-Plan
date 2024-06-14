import requests
import win32com.client
import pythoncom

class NotificationHandler:
    def __init__(self, url):
        self.url = url

    def on_notification(self, event):
        try:
            # WMIイベントから通知内容を取得
            notification_text = event.Description
            print(f"Detected notification: {notification_text}")

            # Webサイトに通知を転送
            self.send_notification_to_website(notification_text)
        except Exception as e:
            print(f"Error processing notification: {e}")

    def send_notification_to_website(self, notification):
        data = {"notification": notification}
        response = requests.post(self.url, json=data)
        print(f"Notification sent to website, status code: {response.status_code}")

def main():
    notification_url = "https://example.com/notify"  # WebサイトのURL
    handler = NotificationHandler(notification_url)

    # WMIイベントの設定
    wmi = win32com.client.GetObject("winmgmts:")
    wql = "SELECT * FROM __InstanceCreationEvent WITHIN 1 WHERE TargetInstance ISA 'Win32_NTLogEvent'"
    watcher = wmi.ExecNotificationQuery(wql)

    print("Listening for notifications...")
    
    while True:
        try:
            event = watcher.NextEvent()
            pythoncom.PumpWaitingMessages()
            handler.on_notification(event)
        except KeyboardInterrupt:
            print("Stopping notification listener.")
            break

if __name__ == "__main__":
    main()
