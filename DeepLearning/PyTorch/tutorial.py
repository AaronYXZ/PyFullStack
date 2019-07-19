import torch

x = torch.randn(4)
w1 = torch.randn(2, 3)
print(torch.clamp(x, min = 0.0))