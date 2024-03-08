import threading
import customtkinter
from tkinter import filedialog
import pytube.exceptions
from pytube import YouTube
import os
import time

'''
For testing purposes: https://www.youtube.com/shorts/UfkCDKnI1CI
'''
# Constants
MY_FONT = ('comic sans ms', 13)
MY_DROPDOWN_FONT = ('comic sans ms', 9)
APP_DIMENSIONS = '320x420'
ICON_FILE = 'montage.ico'


# function that downloads the video
def download_video():
    try:
        save_location = save_to_entry.get()
        if not save_location:
            download_result.configure(text='Choose a destination folder', text_color='blue')
            return
        else:
            # disable ui before downloading video to prevent multiple downloads simultaneously
            disable_ui()
            yt = (YouTube(url_entry.get(), on_progress_callback=check_progress)
                  .streams.filter(progressive=True, file_extension='mp4').get_highest_resolution())
            yt.download(output_path=save_location)
            download_result.configure(text='Downloaded Successfully!', text_color='green')

    except pytube.exceptions.AgeRestrictedError:
        download_result.configure(text='Can not download Video: Age Restriction', text_color='red')
    except pytube.exceptions.VideoUnavailable:
        download_result.configure(text='Can not download Video: Video is unavailable', text_color='red')
    except pytube.exceptions.RegexMatchError:
        download_result.configure(text='Can not download Video: Video does not exist', text_color='red')
    except Exception as e:
        print(f'Unable to download video: {e}')
        download_result.configure(text='Can not download this video :(', text_color='red')
    finally:
        # enable the ui buttons
        enable_ui()
        reset()


# function that downloads the video
def download_audio():
    try:
        save_location = save_to_entry.get()
        if not save_location:
            download_result.configure(text='Choose a destination folder', text_color='blue')
            return
        else:
            # disable ui before downloading audio process to prevent multiple downloads simultaneously
            disable_ui()
            yt = (YouTube(url_entry.get(), on_progress_callback=check_progress)
                  .streams.filter(file_extension='mp4').get_audio_only())
            yt.download(output_path=save_location)
            download_result.configure(text='Downloaded Successfully!', text_color='green')

    except pytube.exceptions.AgeRestrictedError:
        download_result.configure(text='Can not download Audio: Age Restriction', text_color='red')
    except pytube.exceptions.VideoUnavailable:
        download_result.configure(text='Can not download Audio: Video is unavailable', text_color='red')
    except pytube.exceptions.RegexMatchError:
        download_result.configure(text='Can not download Audio: Video does not exist', text_color='red')
    except Exception as e:
        print(f'Unable to download video: {e}')
        download_result.configure(text='Can not download Audio :(', text_color='red')
    finally:
        # enable the ui buttons
        enable_ui()
        reset()


# download video in a separate thread. pytube has block operations that will run in the background. if they run together
# with the gui mainloop, the app will start freezing up. So another thread is used for downloading the video
def download_video_thread():
    threading.Thread(target=download_video).start()


# download audio in a separate thread. pytube has block operations that will run in the background. if they run together
# with the gui mainloop, the app will start freezing up. So another thread is used for downloading the audio
def download_audio_thread():
    threading.Thread(target=download_audio).start()


# after each download, we need to reset the progress_bar, progress_label and download_result
def reset():
    time.sleep(4)
    download_result.configure(text='')
    progress_bar.set(0)
    progress_label.configure(text='0%')
    enable_ui()


# function that opens up a filedialog in order to select a folder to download the video into
def choose_folder():
    folder = filedialog.askdirectory()
    if not folder is None:
        # delete chars starting at index 0, till 'end'. 'end' is a special index that represents the end of Entry widget
        save_to_entry.delete(0, 'end')
        save_to_entry.insert(0, folder)
        return folder
    else:
        return None


# function that updates the progress bar, and calculates how many bytes have been downloaded
def check_progress(stream, chunk, bytes_remaining):
    video_size = stream.filesize
    bytes_downloaded = video_size - bytes_remaining
    percentage_downloaded = int((bytes_downloaded / video_size) * 100)
    # print(percentage_downloaded)
    progress_label.configure(text=str(percentage_downloaded) + '%')
    progress_label.update()
    progress_bar.set(value=(percentage_downloaded / 100))
    progress_bar.update()


# function that disables ui buttons
def disable_ui():
    download_btn.configure(state='disabled')
    download_audio_btn.configure(state='disabled')
    save_to_btn.configure(state='disabled')
    light_dark_optionmenu.configure(state='disabled')
    url_entry.configure(state='disabled')
    save_to_entry.configure(state='disabled')


# function that enables ui buttons
def enable_ui():
    download_btn.configure(state='normal')
    download_audio_btn.configure(state='normal')
    save_to_btn.configure(state='normal')
    light_dark_optionmenu.configure(state='normal')
    url_entry.configure(state='normal')
    save_to_entry.configure(state='normal')


# function that enables light mode
def light_on():
    customtkinter.set_appearance_mode('light')
    light_dark_optionmenu.configure(values=['Dark'])


# function that enables dark mode
def light_off():
    customtkinter.set_appearance_mode('dark')
    light_dark_optionmenu.configure(values=['Light'])


# choice is a predefined parameter. it gives us light_dark_optionmenu.get()
# choice in the optionmenu_callback function will receive the value selected in the CTkOptionMenu
def optionmenu_callback(choice):
    if choice == 'Light':
        light_on()
    else:
        light_off()


# create the main app window: specify width and height, theme and make it non-resizable
customtkinter.set_default_color_theme('dark-blue')
customtkinter.set_appearance_mode('dark')
app = customtkinter.CTk()
app.geometry(APP_DIMENSIONS)
app.title('Stellar Stream')
app.resizable(False, False)
# This makes the icon works on any device. All you have to do is to save the icon into the same dir
icon_path = os.path.join(os.path.dirname(__file__), ICON_FILE)
# change the app icon
app.iconbitmap(icon_path)

# Option Menu to switch between dark and light modes
light_dark_optionmenu = customtkinter.CTkOptionMenu(app, values=['Dark', 'Light'], width=20, corner_radius=11,
                                                    font=MY_DROPDOWN_FONT, dropdown_font=MY_DROPDOWN_FONT,
                                                    command=optionmenu_callback, dropdown_fg_color='dodgerblue4',
                                                    dropdown_text_color='white')
light_dark_optionmenu.pack(anchor='nw', padx=10, pady=10)

# create a label that says: Insert Video URL
insert_link_label = customtkinter.CTkLabel(app, text='Paste Video URL', font=MY_FONT)
insert_link_label.pack(padx=10, pady=10)

# create an entry so that the user can paste the video url
url_entry = customtkinter.CTkEntry(app, width=285, height=35, placeholder_text='https://www.youtube.com/@LogicTinkerer',
                                   corner_radius=12, font=MY_FONT)
url_entry.pack(padx=10, pady=5)

# frame to hold the save_to_btn and save_to_entry
save_to_frame = customtkinter.CTkFrame(app, width=285, height=60, fg_color='transparent')
save_to_frame.pack(pady=10)

# create an entry for the destination folder
save_to_entry = customtkinter.CTkEntry(save_to_frame, width=210, height=35,
                                       placeholder_text='C:/Users/logictinkerer/Videos', corner_radius=12,
                                       font=MY_FONT)
save_to_entry.pack(side='left', padx=5)

# create a button to choose the destination folder
save_to_btn = customtkinter.CTkButton(save_to_frame, text='Save To', width=65, command=choose_folder, font=MY_FONT)
save_to_btn.pack(side='left')

# text to show if video has been downloaded
download_result = customtkinter.CTkLabel(app, text='')
download_result.pack(padx=10, pady=35)

# create a label that says: Insert Video URL
download_label = customtkinter.CTkLabel(app, text='Download', font=MY_FONT)
download_label.pack(padx=10, pady=0)

# downloading Frame
download_frame = customtkinter.CTkFrame(app, width=285, height=30, fg_color='transparent')
download_frame.pack(pady=0)

# create a button to download the video
download_audio_btn = customtkinter.CTkButton(download_frame, text='Audio', width=65, command=download_audio_thread,
                                             font=MY_FONT)
download_audio_btn.pack(side='right', padx=0, pady=10)

# create a button to download the video
download_btn = customtkinter.CTkButton(download_frame, text='Video', width=65, command=download_video_thread,
                                       font=MY_FONT)
download_btn.pack(side='right', padx=4, pady=10)

# progress frame
progress_frame = customtkinter.CTkFrame(app, width=320, height=50, fg_color='transparent')
progress_frame.pack(pady=10)

# progress label
progress_label = customtkinter.CTkLabel(progress_frame, text='0%', font=('comic sans ms', 11))
progress_label.pack(side='right')

# progress bar
progress_bar = customtkinter.CTkProgressBar(progress_frame, width=175, mode='determinate')
progress_bar.set(0)
progress_bar.pack(padx=10, pady=11)

# start the application
app.mainloop()
