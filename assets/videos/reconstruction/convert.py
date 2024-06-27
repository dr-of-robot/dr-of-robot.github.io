import os
import cv2
import subprocess

def convert_videos_to_web_friendly_format():
    # Get the list of all files in the current directory
    files = os.listdir('.')
    
    # Filter out MP4 files
    mp4_files = [f for f in files if f.endswith('.mp4')]
    
    for mp4_file in mp4_files:
        try:
            # Define the output file name
            output_file = os.path.splitext(mp4_file)[0] + '_web.mp4'
            
            # Open the video file using cv2
            cap = cv2.VideoCapture(mp4_file)
            
            # Get video properties
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            # Define the codec and create VideoWriter object
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))
            
            while cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    # Write the frame to the output file
                    out.write(frame)
                else:
                    break
            
            # Release everything if job is finished
            cap.release()
            out.release()
            
            # Use ffmpeg to ensure the audio is converted correctly
            command = f"ffmpeg -i {output_file} -c:v libx264 -c:a aac -strict experimental -b:a 192k -shortest temp.mp4"
            subprocess.call(command, shell=True)
            
            # Rename temp.mp4 to the final output file name
            os.rename('temp.mp4', output_file)
            
            print(f"Converted {mp4_file} to {output_file}")
        except Exception as e:
            print(f"Error converting {mp4_file}: {e}")

if __name__ == "__main__":
    convert_videos_to_web_friendly_format()

