

## Screencasting

ffmpeg for webcam capture

```bash
# records for 10 seconds, TODO: record until exit
ffmpeg -f v4l2 -input_format mjpeg -framerate 30 -video_size 1920x1080 -i /dev/video0 -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -t 10 output.mp4
```

ffmpeg for audio capture

```bash
ffmpeg -f alsa -i default -c:a libmp3lame -b:a 192k -t 10 audio_recording.mp3
```

ffmpeg for screen capture

```bash
ffmpeg -f x11grab -video_size 1920x1080 -framerate 30 -i $DISPLAY -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -t 10 screen_recording.mp4
```

Interlay screen + webcam + audio

```bash
ffmpeg \
  -f x11grab -video_size 1920x1080 -framerate 30 -i $DISPLAY \
  -thread_queue_size 4096 -f v4l2 -input_format mjpeg -framerate 30 -video_size 640x480 -i /dev/video0 \
  -thread_queue_size 4096 -f alsa -i default \
  -filter_complex " \
    [0:v]setpts=PTS-STARTPTS[screen]; \
    [1:v]setpts=PTS-STARTPTS,scale=240x180,pad=250:190:5:5:yellow[cam]; \
    [screen][cam]overlay=main_w-overlay_w-30:main_h-overlay_h-30[outv] \
  " \
  -map "[outv]" -map 2:a \
  -c:v libx264 -preset ultrafast -tune zerolatency -crf 23 -pix_fmt yuv420p \
  -c:a aac -b:a 192k \
  -vsync 1 -max_delay 0 -bufsize 3000k \
  -t 10 \
  combined_recording.mp4
```

add to snippets
shortcut to start/stop recording


