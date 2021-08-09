import pathlib
import torch
from fastmri.data import subsample
from fastmri.data import transforms, mri_data
from fastmri.losses import CannyFilter
from torch.nn import functional as F
import fastmri
import numpy as np
import skimage
from skimage.metrics import structural_similarity, peak_signal_noise_ratio
import matplotlib.pyplot as plt
import sys


# Create a mask function
mask_func = subsample.RandomMaskFunc(
    center_fractions=[0.08, 0.04],
    accelerations=[4, 8]
)

def data_transform(kspace, mask, target, data_attributes, filename, slice_num):
    # Transform the data into appropriate format
    # Here we simply mask the k-space and return the result
    kspace = transforms.to_tensor(kspace)
    masked_kspace, _ = transforms.apply_mask(kspace, mask_func)
    return masked_kspace

dataset_masked = mri_data.SliceDataset(
    root=pathlib.Path(
      '/home/lss/Documents/DL_Project/fastMRI/trials/singlecoil_train'
    ),
    transform=data_transform,
    challenge='singlecoil'
)

dataset = mri_data.SliceDataset(
    root=pathlib.Path(
      '/home/lss/Documents/DL_Project/singlecoil_train'
    ),
    challenge='singlecoil'
)

if len(sys.argv)<2:
    masked_kspace = dataset_masked[54]
    data = dataset[54]
    image = data[2]
    subsampled_image = fastmri.ifft2c(masked_kspace)
    subsampled_image = fastmri.complex_abs(subsampled_image)
    plt.subplot(1,2,1)
    plt.title("Fullysampled Slices")
    plt.imshow(image, cmap = 'gray')
    plt.subplot(1,2,2)
    plt.title("Subsampled Slices")
    plt.imshow(subsampled_image, cmap = 'gray')
    plt.show()
    sys.exit()


if sys.argv[1] == "--iterate":
    mimg = None
    img = None
    for idx, mkspace in enumerate(dataset_masked):
        if idx > 600:
            kspace = dataset[idx]
            image = kspace[2] #fullysampled kspace slice images
            if idx>1200:
                break
            subsampled_image = fastmri.ifft2c(mkspace)
            subsampled_image = fastmri.complex_abs(subsampled_image)
            #image = fastmri.ifft2c(kspace[2])
            #image = fastmri.complex_abs(image)
            if img is None:
                plt.subplot(1, 2, 1)
                plt.title("Fullysampled Slice")
                img = plt.imshow(image, cmap = 'gray')
                plt.subplot(1, 2, 2)
                plt.title("Subsampled Slice")
                mimg = plt.imshow(subsampled_image, cmap = 'gray')
            else:
                img.set_data(image)
                plt.subplot(1, 2, 1)
                plt.title("Fullysampled Slice "+str(idx))
                mimg.set_data(subsampled_image)
                plt.subplot(1, 2, 2)
                plt.title("Subsampled Slice "+str(idx))
            plt.pause(.2)
            plt.draw()

if sys.argv[1] == "--few_main_slices":
    #print('test')
    mimg = None
    img = None
    slice_list2 = [18, 55, 96, 140, 209, 312, 346, 380, 409, 440, 480, 597]
    slice_list = [602, 667, 709, 788, 816, 854, 892, 959, 1029, 1097, 1176]
    plt.figure()
    #plt.subplots(12,2,figsize=(20,8))
    for idx, mkspace in enumerate(dataset_masked):
        if idx >1200:#597:
            break
        kspace = dataset[idx]
        image = kspace[2] #fullysampled kspace slice images
        if idx not in slice_list:
            continue
        subsampled_image = fastmri.ifft2c(mkspace)
        subsampled_image = fastmri.complex_abs(subsampled_image)
        subsampled_image = transforms.center_crop(subsampled_image, (320,320))
        #print(type(image))
        #print(type(subsampled_image))
        print(slice_list.index(idx))
        #image = torch.from_numpy(image)
        #loss calculation
        MSE = np.mean((image - subsampled_image.numpy()) ** 2) 
        NMSE = np.linalg.norm(image - subsampled_image.numpy()) ** 2 / np.linalg.norm(image) ** 2
        PSNR = peak_signal_noise_ratio(image, subsampled_image.numpy(), data_range=image.max())
        SSIM = structural_similarity(
        image, subsampled_image.numpy(), multichannel=False, data_range=image.max()
    )
        plt.subplot(3, 8, 2*(slice_list.index(idx)+1)-1)
        plt.imshow(image, cmap = 'gray')
        plt.subplot(3, 8, 2*(slice_list.index(idx)+1))
        #"PSNR = "+'{0:.10f}\n'.format(PSNR)+
        plt.title("MSE = "+'{0:.10f}\n'.format(MSE*100000000000)+"NMSE = "+'{0:.10f}\n'.format(NMSE*100)+"PSNR = "+'{0:.10f}\n'.format(PSNR)+"SSIM = "+'{0:.10f}'.format(SSIM))
        plt.imshow(subsampled_image, cmap = 'gray')
    #plt.tight_layout()
    plt.show()

if sys.argv[1] == "--edge":
    data = dataset[816]
    image = data[2]
    image = torch.from_numpy(image).cuda()
    if(len(image.shape)<3):
        image = image.unsqueeze(dim = 0)
    if(len(image.shape)<4):
        image = image.unsqueeze(dim = 0)
    img_mean = image.mean()
    print(img_mean)
    if img_mean < 2.8e-05:
        #thresh = 0.000018
        thresh = 0.000026
    elif img_mean <3.8e-05:
        #thresh = 0.000024
        thresh = 0.000027
    else:
        #thresh = 0.000037
        thresh = 0.000045

    image = F.interpolate(image, size=(520, 520), mode='bicubic', align_corners=False)
    #output = F.interpolate(output, size=(420,420), mode='bicubic', align_corners=False)
    canfilt = CannyFilter(k_gaussian = 3, sigma = 1, k_sobel=3, use_cuda=True)
    edge = canfilt.forward(image, low_threshold = thresh, hysteresis = True)
    edge = edge.cpu()
    image = image.cpu()
    image = image.squeeze(dim = 0).squeeze(dim=0)
    edge = edge.squeeze(dim = 0).squeeze(dim=0)
    edge = edge.detach()
    #edge = 10/edge.max() * edge
    #edge = edge**2
    #edge = 255/edge.max() * edge
    print(image.shape, edge.shape)
    #print(edge.max())
    plt.subplot(1,2,1)
    plt.title("Fullysampled Image")
    plt.imshow(image, cmap = 'gray')
    plt.subplot(1,2,2)
    plt.title("Edge of Fullysampled Image")
    plt.imshow(edge, cmap = 'gray')
    plt.show()

