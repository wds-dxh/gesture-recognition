import numpy as np
import torch as t
from model import HandModel
from torch import nn
from torchnet import meter  # 用于可视化
from torch.autograd import Variable     #自动求导
import copy

label = ["also", "attractive", "beautiful", "believe", "de", "doubt", "dream", "express", "eye", "give","handLang", "have",
         "many",
         "me", "method", "no", "only", "over", "please", "put", "say", "smile", "star", "use_accept_give", "very", "watch",
         "you"]
label_num = len(label)
# 模型保存地址即是label+.npz
targetX = [0 for xx in range(label_num)]
target = []
for xx in range(label_num):
    target_this = copy.deepcopy(targetX)
    target_this[xx] = 1
    target.append(target_this)
# 独热码

lr = 1e-3  # learning rate      #学习率
model_saved = 'checkpoints/model'

# 模型定义
model = HandModel()             #模型
optimizer = t.optim.Adam(model.parameters(), lr=lr)     #优化器
criterion = nn.CrossEntropyLoss()           #损失函数

loss_meter = meter.AverageValueMeter()# 用于可视化

epochs = 40
for epoch in range(epochs):
    print("epoch:" + str(epoch))
    loss_meter.reset()# 用于可视化
    count = 0
    allnum = 0
    for i in range(len(label)):
        data = np.load('./npz_files/' + label[i] + ".npz", allow_pickle=True)
        data = data['data']

        for j in range(len(data)):
            print(data[j])
            break
            xdata = t.tensor(data[j])
            optimizer.zero_grad()# 优化器梯度清零
            this_target = t.tensor(target[i]).float()# 独热码
            input_, this_target = Variable(xdata), Variable(this_target) # 自动求导

            output = model(input_)

            outLabel = label[output.tolist().index(max(output))]
            targetIndex = target[i].index(1)
            targetLabel = label[targetIndex]
            if targetLabel == outLabel:
                count += 1
            allnum += 1

            output = t.unsqueeze(output, 0)
            this_target = t.unsqueeze(this_target, 0)

            loss = criterion(output, this_target)
            loss.backward()
            optimizer.step()
            loss_meter.add(loss.data)

    print("correct_rate:", str(count / allnum))

    t.save(model.state_dict(), '%s_%s.pth' % (model_saved, epoch))
