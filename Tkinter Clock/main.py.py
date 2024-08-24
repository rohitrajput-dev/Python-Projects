import tkinter as tk
import datetime
import winsound

# Global list to keep track of alarms
alarms = []

def update_alarms():
    """Updates all alarms and checks if they should be triggered."""
    now = datetime.datetime.now()
    for alarm_time in alarms:
        remaining_time = alarm_time - now
        if remaining_time.total_seconds() <= 0:
            # Alarm should be triggered
            winsound.PlaySound("Music.wav", winsound.SND_ASYNC)
            alarms.remove(alarm_time)  # Remove triggered alarm
    display_alarms()  # Update the display
    # Schedule the function to run again after 1 second
    window.after(1000, update_alarms)

def set_alarm():
    """Sets the alarm and adds it to the list."""
    now = datetime.datetime.now()
    try:
        if hour.get():
            alarm_hour = int(hour.get())
        else:
            alarm_hour = now.hour
        if  min.get():
            alarm_minute = int(min.get())
        else:
            alarm_minute = now.minute
        if sec.get():
            alarm_second = int(sec.get())
        else:
            alarm_second = now.second
        alarm_time = datetime.datetime(now.year, now.month, now.day, alarm_hour, alarm_minute, alarm_second)
        if alarm_time < now:
            alarm_time += datetime.timedelta(days=1)  # Set for the next day if the time is in the past
        if alarm_time  not in alarms:
            alarms.append(alarm_time)
        display_alarms()
    except ValueError:
        status_label.config(text="Invalid inputs. Please enter only numbers.")
        window.after(2000, lambda: status_label.config(text=""))

alarm_labels = {}

def display_alarms():
    """Displays the list of set alarms using available space.""" 
    # Remove the previous label from the grid
    
    global setAlarmLable

    for label_id in list(alarm_labels.keys()):
        alarm_labels[label_id].place_forget()

    # Remove previous setAlarmLable if it exists
    if 'setAlarmLable' in globals():
        setAlarmLable.place_forget()

    num_alarms = len(alarms)
    
    if num_alarms == 0:
        alarm_text = "No alarms set"
        setAlarmLable = tk.Label(window, text=alarm_text, fg="white", bg="#922B21", relief="ridge", font=("Helvetica", 15, "bold"))
        setAlarmLable.place(x=175, y=200)     
    else:
        alarm_text="Your Active Alarms"
        setAlarmLable = tk.Label(window, text=alarm_text, fg="white", bg="#922B21", relief="ridge", font=("Helvetica", 15, "bold"))
        setAlarmLable.place(x=150, y=200)     


    # Create and place the main label

    y_offset = 240
    for i, alarm in enumerate(sorted(alarms)):
        alarm_time = alarm.strftime("%H:%M:%S")
        label = tk.Label(window, text=alarm_time, fg="white", bg="#922B21", font=("Arial", 15))
        alarm_labels[i] = label
        if i < 36:
            submit_button.config(state=tk.NORMAL)
            label.place(x=50 + (i % 4) * 100, y=y_offset + (i // 4) * 30)
        else:
            submit_button.config(state=tk.DISABLED)
            status_label.config(text="No more Alarms. wait for some alarms to be cleared.")
            status_label.place(x = 10, y = 510)
            window.after(2000, lambda: status_label.config(text=""))


# Create the main window
window = tk.Tk()
window.title("Alarm Clock")
window.geometry("500x600")
window.config(bg="#3251c2")
window.resizable(width=False, height=False)


submit_button = tk.Button(window, text="Set Your Alarm", fg="Black", bg="#D4AC0D", width=15, command=set_alarm, font=(20))
submit_button.place(x=160, y=140)

setYourAlarm = tk.Label(window, text="Set Time for 24 hour Cycle", fg="white", bg="#922B21", relief="ridge", font=("Helvetica", 15, "bold"))
setYourAlarm.place(x=120, y=20)

hour = tk.StringVar()
min = tk.StringVar()
sec = tk.StringVar()

hourTime = tk.Entry(window, textvariable=hour, bg="#48C9B0", width=4, font=(20))
hourTime.place(x=160, y=60)

minTime = tk.Entry(window, textvariable=min, bg="#48C9B0", width=4, font=(20))
minTime.place(x=220, y=60)

secTime = tk.Entry(window, textvariable=sec, bg="#48C9B0", width=4, font=(20))
secTime.place(x=280, y=60)

addTime = tk.Label(window, text="Hour     Min     Sec", font=60, fg="white", bg="black")
addTime.place(x=160, y=100)

time_format = tk.Label(window, text="Remember to set time in 24-hour format!", fg="white", bg="#922B21", font=("Arial", 15))
time_format.place(x=70, y=550)

# Start the update loop
update_alarms()

# Start the Tkinter event loop
window.mainloop()
