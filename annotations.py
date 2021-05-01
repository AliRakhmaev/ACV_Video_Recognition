import CrimeVideo
import os


def read_annotation(file_name):
    videos = {}

    with open(file_name, 'r', encoding='utf-8') as g:
        for line in g.read().splitlines():
            words = [word for word in line.split('  ') if len(word) > 0]

            if len(words) == 0:
                continue

            video_name = words[0]
            video_label = words[1]
            incidents = []

            for i in range(2, len(words), 2):
                start_of_crime = int(words[i])
                end_of_crime = int(words[i + 1])

                if start_of_crime != -1:
                    incidents.append((start_of_crime, end_of_crime))

            videos[video_name] = CrimeVideo.CrimeVideo(video_name, video_label, incidents)
    return videos

def write_annotations_for_gluon(clips, path):
    label_to_number = {}

    if not os.path.exists(path):
        os.makedirs(path)

    with open(os.path.join(path, "gluon_annotations.txt"), 'w', encoding='utf-8') as g:
        for clip in clips:
            if clip.label not in label_to_number:
                if len(label_to_number.values()) == 0:
                    label_to_number[clip.label] = 0
                else:
                    label_to_number[clip.label] = max(label_to_number.values()) + 1
            g.write(clip.path + " 1 " + str(label_to_number[clip.label]) + "\n")





# results = read_annotation("Temporal_Anomaly_Annotation_for_Training_Videos.txt")
# results = read_annotation("Temporal_Anomaly_Annotation_for_Testing_Videos.txt")
