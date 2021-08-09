# mri_reconstruction

The stratergy followed is to setup the baseline FastMRI network and then setup a methodology to compare effectiveness of different loss metrics like SSIM, MSE, NMSE, PSNR through assignment of visual ranking for each of them. 

The set considered for it (23 ground-truth vs subsampled pairs):
![MRI_Comp1](https://user-images.githubusercontent.com/58559090/128677388-57a165f5-849b-4b00-b803-9677d1222e14.png)
![mriComp2](https://user-images.githubusercontent.com/58559090/128677405-5793d696-0ecc-4627-95cb-b211aeb95834.jpg)


The methadology in brief is as folows (for a detaild take refer the [PAPER](MRI_Reconstruction.pdf):
1. Set of MRI reconstructed pairs are chosen
2. Loss metrics are applied on these chosen pairs
3. A visual ranking is assigned for the set by means of visual observation (Here observation is a substitute for actual clinical evaluation) which is considered as the golden ranking or the ground truth ranking
4. A small code is arrived at for comparing the rankings by loss metric to ranking by observation. This provides a score for each metric that stands for how effective that metric is for scoring the orginal and reconstructed image
5. The obtained score are then used as weights for creating a weighted sum of these loss metric
6. The weighted sum is then used as loss function in training


The scoring based on comparison with visual ground-truth ranking, is done using this [script](compare_rankings.pl) 

Seperate to this, concept of edge loss is also incorporated. 
![EdgeDetectionFirstResult](https://user-images.githubusercontent.com/58559090/128676856-16357c42-1344-4e50-a084-33750f8e751c.png)

For visualization of fastMRI data for the above purposes this script is used [script](data_viz.py) was used.


The paper is available [HERE](MRI_Reconstruction.pdf)


