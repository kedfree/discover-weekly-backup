## Site can be accessed [here](http://kfmoon.pythonanywhere.com/).

### Uses Spotify's API to save a user's Discover Weekly Playlist.
Simple website allowing for a user to login into Spotify to allow permissions. After permissions have been accepted, the 
program will search through the user's playlist to find the Discover Weekly playlist. A new playlist called "Saved Discover Weekly" 
will be created with the user's Discover Weekly songs. 

Only creates one "Saved Discover Weekly" to prevent clutter and doesn't add duplicate songs no matter the times run.


## Site Usage:
- Follow login instructions, allowing permissions on the spotify page.
- Will be brought to a success page if successfull

*Make sure you have the Discover Weekly Playlist added to your library*

## Recreating on local system:
- Can be run locally using flask
- Must first create an **.env** file following example file
- Client ID and Secret can be created @ https://developer.spotify.com/dashboard/
- After creating **.env** file, proceed to running **weekly.py**
