# kookcast

## overview
You may want to go surfing, but sometimes mother nature doesn't oblige. Surfable conditions arise only when a number of factors such as swell height, the direciton of the wind, and the tide all cooperate with you. 

With the weather constantly changing – how do you keep track of all of the different variables and know when it's time to hit the beach?

"kookcast" is a personal project of mine that helps answer that question. A portmanteau of the slang for a beginner surfer ("kook") and "forecast", the kookcast is a Python application that retrieves, aggregates, and delivers (via email) relevant weather data to the hopeful surfer.

While the primary value of the kookcast is the automatic daily email that it sends, other functionality in this repo includes the ongoing appending of weather data to a file that can be used for historical analysis with tools such as Jupyter Notebook. 

## files in this repo
*Note: I have renamed my files to help communicate the intent of the code written within each. This has been done to aid scannability of the repo. Actual usage of the kookcast would require addressing some file name dependencies within the code.*

### generateForecastandSendemail.py


### plist
the .plist filetype for automating the execution fo the kookcast should be installed to: Macintosh HD/Library/LaunchAgents/filename.plist
