from onnxsim import simplify
import onnx, argparse

def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--onnx_file', type=str, default=r"./yolov8n-seg.onnx", help='data path(s)')
    
    opt = parser.parse_args()
    return opt


if __name__ == '__main__':
    opt = parse_opt()
    onnx_file = opt.onnx_file
    onnx_model = onnx.load(onnx_file)  # load onnx model
    model_simp, check = simplify(onnx_model)
    assert check, "Simplified ONNX model could not be validated"
    onnx.save(model_simp, onnx_file)
    print('finished exporting onnx')
