
## I. Beginning

1. Good afternoon everyone. 
2. It's a pleasure to be here with you today. Let me introduce myself first. 
3. I'm Wang Shuai, a student from BeiJingJiaoTong University. I'm majoring in electronic science and technology. My research field is medical image processing.
4. It's my great pleasure to be here and present my work on Cone Beam CT Series Images Rigid Registration for Temporomandibular Joint via Self-supervised Learning Network. The subject of my talk is to give a full-automatic method for temporomandibular joint CBCT image registration. 

## II. Transition-1
1. My talk will be in five parts.
2. Firstly, I would like to introduce the background of our research.  <font color='red'>[Turn Page 2]</font>


## III. Part-1

The temporomandibular joints (TMJs) registration from CBCT images plays an important role in medical diagnosis of related diseases. However, The traditional iterative method is slow, and it is impossible to judge the changes of the condyle bone, such as absorption and growth.

Manual registration is not only quite time-consuming but also subject to user variability. In order to address this problem, a full-automatic method is required to speed up the registration process while reducing human intervention. In this paper, we will focus on researching and proposing TMJs automatic registration method. <font color='red'>[Turn Page 3]</font>


The challenge for this subject is that The entire image structure is complex and will interfere with the registration of the temporomandibular joints. The registration speed of the traditional method is slow. And it can’t show the change of TMJ clearly.

About the dataset, Our TMJ image data comes from Peking University School and Hospital of Stomatology, consisting of 230 CBCT images. Among them, there are 130 images on the left and 100 images on the right. And there are 40 pairs of clinical data. The side length of volume resolution is 0.125 millimeter. Image size is 481 pixels.  <font color='red'>[Turn Page 4]</font>


<font color='red'>(!!!! click !!!!)</font> Here we focuses on 3D rigid transformation, which only includes rotation and translation. CBCT images mainly show the changes in bone structure that only contain rigid transformation. That's why we do not need to consider affine transformations.

There are no labels. The gold standard(known transformation) for image registration is difficult to obtain. So <font color='red'>(!!!! click !!!!)</font> in this paper We designed a self-supervised learning network based on DenseNet to regress parameters of rigid registration transformation. And we evaluate the registration performance of the proposed DenseNet by comparing it with other two methods, the ANTs and the Elastix method, respectively.


## IV. Transition-2

Now, let’s move to the next part `II.Methods`. <font color='red'>[Turn Page 5]</font>

## V. Part-2

#### 1. Pipeline
This is the workflow of our image registration framework. Let me try to briefly explain this procedure. The first step is to use an initial image as moving image. Construct a random deformation matrix, and synthesize a corresponding fixed image. The second step is to merge two images as input for training registration network. Finally, testing image or clinical image is for testing. <font color='red'>[Turn Page 6]</font>


#### 2.1 Image Processing: Histogram Matching

Before training the network, we need to do some image processing. To mitigate the risk of over-fitting and accelerate the convergence of the network, we decide to perform histogram matching on the original data. Look at the graph. The first image is deemed as the reference image, and the data distribution of all other images is based on this reference image. The establishment of grayscale mapping is to make the distribution of each image as consistent as possible. <font color='red'>[Turn Page 7]</font>


#### 2.2 Image Processing: Image Cropping instead of Size Reduction

In order to improve the similarity between the synthesized data and the clinical data, the each input image pairs are all cut into a $256×256×256$ patch block at the center. These images are the result of cropping. BTW, the gpu limitation is resolved. <font color='red'>[Turn Page 8]</font>

#### 3. Registration Network Architecture

Now I want to describe my registration network architecture. DenseNet is chosen as the backbone due to its transmission efficiency of information and gradients. It consists of 6 dense blocks for better feature extraction. <font color='red'>[Turn Page 9]</font>

#### 4. Loss Functions

Regarding loss functions, we choose The Mean Absolute Error(MAE). Just calculate the absolute distance of label and predicts. 


## VI. Transition-3

Ok, I’ve explained how we did with some details. <font color='red'>[Turn Page 10]</font>


## VII. Part-3

Let's look at the results. Each picture has two layers. The bottom layer is the fixed image, and the top layer is the warped image with color overlay. We choose to observe it from the sagittal slice. It clearly shows the TMJ difference after registration. The left is comparison of initial images. And the others are different methods. <font color='red'>[Turn Page 11]</font>

We also compute the Normalize Correlation Coefficient and Normalize Mutual Information. From the mean and variance, we could get the effectiveness of the method proposed. 

## VIII. Part-4

<font color='red'>[Turn Page 12]</font> Any method has limitations, and we are no exception. Although the registration time is reduced, some moving images with large transformations are still not aligned. <font color='red'>(!!!! click !!!!)</font>

However, it can be seen from the results that it’s similar to the results obtained by Elastix. On the other hand, it also shows the feasibility of our method.

## IX. Part-5

As a conclusion. <font color='red'>[Turn Page 13]</font>


First, We propose a self-supervised-learning framework for the full-automatic TMJ CBCT image registration.

And We demonstrate the excellent DenseNet registration ability in TMJ images and greatly improve the processing speed.

On the other hand, Our method can be applied to any other image registration, not limited to the temporomandibular joints images.

<font color='red'>[Turn Page 15]</font>That’s all I want to say for now on, Thanks!
