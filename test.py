import torch
import torch.nn as nn
import torch.nn.functional as F

# 定义残差块
class ResidualBlock(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1):
        super(ResidualBlock, self).__init__()
        # 第一个卷积层
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)  # 批归一化层
        self.relu = nn.ReLU(inplace=True)  # ReLU激活函数
        # 第二个卷积层
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)  # 批归一化层
        # 跳跃连接
        self.downsample = nn.Sequential()  # 初始化为空
        # 如果步长不为1或输入输出通道数不同，需要调整维度
        if stride != 1 or in_channels != out_channels:
            self.downsample = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(out_channels)
            )

    def forward(self, x):
        identity = x  # 保存输入的identity

        # 第一个残差块
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)

        # 第二个残差块
        out = self.conv2(out)
        out = self.bn2(out)

        # 调整输入的维度以匹配输出
        identity = self.downsample(x)

        # 残差连接
        out += identity
        out = self.relu(out)

        return out

# 构建 CNN 模型
class ResNet(nn.Module):
    def __init__(self, num_classes=10):
        super(ResNet, self).__init__()
        # 初始卷积层、批归一化和 ReLU 激活函数
        self.conv1 = nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        self.relu = nn.ReLU(inplace=True)
        # 四个阶段的残差块序列
        self.layer1 = self.make_layer(64, 3, stride=1)
        self.layer2 = self.make_layer(128, 3, stride=2)
        self.layer3 = self.make_layer(256, 3, stride=2)
        self.layer4 = self.make_layer(512, 3, stride=2)
        # 全局平均池化层和全连接层
        self.avg_pool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(512, num_classes)

    def make_layer(self, out_channels, num_blocks, stride):
        strides = [stride] + [1] * (num_blocks - 1)
        layers = []
        for stride in strides:
            layers.append(ResidualBlock(512, out_channels, stride))
            # 更新输入通道数以便下一个残差块使用
            self.in_channels = out_channels
        return nn.Sequential(*layers)

    def forward(self, x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)

        # 通过四个阶段的残差块
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)

        x = self.avg_pool(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)

        return x

# 创建模型实例
model = ResNet()
print(model)

