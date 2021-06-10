import numpy as np
import skvideo
import cv2

def myConv3D(A, B, param):
    conv_list = []
    shapeA = np.shape(A)
    for x in range(shapeA[0]-2):
        for y in range(shapeA[1]-2):
            for z in range(shapeA[2]-2):
                conv_sum = (B * padded_video[x:x + B.shape[0], y:y + B.shape[1],
                                   z:z + B.shape[2]]).sum()
                conv_list.append(conv_sum)
    conv = np.reshape(conv_list, newshape=param)


    return conv


def create_smooth_kernel(size):
    conv_kernel = np.full((size, size, size), 1 / size ** 3)
    return conv_kernel


def pad_image(A, size):
    shape = np.shape(A)
    padded_array = np.zeros((shape[0] + (size - 1), shape[1] + (size - 1), shape[2] + (size - 1)))
    padded_array[size // 2:-(size // 2), size // 2:-(size // 2), size // 2:-(size // 2)] = A
    return padded_array


if __name__ == '__main__':

    # setting a path for FFmpeg
    video_string = 'video.mp4'
    path = "C:/Program Files (x86)/ffmpeg/ffmpeg-N-99816-g3da35b7cc7-win64-gpl-shared/bin"
    skvideo.setFFmpegPath(path)

    # reading video and printing its shape
    import skvideo.io
    video = skvideo.io.vread(video_string)
# =====================================================================
    # converting video to grayscale
    gray_scale = np.empty([150, 360, 640])
    for i in range(len(video)):
        gray = cv2.cvtColor(video[i], cv2.COLOR_RGB2GRAY)
        gray_scale[i] = gray
    # creating the kernel
    kernel = create_smooth_kernel(size=3)
    print(kernel)
    # padding the video
    padded_video = pad_image(A=gray_scale, size=3)
    print(padded_video)
    # creating the new video
    conv_video = myConv3D(A=padded_video, B=kernel, param=np.shape(gray_scale))
    print(conv_video)
    # check if we have the shape that we want
    print(np.shape(conv_video))
    # saving the new video
    skvideo.io.vwrite('convvideo.mp4', conv_video, backend='ffmpeg')
