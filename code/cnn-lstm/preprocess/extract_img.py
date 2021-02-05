'''
Author: Liu Gang
Date: 2020-12-21 09:33:25
LastEditTime: 2020-12-21 18:34:25
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \可行性实验程序\preprocessing.py
'''

import cv2
import argparse
import dlib
import numpy as np
import os




class VideoPreprocess():

    def __init__(self, opt):
        self.opt = opt
        self.is_success = True

        if opt.source.split('/')[2].split('.')[0] == '1':
            if opt.distance == 'near':
                # near object of video name 1.mp4
                self.start_frame = 1*30
                self.end_frame = 20*30
                print('debug video 1 successful')
            elif opt.distance == 'far':
                # far object of video name 1.mp4
                self.start_frame = 34* 30
                self.end_frame = 53* 30
        elif opt.source.split('/')[2].split('.')[0] == '2':
            if opt.distance == 'near':

                self.start_frame = 1 * 30
                self.end_frame = 7 * 30  # 4秒之前是近的
                print('debug video 2 successful')
            elif opt.distance == 'far':
                # far object of video name 2.mp4
                self.start_frame = 10 * 30  # 6 秒之后是远的
                self.end_frame = 18 * 30  # 10秒之前是远的

        # self.end_frame = 10
        self.predictor_path = "../dlib/shape_predictor_68_face_landmarks.dat"
        self.video_size = (200, 50)  # w h
        self.offset_pixelY = -14
        self.offset_pixelX = 0


    def video_process(self):

        predictor = dlib.shape_predictor(self.predictor_path)

        # 初始化dlib人脸检测器
        detector = dlib.get_frontal_face_detector()

        videoCapture = cv2.VideoCapture(self.opt.source)

        print(videoCapture.isOpened())
        count=0
        while self.is_success:
            self.is_success, frame = videoCapture.read()  # opencv 读取图像的格式为 H,W,C https://blog.csdn.net/sinat_28704977/article/details/89969199
            count+=1
            if count > self.start_frame and count <=self.end_frame:
                print("count",count-self.start_frame)
                dets = detector(frame, 0)#提取关键点
                pt_pos = []
                eye_w, eye_h = 100, 50
                for k, d in enumerate(dets):
                    print("dets{}".format(d))
                    print(
                        "Detection{}: Left: {} Top: {} Right: {} Bottom: {}".format(
                            k, d.left(), d.top(), d.right(), d.bottom()))
                    shape = predictor(frame, d)# 预测人脸形状大小
                    for index, pt in enumerate(shape.parts()):
                        pt_pos.append((pt.x, pt.y))#人脸坐标点

                    cv2.waitKey(30)

                    left_eye = frame[
                               pt_pos[37][1] + self.offset_pixelY:pt_pos[37][1]
                                                                 + eye_h + self.offset_pixelY,
                               pt_pos[36][0] + self.offset_pixelX:pt_pos[36][
                                                                     0] + eye_w +self.offset_pixelX]

                    right_eye = frame[
                                pt_pos[44][1] +self.offset_pixelY:pt_pos[44][1]
                                                                  + eye_h + self.offset_pixelY,
                                pt_pos[42][0] +self.offset_pixelX:pt_pos[42][
                                                                      0] + eye_w +self.offset_pixelX]
                    print("left",left_eye.shape)
                    print("right_eye.shape",right_eye.shape)
                    if opt.save_img == True:
                        if not os.path.exists(
                                os.path.join(opt.save_path, 'left')):
                            os.makedirs(os.path.join(opt.save_path, 'left'))

                        if not os.path.exists(
                                os.path.join(opt.save_path, 'right')):
                            os.makedirs(os.path.join(opt.save_path, 'right'))

                        if not os.path.exists(
                                os.path.join(opt.save_path, 'concat')):
                            os.makedirs(os.path.join(opt.save_path, 'concat'))

                        crop_eye = np.concatenate((left_eye, right_eye),
                                                  axis=1)
                        if left_eye.shape[:2] == (50, 100) and right_eye.shape[:2] == (50, 100):  # 格式为 H*W*C
                            if opt.distance == 'near':
                                # cv2.imwrite(os.path.join(opt.save_path, (
                                #     'left/N_left_eye_area_frame_{}.jpg'.format(
                                #         count))), left_eye)
                                # cv2.imwrite(os.path.join(opt.save_path, (
                                #     'right/N_right_eye_area_frame_{}.jpg'.format(
                                #         count))), right_eye)
                                cv2.imwrite(os.path.join(opt.save_path, (
                                    'concat/N_both_eyes_area_frame_{}.jpg'.format(
                                        count))),
                                            crop_eye)
                            else:
                                # cv2.imwrite(os.path.join(opt.save_path, (
                                #     'left/F_left_eye_area_frame_{}.jpg'.format(
                                #         count))), left_eye)
                                # cv2.imwrite(os.path.join(opt.save_path, (
                                #     'right/F_right_eye_area_frame_{}.jpg'.format(
                                #         count))), right_eye)
                                cv2.imwrite(os.path.join(opt.save_path, (
                                    'concat/F_both_eyes_area_frame_{}.jpg'.format(
                                        count))),
                                            crop_eye)
                            crop_eye = cv2.resize(crop_eye, self.video_size)

                            cv2.imshow('crop_eyes', crop_eye)
            if count > self.end_frame:
                print('completely!')
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        videoCapture.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=str, default='../videos/1.mp4',
                        help='source')  # file/folder, 0 for webcam
    parser.add_argument('--output', type=str,
                        default='../result/both_eyes_concat_near.avi',
                        help='output')  # file/folder, 0 for webcam
    parser.add_argument('--name', type=str,
                        default='video1_B_channel_near_object',
                        help='inference size (pixels)')
    parser.add_argument('--distance', type=str, default='far',
                        help='测试的视频的哪一段，如果为近处，则为near 远处为far')
    parser.add_argument('--save_img', type=bool, default=True, help='是否保存每帧图像')
    parser.add_argument('--save_path', type=str,
                        default='../result/images/video1_near_2/',
                        help='保存图像的路径')
    opt = parser.parse_args()

    videoprocess = VideoPreprocess(opt)
    videoprocess.video_process()
