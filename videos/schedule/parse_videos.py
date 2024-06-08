import cv2, os, glob
import numpy as np




def draw_text(img, text,
          font=cv2.FONT_HERSHEY_SIMPLEX,
          font_scale=1,
          font_thickness=2,
          text_color=(255, 255, 255),
          text_color_bg=(0, 0, 0),
          height=-1,
          width=-1,
          align='right'
          ):

    pad = 10
    img_copy = np.copy(img)
    text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
    text_w, text_h = text_size

    if align is 'right':
        x = width - text_w-1
        y = height - text_h-1
        pos = (x, y)
        cv2.rectangle(img_copy, (x-2*pad, y-2*pad), (x + text_w + 2*pad, y + text_h + 2*pad), text_color_bg, -1)
        img = (np.round(img.astype(np.float32)*0.2 + img_copy.astype(np.float32)*0.8)).astype(np.uint8)
        cv2.putText(img, text, (x - pad, y + text_h + font_scale - 1 - pad), font, font_scale, text_color, font_thickness)
    elif align is 'center':
        x = (width - text_w-1) //2
        y = height - text_h-1
        pos = (x, y)
        cv2.rectangle(img_copy, (x-pad, y-2*pad), (x + text_w + 2*pad, y + text_h + 2*pad), text_color_bg, -1)
        img = (np.round(img.astype(np.float32)*0.2 + img_copy.astype(np.float32)*0.8)).astype(np.uint8)
        cv2.putText(img, text, (x, y + text_h + font_scale - 1 - pad), font, font_scale, text_color, font_thickness)
    elif align is 'left':
        x = 0
        y = height - text_h-1
        pos = (x, y)
        cv2.rectangle(img_copy, (x, y-2*pad), (x + text_w + 2*pad, y + text_h + 2*pad), text_color_bg, -1)
        img = (np.round(img.astype(np.float32)*0.2 + img_copy.astype(np.float32)*0.8)).astype(np.uint8)
        cv2.putText(img, text, (x + pad, y + text_h + font_scale - 1 - pad), font, font_scale, text_color, font_thickness)

    return text_size, img


fps = 30.0
min_iter = 1
max_iter = 12
min_time = 0
# max_time = 1222
# video_name = 'bear_with_schedule'
max_time = 17332
video_name = 'bear_no_schedule'

cap_ours = cv2.VideoCapture(video_name+'.mp4')

# Define the codec and create VideoWriter object
counter = 0
while cap_ours.isOpened():
    ret_ours, frame_ours = cap_ours.read()
    if not ret_ours:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    counter+=1

cap_ours.release()
cv2.destroyAllWindows()

total_frames = counter

print(total_frames)

# Define the codec and create VideoWriter object
cap_ours = cv2.VideoCapture(video_name+'.mp4')
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(video_name+'_time.avi', fourcc, fps, (512,  288))
counter = 0
while cap_ours.isOpened():
    ret_ours, frame_ours = cap_ours.read()
    if not ret_ours:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    iter = int(np.round(min_iter + (max_iter - min_iter) * counter / total_frames))
    time = int(np.round(min_time + (max_time - min_time) * counter / total_frames))
    time_h = time // 3600
    time_m = (time % 3600) // 60
    time_s = time % 60

    if time_h != 0:
        show_time = str(time_h)+'h '+str(time_m).zfill(2)+'m'
    else:
        show_time = str(time_m)+'m '+str(time_s).zfill(2)+'s'
    
    
    
    frame_ours = cv2.resize(frame_ours, (512, 288), interpolation=cv2.INTER_AREA)

    # edit here
    _, frame_ours = draw_text(frame_ours, "Step: "+str(iter)+"k", height=288, width=512, align='left')
    _, frame_ours = draw_text(frame_ours, "Elapsed: "+show_time, height=288, width=512, align='right')

    out.write(frame_ours)
    counter+=1

cap_ours.release()
out.release()
cv2.destroyAllWindows()

os.system('ffmpeg -y -i '+video_name+'_time.avi -c:v libx264 -preset veryslow -crf 23 -pix_fmt yuv420p '+video_name+'_time.mp4')
            