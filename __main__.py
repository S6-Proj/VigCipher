from tkinter import *
from tkinter import ttk

root = Tk()
root.title("Vigenère Cipher")
root.resizable(False,False)
mainframe = ttk.Frame(root, padding="30 30 60 30")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

s = ttk.Style()
s.configure('.',font="Courier")

key = StringVar()
key_entry = ttk.Entry(mainframe, width=25, textvariable=key)
key_entry.grid(column=2, row=1)

plaintext = StringVar()
plaintext_entry = ttk.Entry(mainframe, width=25, textvariable=plaintext)
plaintext_entry.grid(column=2, row=2)

fixkey = ''
fixplaintext = ''
output = StringVar()

def errCheck(event=None):
    fixkey = key.get()
    fixplaintext = plaintext.get()
    fixkey = ''.join(fixkey.split())
    fixplaintext = ''.join(fixplaintext.split())
    if any(not c.isalpha() for c in fixkey) or any(not c.isalpha() for c in fixplaintext):
        return False
    else:
        return True
    
key_entry.bind('<KeyRelease>', errCheck)
plaintext_entry.bind('<KeyRelease>', errCheck)

def code(encode):
    fixkey = (key.get()).lower()
    fixplaintext = (plaintext.get()).lower()
    fixplaintext = ''.join(fixplaintext.split())

    if errCheck():
        x = [None] * len(fixplaintext) 
        z = [None] * len(fixkey)
        
        for i, char in enumerate(fixplaintext):
            if ord(char) != 32:
                x[i] = ord(char) - 97
            else:
                x[i] = 32

            i %= len(fixplaintext)

        for i, char in enumerate(fixkey):
            z[i] = ord(char) - 97

            i %= len(fixkey)
        
        for i in range(len(x)):
            if x[i] == 32 and z[i] != 0:
                x[i] = ' '
            else:
                if encode:
                    if i < len(z):
                        x[i] = chr(((x[i] + z[i])%26) + 97)
                    else: 
                        j = i % len(z)
                        x[i] = chr(((x[i] + z[j])%26) + 97)
                else:
                    if i < len(z):
                        x[i] = chr(((x[i] - z[i])%26) + 97)
                    else:
                        j = i % len(z)
                        x[i] = chr(((x[i] - z[j])%26) + 97)
        
        output.set(''.join(str(i) for i in x))
    else:
        output.set('Special Characters Detected')
        
def copyto_clip():
    if (output.get() == 'Special Characters Detected'):
        return 
    root.clipboard_clear()
    root.clipboard_append(output.get())
    root.update()

ttk.Label(mainframe, text="Key: ").grid(column=1, row=1)
ttk.Label(mainframe, text="Plaintext: ").grid(column=1, row=2)
ttk.Button(mainframe, text="Encode",width=10,command=lambda: code(True)).grid(column=2, row=3)
ttk.Button(mainframe, text="Decode",width=10,command=lambda: code(False)).grid(column=2, row=4)
ttk.Label(mainframe, textvariable=output).grid(column=2,row=5)
ttk.Button(mainframe,text = "Copy result to clipboard",command=copyto_clip).grid(column = 2,row=6)

root.mainloop()
