import torch

from torch import nn
import torchvision.datasets as dsets
import torchvision.transforms as transforms
import matplotlib.pyplot as plt

torch.manual_seed(1) # reproducible

# HYPER PARAMETERS

EPOCH = 1
BATCH_SIZE = 64
TIME_STEP = 28
INPUT_SIZE = 28
LR = 0.01
DOWNLOAD_MNIST = False

# MNIST 手写数字
train_data = dsets.MNIST(
    root = "./mnist/",
    train = True,
    transform=transforms.ToTensor(),
    download=DOWNLOAD_MNIST
)

# plot one example

print(train_data.data.size()) # 60,000, 28, 28)
print(train_data.targets.size()) # 60,000
plt.imshow(train_data.data[0].numpy(), cmap = "gray")
# plt.show()

# Data loader for easy mini-batch return in training
train_loader = torch.utils.data.DataLoader(dataset = train_data, batch_size = BATCH_SIZE, shuffle = True)

# convert test data into variable, pick 2000 samples to speed up testing
test_data = dsets.MNIST(root = "./mnist/", train = False, transform=transforms.ToTensor())
test_x = test_data.data.type(torch.FloatTensor)[:2000] / 255. # 2000, 28, 28
test_y = test_data.targets.numpy()[:2000]


class RNN(nn.Module):
    def __init__(self):
        super(RNN, self).__init__()

        self.rnn = nn.LSTM(
            input_size=INPUT_SIZE,
            hidden_size= 64,
            num_layers=1,
            batch_first=True
        )

        self.out = nn.Linear(64, 10)

    def forward(self, x):
        # x shape (batch, time_step, input_size)
        # r_out shape (batch, time_step, output_size)
        # h_n shape (n_layers, batch, hidden_size) LSTM 有两个hidden states, h_n是分线， h_c是主线
        r_out, (h_n, h_c) = self.rnn(x, None)
        out = self.out(r_out[:, -1, :])         # 这里 r_out[:, -1, :] 的值也是 h_n 的值
        return out

rnn = RNN()
print(rnn)

optimizer = torch.optim.Adam(rnn.parameters(), lr = LR)
loss_func = nn.CrossEntropyLoss()

for epoch in range(EPOCH):
    for step, (b_x, b_y) in enumerate(train_loader):
        b_x = b_x.view(-1, 28, 28) # reshape to batch, time_step, input_size

        output = rnn(b_x)
        loss = loss_func(output, b_y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if step % 50 == 0:
            test_output = rnn(test_x)
            pred_y = torch.max(test_output, 1)[1].data.numpy()
            accuracy = float((pred_y == test_y).astype(int).sum()) / float(test_y.size)
            print('Epoch: ', epoch, '| train loss: %.4f' % loss.data.numpy(), '| test accuracy: %.2f' % accuracy)

test_output = rnn(test_x[:10].view(-1, 28,28))
pred_y = torch.max(test_output, 1)[1].data.numpy()
print(pred_y, "prediction number")
print(test_y[:10], "real number")