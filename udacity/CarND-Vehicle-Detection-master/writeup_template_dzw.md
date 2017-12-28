## Vehicle Detection Project

The goals / steps of this project are the following:

- Perform a Histogram of Oriented Gradients (HOG) feature extraction on a labeled training set of images and train a classifier Linear SVM classifier
- Optionally, you can also apply a color transform and append binned color features, as well as histograms of color, to your HOG feature vector.
- Note: for those first two steps don't forget to normalize your features and randomize a selection for training and testing.
- Implement a sliding-window technique and use your trained classifier to search for vehicles in images.
- Run your pipeline on a video stream (start with the test_video.mp4 and later implement on full project_video.mp4) and create a heat map of recurring detections frame by frame to reject outliers and follow detected vehicles.
- Estimate a bounding box for vehicles detected.

# [Rubric](https://review.udacity.com/#!/rubrics/513/view) Points

## Here I will consider the rubric points individually and describe how I addressed each point in my implementation.

--------------------------------------------------------------------------------

## Writeup / README

## Histogram of Oriented Gradients (HOG)

### 1\. Explain how (and identify where in your code) you extracted HOG features from the training images.

The code for this step is contained in the second code cell of the IPython notebook.

I started by reading in all the `vehicle` and `non-vehicle` images. Then coverted each image from RGB to greyscale. Then use `skimage.hog()` to extract the hog features.

I started off using the convering RGB to YCbCr color space and then using HOG parameters of `orientations=9`, `pixels_per_cell=(8, 8)` and `cells_per_block=(2, 2)`.

To get an intuition of what features were being extracted I plotted a few random sample of images from the car and non car images:

These are the car images(original image, image in greyscale and hog features: ![alt text][image8]

These are the non car images(original,greyscale) and features: ![alt text][image9]

### 2\. Explain how you settled on your final choice of HOG parameters.

I tried varying number of orientation bins, pixels by cell and number of cells per block.

Orientation bins - i wanted to keep this large enough that it would be able to account for a varying degree of gradients. This may help identify the shape or edges of cars taken at different angles.

Pixels by cell (range between 8 and 16) - I wanted to keep this small enough so that it has a finer resolution of the car image. For example, the larger the number of pixels per cells is, the courser the shape of the car will be

### 3\. Describe how (and identify where in your code) you trained a classifier using your selected HOG features (and color features if you used them).

Before training a linear SVC, i normalized the hog features using `sklearn.StandardScaler()`

I tried using HOG features, spatial and color histograms at first but it hurt my precision score. It had a higher number of false positives.

I then trained a linear SVM using only HOG features and got pretty good results. ('recall score', 0.97701793721973096) ('precision score', 0.98641765704584039)

## Sliding Window Search

### 1\. Describe how (and identify where in your code) you implemented a sliding window search. How did you decide what scales to search and how much to overlap windows?

I implemented a sliding window search using the Hog Sub-sampling window search.

Here what i did was a) First extract hog features for the entire image b) Then, divide the image into sliding windows of size 64 pixels going across and going down. I used an overlap of 50% to start with and seemed to get good results overall c) For each sliding window, I would determine the number of blocks within a sliding window and sample from the hog features. d) Once I had the hog features for each sliding window, I would use the model trained earlier and determine if a car was found

For the scales to search, I used a naive approach. I implemented a list to iterate through the image as shown below. The list contains the y start, y stop and scale. As you can see, as we move from the lower half of the image towards the bottom of the image the scale increases. This is intuitive as we expect cars that are towards the middle half of the image to be further away and hence the aspect ratio would be smaller while cars that are towards the bottom of the image to be nearer and the aspect ratio will be larger.

img_scales_settings = [[400,464,1], [416,480,1], [400,496,1.5], [432,528,1.5], [400,528,2], [432,560,2], [400,596,3.5], [464,660,3.5]]

Examples of overlapping sliding windows: ![alt text][image11]

### 2\. Show some examples of test images to demonstrate how your pipeline is working. What did you do to optimize the performance of your classifier?

To optimize the performance of the classifier, I did a a few things. a) Converted the image from RGB to YCrCb color space b) I experimented with different number of features ( i.e HOG, Spatial and Color Histogram) but ultimately decided that HOG features alone was better. c) I also experimented with the scale of the sliding window

Examples of Image with 2 Cars: ![alt text][image11]

Examples of Image with 1 Cars: ![alt text][image12]

--------------------------------------------------------------------------------

## Video Implementation

### 1\. Provide a link to your final video output. Your pipeline should perform reasonably well on the entire project video (somewhat wobbly or unstable bounding boxes are ok as long as you are identifying the vehicles most of the time with minimal false positives.)

Here's a [link to my video result][image13]

### 2\. Describe how (and identify where in your code) you implemented some kind of filter for false positives and some method for combining overlapping bounding boxes.

I performed the following a) use a method to find all bounding boxes that contain a car. These bounding boxes will overlap b) Make a copy of the image or pixels and initialize to zero. c) Iterate over the bounding boxes, for each pixel within a bounding box increment the value by 1 d) Apply a treshold to filter for pixels with less than 1 bounding box e) Then use `scipy.ndimage.measurements.label()` to identify segments in the heatmap. Each segment is then assumed to be where a car or object is located f) Take the min and max index of the segments and use that to form the top left and bottom right of a bounding box

## Here are six frames with merged bounding boxes and their corresponding heatmaps:

![alt text][image10]

--------------------------------------------------------------------------------

## Discussion

### 1\. Briefly discuss any problems / issues you faced in your implementation of this project. Where will your pipeline likely fail? What could you do to make it more robust?

One issue I ran into was ensuring the images from the video were very similar to the the images used for training. For example, in the images used for training, I noticed most of the car images had close up perspectives or views of the cars and little background in the car images.. i.e the image of pixel size 64 x 64 was mostly covered by the car image. Thus, I had to make sure when I was scaling the sliding window each sliding window would capture the car in the same perspective or shape.

[//]: # "Image References"
[image1]: ./examples/car_not_car.png
[image10]: ./examples/test_img_bbox_heatmap.png
[image11]: ./examples/sliding_window_examples.png
[image12]: ./examples/sliding_window_examples2.png
[image13]: ./test_video_out.mp4
[image2]: ./examples/HOG_example.jpg
[image3]: ./examples/sliding_windows.jpg
[image4]: ./examples/sliding_window.jpg
[image5]: ./examples/bboxes_and_heat.png
[image6]: ./examples/labels_map.png
[image7]: ./examples/output_bboxes.png
[image8]: ./examples/car_img_hog_features1.png
[image9]: ./examples/non_car_img_hog_features1.png
[video1]: ./project_video.mp4
