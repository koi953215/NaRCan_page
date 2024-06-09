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

# task = 'styletransfer'
# scenes = ['bear', 'boat', 'hot-air-ballon', 'overlook-the-ocean', 'shark-ocean']
# other_methods = ['input', 'hash', 'codef', 'medm']

def parse_one_task(task, scenes, other_methods):
    for scene in scenes:
        for other_method in other_methods:
            other_video_path = './'+task+'/'+scene+'_'+other_method+'.mp4'

            if os.path.isfile(other_video_path):
                H = 432
                W = 768
                fps = 20.0
                ours_video_path = './'+task+'/'+scene+'_ours.mp4'
                cap_ours = cv2.VideoCapture(ours_video_path)
                
                cap_other = cv2.VideoCapture(other_video_path)
                
                # Define the codec and create VideoWriter object
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                out = cv2.VideoWriter(task+'_'+scene+'_'+other_method+'_vs_ours_video.avi', fourcc, fps, (2*W,  H))
                while cap_ours.isOpened() and cap_other.isOpened():
                    ret_ours, frame_ours = cap_ours.read()
                    ret_other, frame_other = cap_other.read()
                    if not ret_ours or not ret_other:
                        print("Can't receive frame (stream end?). Exiting ...")
                        break
                    
                    if frame_ours.shape[0] != 432 or frame_ours.shape[1] != 768:
                        frame_ours = cv2.resize(frame_ours, (768, 432), interpolation=cv2.INTER_AREA)
                    if frame_other.shape[0] != 432 or frame_other.shape[1] != 768:
                        frame_other = cv2.resize(frame_other, (768, 432), interpolation=cv2.INTER_AREA)
                    
                    
                    

                
                    # edit here
                    _, frame_ours = draw_text(frame_ours, "Ours", height=H, width=W, align='right')
                    if other_method is 'hash':
                        _, frame_other = draw_text(frame_other, "Hashing-nvd", height=H, width=W, align='left')
                    if other_method is 'input':
                        _, frame_other = draw_text(frame_other, "Input", height=H, width=W, align='left')
                    if other_method is 'codef':
                        _, frame_other = draw_text(frame_other, "CoDeF", height=H, width=W, align='left')
                    if other_method is 'medm':
                        _, frame_other = draw_text(frame_other, "MeDM", height=H, width=W, align='left')
                
                    frame = cv2.hconcat([frame_other, frame_ours]) 
                
                    out.write(frame)
                
                cap_ours.release()
                cap_other.release()
                out.release()
                cv2.destroyAllWindows()

                os.system('ffmpeg -y -i '+task+'_'+scene+'_'+other_method+'_vs_ours_video.avi -c:v libx264 -preset veryslow -crf 23 -pix_fmt yuv420p '+task+'_'+scene+'_'+other_method+'_vs_ours_video.mp4')
            else:
                ## handling medm for handwrite
                H = 432
                W = 768
                fps = 20.0
                ours_video_path = './'+task+'/'+scene+'_ours.mp4'
                cap_ours = cv2.VideoCapture(ours_video_path)
                
                # Define the codec and create VideoWriter object
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                out = cv2.VideoWriter(task+'_'+scene+'_'+other_method+'_vs_ours_video.avi', fourcc, fps, (2*W,  H))
                while cap_ours.isOpened():
                    ret_ours, frame_ours = cap_ours.read()
                    if not ret_ours:
                        print("Can't receive frame (stream end?). Exiting ...")
                        break
                    
                    if frame_ours.shape[0] != 432 or frame_ours.shape[1] != 768:
                        frame_ours = cv2.resize(frame_ours, (768, 432), interpolation=cv2.INTER_AREA)
                    
                    frame_other = np.ones((432, 768, 3), np.uint8)*255
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    if task is 'handwrite':
                        text = "Cannot add handwritten characters"
                    elif task is 'dynamic':
                        text = "Cannot segment dynamic objects"
                    textsize = cv2.getTextSize(text, font, 1, 2)[0]
                    textX = (768 - textsize[0]) // 2
                    textY = (432 + textsize[1]) // 2

                    # add text centered on image
                    cv2.putText(frame_other, text, (textX, textY), font, 1, (0, 0, 0), 2)
                    

                
                    # edit here
                    _, frame_ours = draw_text(frame_ours, "Ours", height=H, width=W, align='right')
                    if other_method is 'hash':
                        _, frame_other = draw_text(frame_other, "Hashing-nvd", height=H, width=W, align='left')
                    if other_method is 'input':
                        _, frame_other = draw_text(frame_other, "Input", height=H, width=W, align='left')
                    if other_method is 'codef':
                        _, frame_other = draw_text(frame_other, "CoDeF", height=H, width=W, align='left')
                    if other_method is 'medm':
                        _, frame_other = draw_text(frame_other, "MeDM", height=H, width=W, align='left')
                
                    frame = cv2.hconcat([frame_other, frame_ours]) 
                
                    out.write(frame)
                
                cap_ours.release()
                out.release()
                cv2.destroyAllWindows()

                os.system('ffmpeg -y -i '+task+'_'+scene+'_'+other_method+'_vs_ours_video.avi -c:v libx264 -preset veryslow -crf 23 -pix_fmt yuv420p '+task+'_'+scene+'_'+other_method+'_vs_ours_video.mp4')
            
            
            

            ## canonical image
            H = 432
            W = 768
            fps = 20.0
            ours_canonical_path = './'+task+'/'+scene+'_ours_canonical.png'
            other_canonical_path = './'+task+'/'+scene+'_'+other_method+'_canonical.png'
            # Define the codec and create VideoWriter object
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(task+'_'+scene+'_'+other_method+'_vs_ours_canonical.avi', fourcc, fps, (2*W,  H))
            print(other_method)
            for i in range(5):
                frame_ours = cv2.imread(ours_canonical_path)
                if frame_ours.shape[0] != H or frame_ours.shape[1] != W:
                    frame_ours = cv2.resize(frame_ours, (W, H), interpolation=cv2.INTER_CUBIC)
                if other_method is 'input' or other_method is 'medm':
                    frame_other = np.ones((H, W, 3), np.uint8)*255
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    text = "No canonical image"

                    # get boundary of this text
                    textsize = cv2.getTextSize(text, font, 1, 2)[0]

                    # get coords based on boundary
                    textX = (W - textsize[0]) // 2
                    textY = (H + textsize[1]) // 2

                    # add text centered on image
                    cv2.putText(frame_other, text, (textX, textY), font, 1, (0, 0, 0), 2)
                else:
                    frame_other = cv2.imread(other_canonical_path)
                    frame_other = cv2.resize(frame_other, (W,H), interpolation=cv2.INTER_CUBIC)
                # edit here
                _, frame_ours = draw_text(frame_ours, "Ours", height=H, width=W, align='right')
                if other_method is 'hash':
                    _, frame_other = draw_text(frame_other, "Hashing-nvd", height=H, width=W, align='left')
                if other_method is 'input':
                    _, frame_other = draw_text(frame_other, "Input", height=H, width=W, align='left')
                if other_method is 'codef':
                    _, frame_other = draw_text(frame_other, "CoDeF", height=H, width=W, align='left')
                if other_method is 'medm':
                    _, frame_other = draw_text(frame_other, "MeDM", height=H, width=W, align='left')
                frame = cv2.hconcat([frame_other, frame_ours]) 
                out.write(frame)
            out.release()
            cv2.destroyAllWindows()
            os.system('ffmpeg -y -i '+task+'_'+scene+'_'+other_method+'_vs_ours_canonical.avi -c:v libx264 -preset veryslow -crf 23 -pix_fmt yuv420p '+task+'_'+scene+'_'+other_method+'_vs_ours_canonical.mp4')
            
            ## canonical image edited
            H = 432
            W = 768
            fps = 20.0
            ours_canonical_path = './'+task+'/'+scene+'_ours_canonical_edit.png'
            other_canonical_path = './'+task+'/'+scene+'_'+other_method+'_canonical_edit.png'
            # Define the codec and create VideoWriter object
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(task+'_'+scene+'_'+other_method+'_vs_ours_canonical_edit.avi', fourcc, fps, (2*W,  H))
            for i in range(5):
                frame_ours = cv2.imread(ours_canonical_path)
                if frame_ours.shape[0] != H or frame_ours.shape[1] != W:
                    frame_ours = cv2.resize(frame_ours, (W, H), interpolation=cv2.INTER_CUBIC)
                if other_method is 'input' or other_method is 'medm':
                    frame_other = np.ones((H, W, 3), np.uint8)*255
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    text = "No canonical image"

                    # get boundary of this text
                    textsize = cv2.getTextSize(text, font, 1, 2)[0]

                    # get coords based on boundary
                    textX = (W - textsize[0]) // 2
                    textY = (H + textsize[1]) // 2

                    # add text centered on image
                    cv2.putText(frame_other, text, (textX, textY), font, 1, (0, 0, 0), 2)
                else:
                    frame_other = cv2.imread(other_canonical_path)
                    frame_other = cv2.resize(frame_other, (W, H), interpolation=cv2.INTER_CUBIC)
                # edit here
                _, frame_ours = draw_text(frame_ours, "Ours", height=H, width=W, align='right')
                if other_method is 'hash':
                    _, frame_other = draw_text(frame_other, "Hashing-nvd", height=H, width=W, align='left')
                if other_method is 'input':
                    _, frame_other = draw_text(frame_other, "Input", height=H, width=W, align='left')
                if other_method is 'codef':
                    _, frame_other = draw_text(frame_other, "CoDeF", height=H, width=W, align='left')
                if other_method is 'medm':
                    _, frame_other = draw_text(frame_other, "MeDM", height=H, width=W, align='left')
                frame = cv2.hconcat([frame_other, frame_ours]) 
                out.write(frame)
            out.release()
            cv2.destroyAllWindows()
            os.system('ffmpeg -y -i '+task+'_'+scene+'_'+other_method+'_vs_ours_canonical_edit.avi -c:v libx264 -preset veryslow -crf 23 -pix_fmt yuv420p '+task+'_'+scene+'_'+other_method+'_vs_ours_canonical_edit.mp4')

            # get thumbnail images
            os.system('ffmpeg -y -i ./'+task+'/'+scene+'_input.mp4 -vf "select=eq(n\,0)" -q:v 3 ../thumbnails/'+task+'_'+scene+'_thumbnail.jpg')

# parse_one_task('styletransfer', ['bear', 'boat', 'hot-air-ballon', 'overlook-the-ocean', 'shark-ocean'], ['input', 'hash', 'codef', 'medm'])
parse_one_task('handwrite', ['train', 'camel', 'cat', 'car-turn', 'tiger'], ['input', 'hash', 'codef', 'medm'])
# parse_one_task('dynamic', ['coral-reef', 'butterfly', 'two-swan', 'woman-drink', 'surf'], ['input', 'hash', 'codef', 'medm'])