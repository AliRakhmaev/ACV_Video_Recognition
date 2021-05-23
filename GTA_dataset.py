import os
import argparse
from pathlib import Path
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import *
from shutil import copyfile

import annotations
import CrimeVideo

ap = argparse.ArgumentParser()
ap.add_argument("-in", "--input_directory",
                help="path to directory to explore for videos", default="E:\DS project\Datasets\GTA_Dataset")
ap.add_argument("-out", "--output_directory",
                help="path to directory to save the fragments", default="E:\DS project\Datasets\GTA_videos_directory_resized")
ap.add_argument("-out_anno", "--output_annotations",
                help="path to directory to save the annotation file for Gluon framework", default="E:\DS project\Datasets\GTA_videos_annotations_resized")
args = ap.parse_args()

# Specify the path where to locate the fragments
directory = os.path.abspath(args.output_directory)
video_annotations = []

if not os.path.exists(directory):
    os.makedirs(directory)
os.chdir(directory)

# Specify the path to the directory with videos. The script will go through all the inner directories and will
# capture paths to the videos. IT MEANS ALL THE VIDEOS!
# NOTE: For now the crawler restricted to mp4 format.
for dirpath, dirnames, files in os.walk(os.path.abspath(args.input_directory)):
    for file in files:
        if file.endswith(".mp4"):
            label = os.path.basename(os.path.normpath((Path(os.path.join(dirpath, file)).parent.absolute()).parent.absolute()))
            video_number = os.path.basename(os.path.normpath((Path(os.path.join(dirpath, file)).parent.absolute())))

            original_video = VideoFileClip(os.path.join(dirpath, file))
            resized_video = original_video.resize(0.25)  # width and heigth multiplied by 0.25

            # copyfile(os.path.join(dirpath, file), os.path.join(directory,label + "_" + video_number + "_" + file))
            resized_video.write_videofile(label + "_" + video_number + "_" + file, threads=12)


            video_annotations.append(CrimeVideo.CrimeVideo(label + "_" + video_number + "_" + file,label, [(-1, -1)]))

annotations.write_annotations_for_gluon(video_annotations, args.output_annotations)

print("Total videos: " + str(len(video_annotations)))
