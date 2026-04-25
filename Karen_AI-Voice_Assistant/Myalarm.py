import datetime
import winsound
import threading

def play_alarm():
    print("Alarm is running...")
    winsound.PlaySound('abc.wav', winsound.SND_FILENAME | winsound.SND_LOOP)

def alarm(Timing):
    
    alarm_time = datetime.datetime.strptime(Timing, "%I:%M %p")
    Horeal = alarm_time.hour
    Mireal = alarm_time.minute

    print(f"Done, alarm is set for {Timing}")

    def check_time():
        while True:
            now = datetime.datetime.now()
            if Horeal == now.hour and Mireal == now.minute:
                play_alarm()
                break

    
    t = threading.Thread(target=check_time)
    t.daemon = True  
    t.start()
