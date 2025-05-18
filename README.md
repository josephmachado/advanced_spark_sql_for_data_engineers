

## Screencasting

ffmpeg for webcam capture

```bash
# records for 10 seconds, TODO: record until exit
ffmpeg -f v4l2 -input_format mjpeg -framerate 30 -video_size 1920x1080 -i /dev/video0 -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -t 10 output.mp4
```

ffmpeg for audio capture
