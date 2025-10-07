Converting to CPX compatible .wav with ffmpeg

`ffmpeg -i INPUT.wav -ar 22050 -ac 1 OUTPUT.wav`

Where `INPUT.wav` and `OUTPUT.wav` should be changed to your input file and output filenames.
This works to convert wav's.  Might need some additional code to do other conversions.
