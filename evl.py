import cv2
import os
import numpy as np
from skimage.metrics import structural_similarity as ssimz
from PIL import Image
from skimage.metrics import peak_signal_noise_ratio
from SSIM_PIL import compare_ssim
import tensorflow as tf
sr_path = 'C:/Users/Pragyan/Desktop/20230406-172508_HypergraphII_celeba-hq_shape256x256_grid_mask'
hr_path = 'C:/Users/Pragyan/Desktop/coin2_256 - Copy'
psnr = []
ssim = []
l1ls = []
l2ls = []
i = 0
text_file = open("./results_coin.txt", "w")
#for i in range (1,8): #range(307, 403): #[3, 6, 7]: 
for root, dirs, files in os.walk (sr_path) :
    for file in files :
        if not file.split('.')[-1] in ['jpg', 'png', 'jpeg'] :
            continue
        st = str(i)+'.png'
        stk = str(i)+'.png'
        sr = tf.image.decode_image(tf.io.read_file(os.path.join(root, file)))
        print (os.path.join(root, file))
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
        l1 = np.sum(np.abs(hr - sr))
        l2 = np.sqrt(np.sum(np.square(hr-sr)))
        result_image = "IMAGE = " + file + " \t| PSNR = " + str(p) + "\t| SSIM = " + str(s) + "\t| L1 = " + str(l1) + "\t| L2 = " + str(l2) + "\n"
        text_file.write(result_image)
        psnr.append(p)
        ssim.append(s)
        l1ls.append(l1)
        l2ls.append(l2)
print()
text_file.write("-----------------------------\n")
final_result = "=>> MEAN PSNR = " + str(np.mean(psnr)) + " \t =>> MEAN SSIM = " + str(np.mean(ssim)) + " \t =>> MEAN L1 = " + str(np.mean(l1ls)) + " \t =>> MEAN L2 = " + str(np.mean(l2ls))
print(sr_path + "   =>> MEAN PSNR = " + str(np.mean(psnr)) + " \t =>> MEAN SSIM = " + str(np.mean(ssim)) + " \t =>> MEAN L1 = " + str(np.mean(l1ls)) + " \t =>> MEAN L2 = " + str(np.mean(l2ls)))
text_file.write(final_result)
print()
text_file.write("\n")
final_result = "=>> STDDEV PSNR = " + str(np.std(psnr)) + " \t =>> STDDEV SSIM = " + str(np.std(ssim)) + " \t =>> STDDEV L1 = " + str(np.std(l1ls)) + " \t =>> STDDEV L2 = " + str(np.std(l2ls))
print(sr_path + "   =>> STDDEV PSNR = " + str(np.std(psnr)) + " \t =>> STDDEV SSIM = " + str(np.std(ssim)) + " \t =>> STDDEV L1 = " + str(np.std(l1ls)) + " \t =>> STDDEV L2 = " + str(np.std(l2ls)))
text_file.write(final_result)
print()
text_file.close()
print ("DONE")