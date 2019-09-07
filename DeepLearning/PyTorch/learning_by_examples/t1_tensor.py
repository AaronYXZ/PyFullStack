import torch

"""
manually implement both the forward and backward passes without using tensor's autograd
"""

dtype = torch.float
device = torch.device("cpu")

# N is batch size; D_in is input dimension;
# H is hidden dimension; D_out is output dimension.
N, D_in, H, D_out = 64, 1000, 100, 10

# create random input and output data
x = torch.randn(N, D_in, device = device, dtype = dtype)
y = torch.randn(N, D_out, device = device, dtype = dtype)

# Randomly initialize weights
w1 = torch.randn(D_in, H, device=device, dtype=dtype)
w2 = torch.randn(H, D_out, device=device, dtype=dtype)

learning_rate = 1e-6

for t in range(5000):
    # forward pass: compute predicted y
    h = x.mm(w1) #h.size() == (N, H)
    h_relu = h.clamp(min = 0)
    y_pred = h_relu.mm(w2)

    # compute and print loss
    loss = (y_pred - y).pow(2).sum().item()
    # print(t, loss)

    # Backprop to compute gradients of w1 and w2 with respect to loss
    grad_y_pred = 2.0 * (y_pred - y)
    grad_w2 = h_relu.t().mm(grad_y_pred)
    grad_h_relu = torch.mm(grad_y_pred, w2.t())
    grad_h = grad_h_relu.clone()
    grad_h[h < 0] = 0
    grad_w1 = torch.mm(x.t(), grad_h)

    # update weights using gradient descent
    w1 -= learning_rate * grad_w1
    w2 -= learning_rate * grad_w2

    if t % 100 == 0:
        print(loss)
    if t == 4999:
        print(loss)




