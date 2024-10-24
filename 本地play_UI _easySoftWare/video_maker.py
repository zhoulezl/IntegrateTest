import pyautogui
import time
import imageio
import os


# # 设置录制参数
# recording_duration = 10  # 录制时长（秒）
# frame_interval = 20  # 每秒捕获的帧数（FPS）
# output_video_file = "recorded_video.mp4"
# output_image_folder = "screenshots"

class VideoMaker:
    test_fini = False
    def make_screenshot(self, output_image_folder):
        # 确保输出文件夹存在
        if not os.path.exists(output_image_folder):
            os.makedirs(output_image_folder)

        # 获取屏幕大小
        screen_width, screen_height = pyautogui.size()
        # 开始录制
        # print(f"开始录制 {recording_duration} 秒...")
        start_time = time.time()
        frame_count = 0
        while not self.test_fini:
            # 捕获屏幕截图
            screenshot = pyautogui.screenshot(region=(0, 0, screen_width, screen_height))
            # 保存截图
            frame_filename = os.path.join(output_image_folder, f"frame_{frame_count:04d}.png")
            screenshot.save(frame_filename)
            # print(time.time(), frame_filename)
            # 增加帧数
            frame_count += 1
            # 等待下一帧的时间
            time.sleep(1 / 3)
        # 测试线程结束后再录制3秒
        for i in range(3):
            # 捕获屏幕截图
            screenshot = pyautogui.screenshot(region=(0, 0, screen_width, screen_height))
            # 保存截图
            frame_filename = os.path.join(output_image_folder, f"frame_{frame_count:04d}.png")
            screenshot.save(frame_filename)
            # print(time.time(), frame_filename)
            # 增加帧数
            frame_count += 1
            # 等待下一帧的时间
            time.sleep(1 / 3)
        print("录制结束。")
        # return frame_count

    def make_video(self, output_image_folder, output_video_file):
        frame_count = 0
        for root, dirs, files in os.walk(output_image_folder):
            for file in files:
                if file.endswith('.png'):
                    frame_count += 1
        # 创建视频文件
        with imageio.get_writer(output_video_file, fps=3) as writer:
            for i in range(frame_count):
                frame_filename = os.path.join(output_image_folder, f"frame_{i:04d}.png")
                image = imageio.v2.imread(frame_filename)
                writer.append_data(image)

        print(f"视频已保存到 {output_video_file}")
