import sys
import torch
from tool.darknet2pytorch import Darknet


def transform_to_onnx(cfgfile, weightfile, batch_size=1):
    model = Darknet(cfgfile)

    model.print_network()
    model.load_weights(weightfile)
    print('Loading weights from %s... Done!' % (weightfile))

    # model.cuda()

    x = torch.randn((batch_size, 3, model.height, model.width), requires_grad=True)  # .cuda()

    onnx_file_name = "yolov4.onnx"

    # Export the model
    print('Export the onnx model ...')
    torch.onnx.export(model,
                      x,
                      onnx_file_name,
                      export_params=True,
                      opset_version=11,
                      do_constant_folding=True,
                      input_names=['input'], output_names=['output'],
                      dynamic_axes={
                          'input': {0: 'batch_size'},
                          'output': {0: 'batch_size'},
                        })

    print('Onnx model exporting done')
    return onnx_file_name


if __name__ == '__main__':
    if len(sys.argv) == 3:
        cfgfile = sys.argv[1]
        weightfile = sys.argv[2]
        transform_to_onnx(cfgfile, weightfile)
    elif len(sys.argv) == 4:
        cfgfile = sys.argv[1]
        weightfile = sys.argv[2]
        batch_size = int(sys.argv[3])
        transform_to_onnx(cfgfile, weightfile, batch_size)
    else:
        print('Please execute this script this way:\n')
        print('  python darknet2onnx.py <cfgFile> <weightFile>')
        print('or')
        print('  python darknet2onnx.py <cfgFile> <weightFile> <batchSize>')
