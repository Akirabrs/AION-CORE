import torch
import torch.nn as nn
import torch.nn.functional as F

# 1. Bloco Residual (Estilo ResNet)
class ResidualBlock(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1, downsample=None):
        super(ResidualBlock, self).__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels//4, kernel_size=1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels//4)
        self.conv2 = nn.Conv2d(out_channels//4, out_channels//4, kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels//4)
        self.conv3 = nn.Conv2d(out_channels//4, out_channels, kernel_size=1, bias=False)
        self.bn3 = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU(inplace=True)
        self.downsample = downsample

    def forward(self, x):
        residual = x
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)
        out = self.conv2(out)
        out = self.bn2(out)
        out = self.relu(out)
        out = self.conv3(out)
        out = self.bn3(out)
        if self.downsample:
            residual = self.downsample(x)
        out += residual
        out = self.relu(out)
        return out

# 2. A Rede Principal (NPE-CNN) - Teacher Brain
class NPE_Brain(nn.Module):
    def __init__(self, num_classes=4):
        super(NPE_Brain, self).__init__()
        # Entrada: Mapa do plasma (1 canal)
        self.in_channels = 64
        self.conv1 = nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        self.relu = nn.ReLU(inplace=True)
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)

        # Camadas ResNet (Profundidade)
        self.layer1 = self._make_layer(64, 3)
        self.layer2 = self._make_layer(128, 4, stride=2)
        self.layer3 = self._make_layer(256, 6, stride=2)

        # Cabeças de Saída (Multi-Task)
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        
        # Head 1: Classificação (Estável, VDE, Disrupção)
        self.fc_class = nn.Linear(256, num_classes)
        
        # Head 2: Regressão (Ganhos Kp, Kd ótimos para o FPGA)
        self.fc_regress = nn.Linear(256, 2) 
        
        # Head 3: PSQ (Predictive Safety Quotient / Incerteza)
        self.fc_uncertainty = nn.Linear(256, 1)

    def _make_layer(self, out_channels, blocks, stride=1):
        downsample = None
        if stride != 1 or self.in_channels != out_channels:
            downsample = nn.Sequential(
                nn.Conv2d(self.in_channels, out_channels, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(out_channels),
            )
        layers = []
        layers.append(ResidualBlock(self.in_channels, out_channels, stride, downsample))
        self.in_channels = out_channels
        for _ in range(1, blocks):
            layers.append(ResidualBlock(self.in_channels, out_channels))
        return nn.Sequential(*layers)

    def forward(self, x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)

        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)

        x = self.avgpool(x)
        x = torch.flatten(x, 1)

        # Saídas para o Aluno (FPGA)
        class_out = self.fc_class(x)      # Diagnóstico
        regress_out = self.fc_regress(x)  # Ganhos Sugeridos [Kp, Kd]
        psq = torch.sigmoid(self.fc_uncertainty(x)) # PSQ (Confiança 0-1)
        
        return regress_out, psq
