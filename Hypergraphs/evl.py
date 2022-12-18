import cv2
import os
import numpy as np
from skimage.metrics import structural_similarity as ssimz
from PIL import Image
from skimage.metrics import peak_signal_noise_ratio
#from SSIM_PIL import compare_ssim
import tensorflow as tf
sr_path = './Testing2/test_4'
hr_path = './celeba-hq'
psnr = []
ssim = []
i = 0
text_file = open("./result_test_4.txt", "w")
#for i in range (1,8): #range(307, 403): #[3, 6, 7]: 
for root, dirs, files in os.walk (sr_path) :
    for file in files :
        if not file.split('.')[-1] in ['jpg', 'png', 'jpeg'] :
            continue
        st = str(i)+'.png'
        stk = str(i)+'.png'
        sr = tf.image.decode_image(tf.io.read_file(os.path.join(root, file)))
        #print (os.path.join(root, file))
        #sr = np.squeeze(sr)
        hr = tf.image.decode_image(tf.io.read_file(os.path.join(hr_path, file)))
        if hr.shape[2]==4:
            hr = hr[:,:,:-1]
        if sr.shape[2]==4:
            sr = sr[:,:,:-1]
        sr = tf.expand_dims(sr, axis=0)
        hr = tf.expand_dims(hr, axis=0)
        #hr = tf.image.convert_image_dtype(hr, tf.float32)
        #sr = tf.image.convert_image_dtype(sr, tf.float32)
        sr1 = cv2.imread(os.path.join(root, file))
        hr1 = cv2.imread(os.path.join(hr_path, file))
        #s = compare_ssim(hr, sr)
        s = tf.image.ssim(hr, sr, max_val=255, filter_size=11, filter_sigma=1.5, k1=0.01, k2=0.03)
        #s = tf.image.ssim(hr, sr, max_val=1.0, filter_size=11, filter_sigma=1.5, k1=0.01, k2=0.03)
        #s = int(s)
        p = peak_signal_noise_ratio(hr1, sr1)
        result_image = "IMAGE = " + file + " \t| PSNR = " + str(p) + "\t| SSIM = " + str(s) + "\n"
        text_file.write(result_image)
        print (result_image)
        psnr.append(p)
        ssim.append(s)
print()
final_result = "=>> MEAN PSNR = " + str(np.mean(psnr)) + " \t =>> MEAN SSIM = " + str(np.mean(ssim))
print(sr_path + "   =>> MEAN PSNR = " + str(np.mean(psnr)) + " \t =>> MEAN SSIM = " + str(np.mean(ssim)))
text_file.write("-----------------------------\n")
text_file.write(final_result)
text_file.close()
print ("DONE")