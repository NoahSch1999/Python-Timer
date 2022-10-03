import PySimpleGUI as sg
import time
import simpleaudio as sa

tHours = 0
tMinutes = 0
tSeconds = 0
myWindow = 0

## alarm name / filepath and read/write from/to file to save the alarm directory

def SaveAlarmSettings(browsePath):
    file = open("DoNotTouch!/AlarmSettings.txt", "w")
    file.write(browsePath)
    file.close()

def CalculateTime(hours, minutes, seconds): # Method that transforms hours and minutes into seconds and calculates a total amount of seconds
    totalSeconds = (int(hours) * 3600) + (int(minutes) * 60) + int(seconds)
    return totalSeconds

def main():
    statusBarCD = [[ sg.Text(text="0", justification = "c", font = ("Trebuchet MS Fet", 30), text_color = "black", background_color = "white", key="cdText") ]]
    buttonStart = [[sg.Button("Start Timer", button_color="red", font=("Trebuchet MS Fet", 10), tooltip="Pressing this starts the timer", border_width = 5, mouseover_colors =("red", "pink"), size=(15, 2))]]
    buttonFile = sg.FileBrowse( button_text="Alarm Selection", key='sFilePath')
    textFile = sg.Text(font = ("Trebuchet MS Fet", 12), text_color = "black", background_color = "white")

    colh = [ [sg.Text(text = "Hours: ", key='hrs', background_color="LightBlue", font = ("Trebuchet MS Fet", 15), text_color="black")],  [sg.Input(background_color = "white", border_width = 4, key='iHours' )] ]
    colm = [ [sg.Text(text = "Minutes: ", key='mins', background_color="LightBlue", font = ("Trebuchet MS Fet", 15), text_color="black")],  [sg.Input( background_color = "white", border_width = 4, key='iMins'  )] ]
    cols = [ [sg.Text(text = "Seconds: ", key='sec', background_color="LightBlue", font = ("Trebuchet MS Fet", 15), text_color="black")],  [sg.Input( background_color = "white", border_width = 4, key='iSecs' )] ]
   
    textAlarm = sg.Text(text="Alarm Repeats:", background_color="LightBlue", font = ("Trebuchet MS Fet", 14), text_color="black")
    inputAlarm = sg.Input( background_color = "white", size=(3,1), justification="c", border_width = 4, key='sRepeats'  )


    layout = [
    [statusBarCD],
    [sg.Column(colh, background_color="LightBlue")], 
    [sg.Column(colm, background_color="LightBlue")], 
    [sg.Column(cols, background_color="LightBlue")],
    [textAlarm, inputAlarm],
    [buttonStart],
    [buttonFile]
    ]

    myWindow = sg.Window("aZero Timer", layout, margins=(10, 10), background_color = "LightBlue")
    

    file = open("DoNotTouch!/AlarmSettings.txt")
    loadedAlarm = file.readline()
    file.close()

    myWindow.finalize()
    while 1:

        tHours, tMinutes, tSeconds, repeats = 0, 0, 0, 0
        
        event, values = myWindow.read()

        if event == sg.WIN_CLOSED:
            break

        if event == "Start Timer":
            
            browsePath = values['sFilePath']
            if browsePath == "":
                browsePath = loadedAlarm
            else:
                SaveAlarmSettings(browsePath)
                
            tHours = values['iHours']
            if tHours == "":
                tHours = 0

            tMinutes = values['iMins']
            if tMinutes == "":
                tMinutes = 0

            tSeconds = values['iSecs']
            if tSeconds == "":
                tSeconds = 0

            repeats = values['sRepeats']
            if repeats == "":
                repeats = 1
                
            cd = CalculateTime(tHours, tMinutes, tSeconds)
            
            start = time.time()
            
            while 1:

                current = time.time() - start

                myWindow.finalize()
                myWindow['cdText'].update( str(int((cd - current) / 3600)) + " : " + str(int(((cd - current) % 3600) / 60)) + " : " + str(int((cd - current) % 60)) )

                if current > cd:

                    myWindow['cdText'].update("Done!")
                    myWindow.finalize()
                    try:
                        wavFile = sa.WaveObject.from_wave_file(browsePath)
                    except:
                        wavFile = sa.WaveObject.from_wave_file("DoNotTouch!/duckDefault.wav")

                    for x in range(int(repeats)):
                        playObj = wavFile.play()
                        playObj.wait_done()
                    
                    myWindow['cdText'].update("0 : 0 : 0")
                    myWindow['sRepeats'].update("")
                    myWindow['iHours'].update("")
                    myWindow['iMins'].update("")
                    myWindow['iSecs'].update("")
                    
                    break
    
    myWindow.close()

main()

