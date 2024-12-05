import tkinter as tk
from tkinter import messagebox
from onnx_detect import YOLOv8, calculate_r_value
import cv2
import glob
import os



def main():
    root = tk.Tk()
    root.title("际遥双能煤矸石检测系统")

    # 模型文件路径输入框
    model_path = tk.Label(root, text="模型文件路径:")
    model_path.grid(row=0, column=0, padx=5, pady=5)
    entry_model = tk.Entry(root, width=50)
    entry_model.grid(row=0, column=1, padx=5, pady=5)

    # 待检图片路径输入框
    source_path = tk.Label(root, text="待检图片路径:")
    source_path.grid(row=1, column=0, padx=5, pady=5)
    entry_source = tk.Entry(root, width=50)
    entry_source.grid(row=1, column=1, padx=5, pady=5)

    # 检测结果保存路径输入框
    source_result = tk.Label(root, text="检测结果保存路径:")
    source_result.grid(row=2, column=0, padx=5, pady=5)
    entry_result = tk.Entry(root, width=50)
    entry_result.grid(row=2, column=1, padx=5, pady=5)

    # 滚动加载选项
    var_scroll = tk.BooleanVar(value=True)
    check_scroll = tk.Checkbutton(root, text="滚动加载更多数据", variable=var_scroll)
    check_scroll.grid(row=3, column=1, padx=5, pady=5)

    # 搜索结果文本框
    text_results = tk.Text(root, height=10, width=50)
    text_results.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
    root.update_idletasks() 

    # 搜索按钮
    def on_search_click():
        model = entry_model.get().strip()
        source = entry_source.get().strip()
        result = entry_result.get().strip()
        count = 0
        try:
            detection = YOLOv8(model, 0.5, 0.5)
            image_path = source
            os.makedirs(result, exist_ok=True)
            for i in glob.glob(image_path + '\\*.tif'):
                count += 1
                ori_img, frame = calculate_r_value(i)
                output_frame = detection.main(ori_img, frame)
                image_name = i.split('\\')[-1]
                cv2.imwrite(f"{result}/{image_name}", output_frame)
                text = f"{image_name} 推理完成\n"

                text_results.insert(tk.END, text)
                text_results.see(tk.END)

                root.update_idletasks() 
                text_results.see(tk.END)  # 自动滚动到底部

            # 弹窗提示推理完成
            messagebox.showinfo("完成", "推理已完成！")
        except Exception as e:
            messagebox.showerror("错误", f"搜索过程中发生错误：{e}")

    button_search = tk.Button(root, text="检测", command=on_search_click)
    button_search.grid(row=5, column=1, padx=5, pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
