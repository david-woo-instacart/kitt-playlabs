**Advanced Lane Finding Project**

The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

[//]: # (Image References)

[image1]: ./examples/undistort_output.png "Undistorted"
[image2]: ./test_images/test1.jpg "Road Transformed"
[image3]: ./examples/binary_combo_example.jpg "Binary Example"
[image4]: ./examples/warped_straight_lines.jpg "Warp Example"
[image5]: ./examples/color_fit_lines.jpg "Fit Visual"
[image6]: ./examples/example_output.jpg "Output"
[video1]: ./project_video_out.mp4 "Video"
[image7]: ./examples/orig_undistorted_img.png "Undistorted Image"
[image8]: ./examples/car_orig_undistorted_img.png "Car Undistorted Image"
[image9]: ./examples/color_gradient_threshold.png "Color & Gradient Threshold Image"
[image10]: ./examples/lane_curvature.png "Lane curvature using polyfit"
[image11]: ./examples/3_src_lane_trapezium.png "3_src_lane_trapezium"
[image12]: ./examples/3_dst_lane_bird_eye.png "3_dst_lane_bird_eye"
[image13]: ./examples/3_src_dst_curved_lanes.png "3_src_dst_curved_lanes"
[image14]: ./examples/6_mapped_lane.png "6_mapped_lane"

## [Rubric](https://review.udacity.com/#!/rubrics/571/view) Points

### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---

### Writeup / README

#### 1. Provide a Writeup / README that includes all the rubric points and how you addressed each one.  You can submit your writeup as markdown or pdf.  [Here](https://github.com/udacity/CarND-Advanced-Lane-Lines/blob/master/writeup_template.md) is a template writeup for this project you can use as a guide and a starting point.  

You're reading it!

### Camera Calibration

#### 1. Briefly state how you computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image.

The camera matrix tries to find the projective transformation from camera coordinates to pixel or image coordinates.

Steps:
1) Create an array of object points which represent the x, y, z points of the camera coordinates in the real world. Assume these object points are the same for each camera image.
2) Iterate through the camera images
3) For each camera image, given the expected number of inner corners in the image, find all the inner chessboard corners in the image, using `cv2.findChessboardCorners()`
4) If corners are found, return the image coordinates of the inner corners.
5) Store the object real world coordinates `objpoints` and image coordinates `imgpoints` for each image
6) Given the object points and image points of the corners across images, we then compute the camera calibration and the distortion coefficients, using `cv2.calibrateCamera()`
7) The camera calibration calculates the intrinsic parameters. This refers to the projective transformation from camera coordinates to pixel coordinate which includes the optical center, focal center and skew. The distortion coefficients corrects for warping of the images especially due to lens distortion or bending of the light towards the edges of the lens
8) Undistort the image using `cv2.undistort()` function and obtained this result:

![alt text][image7]

### Pipeline (single images)

#### 1. Provide an example of a distortion-corrected image.

I applied the camera matrix and distortion coefficients previously obtain and undistorted the image using `cv2.undistort()` function and obtained the below result (it's more evident from the horizontal sign boards, on the left the sign boards are warped, on the right the sign boards are unwarped):

![alt text][image8]

#### 2. Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image.  Provide an example of a binary image result.

I tried a few different combinations for form a thresholded binary image (color transform, absolute sobel thresholding for both x and y, thresholding based on the magnitude / direction of the gradient).

I finally settled on using color spaces and magnitude of the gradient to form a thresholded binary image. Below are some of the details:
a) color transforms - Transformed the image to HLS color space and applied thresholds based on the saturation level
b) Magnitude gradient threshold - Calculate the gradient both in the x and y direction. Then calculate the magnitude based on the square root of sum squares and set a threshold

Here is an output of this step:
![alt text][image9]

#### 3. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.


Steps:
1) Draw a trapezium that represents the start and end of lanes lines in the original image. Use the four corners of the trapezium and stores as source points (`src`)
2) Then determine the four corresponding points in the destination image. This is done using the height and width of the image and applying an offset to the height and width of the image, I subtracted an offset of 100 pixels from both sides of the width of the image,  store these points as destination points (`dst`)
3) Calculate the transform matrix from the source points to the destination points using `cv2.getPerspectiveTransform`
4) Then apply the transform matrix to the original image to get the bird eye view of the lane lines.

The code for my perspective transform includes a function called `warper()`, which appears in lines 1 through 8 in the file `example.py` (output_images/examples/example.py) (or, for example, in the 3rd code cell of the IPython notebook).  The `warper()` function takes as inputs an image (`img`), as well as source (`src`) and destination (`dst`) points.  I chose the hardcode the source and destination points in the following manner:

```python
src = np.float32([
                [src_offset_x_top_left,src_start_y],
                [img_size[0]-src_offset_x_top_right,src_start_y,
                [img_size[0]-src_offset_x_btm_right,img_size[1],
                [src_offset_x_btm_left,img_size[1]]
                ])
dst = np.float32([
                [dst_offset,dst_offset],
                [img_size[0]-dst_offset,dst_offset],
                [img_size[0]-dst_offset,img_size[1]],
                [dst_offset,img_size[1]]
                ])
```

This resulted in the following source and destination points:

| Source        | Destination   |
|:-------------:|:-------------:|
| 575, 460      | 100, 100        |
| 705, 460      | 1180, 100      |
| 1180, 720     | 1180, 720      |
| 150, 720      | 100, 720        |

Below are results for a curved line, left show original image with trapezium, right shows perspective transformed image:

![alt text][image13]

#### 4. Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial?

First, I'll describe how I identified lane-line pixels and then discuss how I fit their positions with a polynomial

Steps for identifying lane-line pixels:
1) From my thresholded binary image, I plotted a histogram that summed up the y values across the x values. Since lanes are mostly vertical vs horizontal, the peaks in the histogram should reflect where the lane lines begin
2) To get the peaks of the histogram, i seperated the histogram by calculating the midpoint.
3) From the midpoint of the histogram, I got the starting position of the left lane by determining the peak to the left of the midpoint and got the starting position of the right lane by determining the peak to the right of the midpoint

Steps for fitting their positions with a polynomial:
1) Given the starting points of the left and right lane, I then used a sliding window to get all the pixels that would reflect the left and right lane.
I started within 9 sliding windows per image with a margin or window size of 100 pixel. The sliding windows would move from the bottom of the image to the top of the image and the sliding window would get recentered of each iteration based on the lane pixels identified
2) The sliding window determines all non-zero points and adds the indexes to `left_lane_inds` and `right_lane_inds`, for the left and right lane respectively. These non-zero points are assumed to represent the lane lines. If there are at least 50 pixels detected, the sliding window gets recentered for the next iteration, this way it can moved along curved lanes as well
3) I then use the the indexes of the left and right lane pixels to get all non-zero points and then fit a 2nd degree polynomial based on the x and y coordinates

Below shows the histogram to get starting position of lane pixels and the sliding windows and polynmial fit.

![alt text][image10]

#### 5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

I calculated the radius of the curve closest to my vehicle using the below formula. Since the y values increase from top to bottom, to get the radius closest to my vehicle I used the y value corresponding to the bottom of the image in this case y_max = image.shape[0]

```python
left_curve = (1 + (2*left_fit[0]*y_max + left_fit[1])**2)**(3/2) / np.abs(2*left_fit[0])

right_curve = (1 + (2*right_fit[0]*y_max + right_fit[1])**2)**(3/2) / np.abs(2*right_fit[0])
```

#### 6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

Below is an example of my result plotted back down into the road whereby the lane is identified clearly

![alt text][image14]

---

### Pipeline (video)

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).

Here's a [link to my video result](./project_video_out.mp4)

---

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

Some problems I faced was identifying the lane lines. I had to try different combinations of image mask (setting threshold on color space, different gradients) to get a clear representation of the lane lines in the image. This seemed to skew towards more hand-based rules or heuristics In a practical pipeline, this could be quite brittle as it may not be able to generalize beyond the trained set of images. We could potentially use convolutional neural networks to identify the lane lines, this way identifying lane lines can be more robust.
