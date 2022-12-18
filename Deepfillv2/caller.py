import os

path = './eg/celeba5/'

for root, dirs, files in os.walk (path) :
    for file in files :
        if not file.split('.')[-1] in ['jpg', 'png', 'jpeg'] :
            continue
        img = path + file
        msk = './eg/celeba5_m/' + file[:-4] +'.png'#maskpath
        opt = './eg/celeba5h_o/' + file
        cpt = './pretrained/states_100000_best_v2.pth' #checkpoint
        cm = 'python test.py --image ' + img + ' --mask ' + msk + ' --out ' + opt + ' --checkpoint ' + cpt
        print (cm)
        #os.popen(cm)
        os.system(cm)
        
print ("END")