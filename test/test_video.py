from core.video import get_video_info


video_path = "input/video.mp4"

info = get_video_info(video_path)

print(f"Resolution : {info['width']} x {info['height']}")
print(f"FPS        : {info['fps']:.2f}")
print(f"Frames     : {info['frame_count']}")
print(f"Duration   : {info['duration']:.2f} seconds")