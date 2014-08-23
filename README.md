vidcut
======

A Python script to cut a video file (MP4, AVI, WMV, MOV, FLV, MPG) or a collection of video files inside a directory. This script requires the path of [ffmpeg](https://www.ffmpeg.org/) set in the PATH environment variable.

## Syntax
The Script can take 4 arguments of which 2 are optional.

1. A Video file or the directory containing video files.
2. The time in hh:mm:ss format at which the video is cut.
3. (optional) Required cut piece - `left` or `right`. If no value is given both left and right cut pieces are generated.
4. (optional) The direction (*start to end* or *end to start*) the cut time is measured. Value `rev` takes the cut time as from the end. If *rev* is not mentioned, the cut time is assumed to be from the start.

### Example:
- Generate left and right pieces from cutting at 5 min, 35 sec from the start
		vidcut.py test.mp4 00:05:35
	
- Generate only the right side piece for all the videos in the **videos** *directory/folder*
		vidcut.py videos 00:05:35 right

- Generate only the left piece after cutting at 5 min, 35 sec before the *end of the video* (without knowing the full length of the videos)
		vidcut.py videos 00:05:35 left rev
	
- Generate the first 10 seconds and the last 10 seconds
		vidcut.py test.mp4 00:00:10 left
		vidcut.py test.mp4 00:00:10 right rev
		


