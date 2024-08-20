import pyttsx3, webbrowser as wb, smtplib, datetime, wikipedia, os, time
import speech_recognition as sr
import random
from youtubesearchpython import VideosSearch


recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Set the speech rate
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-5)

# Set the voice
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

recognizer.pause_threshold = 0.5

reminders = []

hour = int(datetime.datetime.now().hour)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def greeting():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak('Good Morning!')
    elif hour >= 12 and hour < 18:
        speak('Good Afternoon!')
    else:
        speak('Good Evening!')

    speak('I am glad to see you back Bishal')
    speak('How can I help you today sir?')


def send_email(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('broy950@gmail.com', 'plbzzgnixbxujceo')  # Use environment variables for security
        server.sendmail('broy950@gmail.com', to, content)
        server.close()
        speak("Email has been sent successfully!")
    except Exception as e:
        print(e)
        speak("I was unable to send the email. Please try again later.")

def setReminder(reminders):
    speak("What would you like me to remind you sir?")
    content = capture_command()
    speak("What time or date would you like to set this as?")
    timeRemind = capture_command()

    fullCommand = content + 'at' + timeRemind
    reminders.append(fullCommand)
    
    return reminders


def tasks_do(text):
    # Handle sending an email
    if 'send email to' in text:
        try:
            speak("What would you like to send, sir?")
            content = capture_command()  # Captures the content of the email
            to = "broy950" + '@gmail.com'
            send_email(to, content)
        except Exception as e:
            print(e)
            speak("I was unable to send the email. Please try again later.")
    
    # Handle opening Google
    elif 'open google' in text or 'open browser' in text:
        wb.open('https://www.google.com')
    
    # Handle opening GitHub
    elif 'open github' in text:
        wb.open('https://github.com/')

    # Handle Google search
    elif 'search in google for' in text:
        try:
            search_query = text.replace('search in google for', '').strip()
            wb.open(f'https://www.google.com/search?q={search_query}')
        except:
            speak('Could not catch that. Please try again.')

    # Handle YouTube search
    elif 'search in youtube for' in text:
        try:
            search_query = text.replace('search in youtube for', '').strip()
            wb.open(f'https://www.youtube.com/results?search_query={search_query}')
        except:
            speak('Could not catch that. Please try again.')

    # Handle Wikipedia search
    elif 'search in wikipedia for' in text:
        try:
            search_query = text.replace('search in wikipedia for', '').strip()
            speak('Here is what I found on Wikipedia.')
            wiki_results = wikipedia.summary(search_query, sentences=4)
            print(wiki_results)
            speak(wiki_results)
        except:
            speak('Could not catch that. Please try again.')

    # Handle playing a specific video on YouTube
    elif 'play in youtube' in text:
        try:
            search_query = text.replace('play in youtube', '').strip()
            search = VideosSearch(search_query, limit=1)
            search_link = search.result()['result'][0]['link']
            wb.open(search_link)
        except:
            speak('Could not catch that. Please try again.')
    
    # Handle opening Visual Studio Code
    elif 'open virtual studio' in text:
        path = "C:/Users/broy9/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Visual Studio Code/Visual Studio Code.lnk"
        os.startfile(path)
    
    # Handle playing music
    elif 'play music' in text:
        path = "D:/music"
        songs = os.listdir(path)
        os.startfile(os.path.join(path, songs[7]))

    # Handle time inquiry
    elif 'what is the time' in text:
        speak(f'The time is {datetime.datetime.now().strftime("%H:%M:%S")}')

    # Handle assistant introduction
    elif 'introduce yourself' in text:
        speak("Hello, I am Bishal's assistant, here to help anytime with your needs!")
    
    # Handle setting an alarm
    elif 'set an alarm for' in text:
        try:
            alarm_time_str = text.replace('set an alarm for', '').strip().upper().replace(".", "")
            # print(f"Alarm time string received: {alarm_time_str}")
            alarm_time = datetime.datetime.strptime(alarm_time_str, '%I:%M %p')
            speak(f'Setting an alarm for {alarm_time_str}')

            while True:
                now_time = datetime.datetime.now().strftime('%I:%M %p')
                if now_time >= alarm_time.strftime('%I:%M %p'):
                    speak('Time to wake up, sir!')
                    os.system('start D:/music/looperman-l-2693471-0206836-lil-tecca-tropical-steel-drums.wav')
                    break
                time.sleep(10)
        except ValueError as e:
            # print(f"Error parsing time: {e}")
            speak('Could not catch that. Please try again.')

    elif 'start a stopwatch' in text:
        speak('Stopwach has begun')
        begin = time.time()
        endTimer = capture_command()
        if 'stop' in text:
            end = time.time()
            elapsed = int(end - begin)
            speak(f"The time is {elapsed}, seconds")
            print({elapsed} + "seconds")

    elif 'set a reminder' in text or 'set another reminder' in text:
        try:
            setReminder(reminders)
            speak("Reminder successfully set!")
        except:
            speak('Could not catch that. Please try again.')
    
    elif 'show me all my reminders' in text:
        for remind in reminders:
            print(remind)
            speak(f'you have a reminder of {remind}')
        



def capture_command():
    global recognizer
    with sr.Microphone() as mic:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(mic, duration=0.5)
        audio = recognizer.listen(mic)
        try:
            # Recognize speech
            text = recognizer.recognize_google(audio)
            text = text.lower()
            print(f"Recognized: {text}")
            return text
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Could you please repeat?")
            return capture_command()


def command():
    while True:
        text = capture_command()
        
        # Execute recognized tasks
        tasks_do(text)

        # Check for a command to exit the loop
        if "exit the program" in text or "quit the program" in text:
            speak("Goodbye!")
            hour = int(datetime.datetime.now().hour)
            if hour >= 0 and hour < 12:
                speak("Have a good day sir!")
            elif hour >= 18 and hour < 24:
                speak('Good night sir!')
            else:
                speak('Have a good evening sir!')
            break


greeting()
command()
