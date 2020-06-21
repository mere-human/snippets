# YT Playlist Dumper

This console app gets your YouTube playlists and items in them and dumps it in JSON format. This helps you to track down deleted videos.

## Details

Run the sample using the following command:

`python playlists.py`

The sample will attempt to open a new window or tab in your default browser. If this fails, copy the URL from the console and manually open it in your browser.

If you are not already logged into your Google account, you will be prompted to log in. If you are logged into multiple Google accounts, you will be asked to select one account to use for the authorization.

Click the Accept button.
The sample will proceed automatically, and you may close the window/tab.

Authorization information is stored on the file system, so subsequent executions will not prompt for authorization.
