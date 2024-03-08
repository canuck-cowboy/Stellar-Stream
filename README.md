![image](https://github.com/AbedIronman/Stellar-Stream/assets/57958425/442c8daa-b642-4f51-bbbe-8070054d658d)

# Stellar Stream

Stellar Stream is a simple desktop application built using Python (CustomTkinter) for downloading videos and audio from YouTube.

## Features

- Download videos or audio from YouTube by pasting the video URL
- Choose a destination folder to save the downloaded files
- Option to switch between dark and light modes for the user interface
- Visual progress indication during the download process
- Once the video starts downloading, the UI becomes disabled in order to prevent multiple downloads at the same moment

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/AbedIronman/stellar-stream.git
    ```

2. Install the required dependencies:

    ```bash
    pip install pytube customtkinter
    ```

3. Run the application:

    ```bash
    python app.py
    ```

## Usage

1. Paste the YouTube video URL into the provided field.
2. Choose a destination folder to save the downloaded files.
3. Click on the "Video" or "Audio" button to start the download process.
4. Monitor the progress using the progress bar and percentage indicator.
5. Once the download is complete, the status will be displayed.

## Dependencies

- pytube
- customtkinter

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

