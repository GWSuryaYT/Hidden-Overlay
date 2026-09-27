import ctypes as ct
import ctypes.wintypes as w
import tkinter as tk
from gemini import response
import speech_recognition as sr
import threading
from gemini import previousmsg
from gemini import context
from gemini import both


# ==============================================================================
# 1. WINDOWS API CONFIGURATION (Hide the screen from captures)
# ==============================================================================


WDA_EXCLUDEFROMCAPTURE = 0x00000011  # Keeps window invisible to captures

def boolcheck(result, func, args):
    if not result:
        raise ct.WinError(ct.get_last_error())

# Load the user32 library safely with strict error handling
user32 = ct.WinDLL('user32', use_last_error=True)

SetWindowDisplayAffinity = user32.SetWindowDisplayAffinity
SetWindowDisplayAffinity.argtypes = w.HWND, w.DWORD
SetWindowDisplayAffinity.restype = w.BOOL
SetWindowDisplayAffinity.errcheck = boolcheck

GetForegroundWindow = user32.GetForegroundWindow
GetForegroundWindow.argtypes = ()
GetForegroundWindow.restype = w.HWND








# ==============================================================================
# 2. AFFINITY FUNCTION
# ==============================================================================


def apply_protection():
    # Force focus so ur and my window is guaranteed to be the active foreground window
    root.focus_force()
    root.update()
    
    # Grab the active native window handle
    h = GetForegroundWindow()
    
    # Apply the working affinity block automatically
    SetWindowDisplayAffinity(h, WDA_EXCLUDEFROMCAPTURE)
    print(f"Successfully protected window handle: {hex(h)}")







# ==============================================================================
# Functions:
# ==============================================================================

saved_previous_msgs = []
def send_msg():
    msg = input_entry.get()
    reply = response(msg, saved_previous_msgs)

    #saving the mesgs:
    if previousmsg:
        data = {"prompt": msg, "Gemini_reply": reply} 
        saved_previous_msgs.append(data)

    # 1. Allow program to edit the text
    paragraph_text.config(state="normal")  
    # Clear old text and insert new response
    paragraph_text.delete("1.0", tk.END)

    paragraph_text.insert(tk.END, reply + "\n")
    input_entry.delete(0, tk.END)
    
    # Resize the entire screen to fit the new text length
    resize_window_to_fit()

    # 2. Prevent user from editing the text
    paragraph_text.config(state="disabled") 





# Helper function to safely update UI from the background thread
def update_status(message):

    #first we need to enable the editing
    paragraph_text.config(state="normal")
    paragraph_text.delete("1.0", tk.END)
    paragraph_text.insert(tk.END, message + "\n")
    
    # Resize the entire screen to fit the new text length
    resize_window_to_fit()

    #now again disable it
    paragraph_text.config(state="disabled")




#helper function that let the ui change size:
def resize_window_to_fit():
    # Force tkinter to calculate the current layout size
    root.update_idletasks()
    
    # Get the number of visual text lines
    num_lines = int(paragraph_text.index('end-1c').split('.'))
    
    # Calculate new window height: 
    # (Number of lines * line height in pixels) + extra padding for input fields/buttons
    line_height = 20  # Approximate pixel height for Helvetica 14
    padding = 120     # Pixels reserved for margins and bottom buttons

    # Enforce a minimum window height (e.g., 300px) so it looks good when empty
    calculated_height = (num_lines * line_height) + padding

    #setting a max boundaries
    min_height = 500
    max_height = 900


    new_height = max(min_height, min(calculated_height, max_height))
    
    # Apply the new geometry to the entire application window (width stays 700)
    root.geometry(f"700x{new_height}")




def speech_thread_worker():

    #change this value to the index value of your mic for that use the mic-finder.py
    mic_index = 2

    r = sr.Recognizer()

    r.pause_threshold = 1.5

    try:
        with sr.Microphone(device_index=mic_index) as source:
            update_status("Adjusting for ambient noice... Please wait.")
            r.adjust_for_ambient_noise(source=source, duration=2)

        
            update_status('🎤Listening...')
            audio_text = r.listen(source=source)

            update_status("Processing audio...")
            # Transcribe the audio data to text string
            recognized_text = r.recognize_google(audio_text)
            

            #put the text on the send option so u can check and send it
            input_entry.delete(0, tk.END)
            input_entry.insert(0, recognized_text)
            update_status(f"Recognized: {recognized_text}")

    except sr.UnknownValueError:
        update_status("Sorry, I didn't catch that.")
    except sr.RequestError:
        update_status("Could not request results; check your internet connection.")
    except Exception as e:
        update_status(f"An error occurred: {str(e)}")




def recognizer():
    #here we will use threading lib so our code run on background that wont effect our main gui anymore
    threading.Thread(target=speech_thread_worker, daemon=True).start()








# ==============================================================================
# 3. INTERFACE & STYLING
# ==============================================================================


root = tk.Tk()
root.geometry("700x500")
root.configure(bg="#030101")
root.title('The world is good')

root.attributes("-alpha", 0.7)

# Optional: To make it borderless like a real overlay, uncomment the next line:
# root.overrideredirect(True)

# widgets:
# Set up the text widget with your custom colors
paragraph_text = tk.Text(root, fg="#FFFFFF", bg="#000000", font=("Helvetica", 14), bd=0,width= 100,height=1 ,state="disabled", yscrollcommand=None)
paragraph_text.pack(side=tk.TOP, pady=10, fill=tk.BOTH, expand=True)

# 2. The Bottom Frame (holds all my control buttons and entry fields safely)
bottom_frame = tk.Frame(root, bg="#030101")
bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

# 3. other input items
input_entry = tk.Entry(bottom_frame, width=50, bg="white", font=("Helvetica", 14), bd=0)
input_entry.pack(side=tk.LEFT, padx=10, pady=5)

send_btn = tk.Button(bottom_frame, text="Send", command=send_msg, fg="#FFFFFF", bg="#6EA1FF")
send_btn.pack(side=tk.LEFT, pady=5, padx=10)

mic_btn = tk.Button(bottom_frame, text="Mic", command=recognizer, fg="#FFFFFF", bg="#0059ff")
mic_btn.pack(side=tk.LEFT, pady=5, padx=10)







# ==============================================================================
# 4. EXECUTION TIMING CONTROL
# ==============================================================================


# Instead of a button, wait 150ms for Tkinter to render, then run protection
# root.after(150, apply_protection)

root.mainloop()