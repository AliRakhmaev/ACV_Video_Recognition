import os
import argparse
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import *

import annotations
import CrimeVideo

ap = argparse.ArgumentParser()
ap.add_argument("-in", "--input_directory",
                help="path to directory to explore for videos", default="E:\DS project\Datasets\Real_UCF_Dataset")
ap.add_argument("-annot", "--annotations",
                help="path to annotation file", default="Temporal_Anomaly_Annotation_for_Training_Videos.txt")
ap.add_argument("-out", "--output_directory",
                help="path to directory to save the fragments", default="E:\DS project\Datasets\Testing_directory_train")
ap.add_argument("-out_anno", "--output_annotations",
                help="path to directory to save the annotation file for Gluon framework", default="E:\DS project\Datasets\Testing_annotations_train")
args = ap.parse_args()

video_annotations = annotations.read_annotation(args.annotations)

# Specify the path where to locate the fragments
directory = os.path.abspath(args.output_directory)
video_paths_with_names = []

# Specify the path to the directory with videos. The script will go through all the inner directories and will
# capture paths to the videos. IT MEANS ALL THE VIDEOS!
# NOTE: For now the crawler restricted to mp4 format.
for dirpath, dirnames, files in os.walk(os.path.abspath(args.input_directory)):
    for file in files:
        if file.endswith(".mp4") and file in video_annotations:
            video_paths_with_names.append((os.path.join(dirpath, file), file))

print("Total videos: " + str(len(video_paths_with_names)))

# Change the current directory
# to specified directory
if not os.path.exists(directory):
    os.makedirs(directory)
os.chdir(directory)

# Annotation objects for new generated videos
generated_video_annotations = []

# Due to configuration issue of moviepy while handling of audio files error we have to delete garbage audio files manually
additional_audio_files_to_delete = []

for video_path, video_name in video_paths_with_names:
    original_video = VideoFileClip(video_path)
    fps = original_video.fps
# Some audiofiles in videos are corrupted and arise the errors in MoviePy.
# This is if such an expection occurs the program ignore writing teh audio from original video.
    for count, (start, end) in enumerate(video_annotations[video_name].incidents):
        try:
            try:
                video_clip = original_video.subclip(start / fps, end / fps)
                video_clip.write_videofile(video_name[:-4] + "_incident_" + str(count) + ".mp4", threads=12)
            except AttributeError:
                additional_audio_files_to_delete.append(os.path.join(os.getcwd(), video_name[:-4] + "_incident_" + str(count) + "TEMP_MPY_wvf_snd.mp3"))
                video_clip = original_video.subclip(start / fps, end / fps)
                video_clip.write_videofile(video_name[:-4] + "_incident_" + str(count) + ".mp4", threads=12, audio=False)

            generated_video_annotations.append(CrimeVideo.CrimeVideo(video_name[:-4] + "_incident_" + str(count) + ".mp4", video_annotations[video_name].label, [(start, end)]))

        except RuntimeError:
            continue

for audio_path in additional_audio_files_to_delete:
    os.remove(audio_path)

annotations.write_annotations_for_gluon(generated_video_annotations, args.output_annotations)
