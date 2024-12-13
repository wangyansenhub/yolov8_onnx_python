def calculate_r_value(image_path):

# 读取tif格式的图片
    # image_path = "data/20241126-gan/20241126093638.tif"  # 替换为实际的图片路径
    image = cv2.imread(image_path,0)

    # 获取图片的高度和宽度
    height, width = image.shape[:2]

    # 计算切割的坐标
    half_width = width // 2

    # 切割出左边的图片（宽度范围0到half_width - 1）
    low_energy_image = image[:, :half_width]
    # print("left_image.shape:", left_image.shape)
    # 切割出右边的图片（宽度范围half_width到width - 1）
    high_energy_image = image[:, half_width:]


    epsilon = 0.0
    # r_value_image = (enhanced_high_energy.astype(np.float32) + epsilon) / (enhanced_low_energy.astype(np.float32) + epsilon)
    r_value_image = (high_energy_image.astype(np.float32) + epsilon) / (low_energy_image.astype(np.float32) + epsilon)


# # 可以进行归一化等操作来完善

        # 将R值图像转换为适合显示和保存的8位无符号整数类型（范围是[0, 255]）
    r_value_image = np.stack((low_energy_image, high_energy_image, r_value_image), axis=-1)
    r_value_image_display = (r_value_image * 255).astype(np.uint8)

    # 显示R值图像（可选，用于直观查看结果）
    # cv2.imshow("R-Value Image", r_value_image_display)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # 保存R值图像（可选，可根据实际需求指定保存路径和文件名）
    return image,r_value_image_display
