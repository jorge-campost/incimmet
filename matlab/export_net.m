incimmetNet = load('RedEnrenada_SegSeman.mat');
incimmetNet

exportONNXNetwork(incimmetNet.net,'incimmet-net.onnx');
