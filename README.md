# Hypergraphs Image Inpainting in Scanning Acoustic Microscopy for Super-Resolution

This repo contains the code of all the models. The codes are basically cloned from other github repositories and changes were made either in the code or in the training data to incorporate our masking method.

## Abstract

Scanning Acoustic Microscopy (SAM) uses highfrequency acoustic waves to generate non-ionizing, labelfree images of the surface and internal structures of industrial objects and biological specimens. The resolution of SAM images is limited by several factors such as the frequency of excitation signals, the signal-to-noise ratio, and the pixel size. We propose to use a hypergraphs image inpainting technique for SAM that fills in missing information to improve the resolution of the SAM image. We compared the performance of our technique with four other different techniques based on generative adversarial networks (GANs), including AOTGAN, DeepFill v2, Edge-Connect and DMFN. Our results show that the hypergraphs image inpainting model provides the SOTA average SSIM of 0.82 with a PSNR of 27.96 for 4× image size enhancement over the raw SAM image. We emphasize the importance of hypergraphs’ interpretability to bridge the gap between human and machine perception, particularly for robust image recovery tools for acoustic scan imaging. We show that combining SAM with hypergraphs can yield more noise-robust explanations.

### Illustration of the overarching image inpainting strategy for SAM. utilizing the alternative hole mask to provide an input image for the model and then employ image inpainting to produce a high-resolution version of the original.

![image](https://user-images.githubusercontent.com/88557062/231522866-fbb6e554-097b-42f9-ae7d-532601cd2d61.png)

### Two-stage course-to-fine hypergraphs image inpainting model architecture. 

![image](https://user-images.githubusercontent.com/88557062/231523103-e774bcb3-5349-46c9-a5bd-897f94163c3f.png)
