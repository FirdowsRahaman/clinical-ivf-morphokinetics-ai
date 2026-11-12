"""Multi-Class Blastocyst Segmentation Architecture (Attention U-Net)
Segmenting Zona Pellucida (ZP), Inner Cell Mass (ICM), Trophectoderm (TE), and Blastocoel Cavity.
Designed for clinical microscopic embryology time-lapse imaging.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F

class ConvBlock(nn.Module):
    def __init__(self, in_channels: int, out_channels: int):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.conv(x)

class AttentionGate(nn.Module):
    def __init__(self, f_g: int, f_l: int, f_int: int):
        super().__init__()
        self.w_g = nn.Sequential(
            nn.Conv2d(f_g, f_int, kernel_size=1, stride=1, padding=0, bias=True),
            nn.BatchNorm2d(f_int)
        )
        self.w_x = nn.Sequential(
            nn.Conv2d(f_l, f_int, kernel_size=1, stride=1, padding=0, bias=True),
            nn.BatchNorm2d(f_int)
        )
        self.psi = nn.Sequential(
            nn.Conv2d(f_int, 1, kernel_size=1, stride=1, padding=0, bias=True),
            nn.BatchNorm2d(1),
            nn.Sigmoid()
        )
        self.relu = nn.ReLU(inplace=True)

    def forward(self, g: torch.Tensor, x: torch.Tensor) -> torch.Tensor:
        g1 = self.w_g(g)
        x1 = self.w_x(x)
        psi = self.relu(g1 + x1)
        psi = self.psi(psi)
        return x * psi

class EmbryoAttentionUNet(nn.Module):
    """Attention U-Net tailored for blastocyst morphology segmentation:
    Classes:
      0: Background
      1: Zona Pellucida (ZP)
      2: Inner Cell Mass (ICM) - critical for fetus development
      3: Trophectoderm (TE) - critical for placental development
      4: Blastocoel Cavity
    """
    def __init__(self, in_channels: int = 1, num_classes: int = 5):
        super().__init__()
        self.enc1 = ConvBlock(in_channels, 32)
        self.pool1 = nn.MaxPool2d(2)
        self.enc2 = ConvBlock(32, 64)
        self.pool2 = nn.MaxPool2d(2)
        self.enc3 = ConvBlock(64, 128)
        self.pool3 = nn.MaxPool2d(2)

        self.bottleneck = ConvBlock(128, 256)

        self.up3 = nn.ConvTranspose2d(256, 128, kernel_size=2, stride=2)
        self.att3 = AttentionGate(f_g=128, f_l=128, f_int=64)
        self.dec3 = ConvBlock(256, 128)

        self.up2 = nn.ConvTranspose2d(128, 64, kernel_size=2, stride=2)
        self.att2 = AttentionGate(f_g=64, f_l=64, f_int=32)
        self.dec2 = ConvBlock(128, 64)

        self.up1 = nn.ConvTranspose2d(64, 32, kernel_size=2, stride=2)
        self.att1 = AttentionGate(f_g=32, f_l=32, f_int=16)
        self.dec1 = ConvBlock(64, 32)

        self.final_conv = nn.Conv2d(32, num_classes, kernel_size=1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        e1 = self.enc1(x)
        e2 = self.enc2(self.pool1(e1))
        e3 = self.enc3(self.pool2(e2))

        b = self.bottleneck(self.pool3(e3))

        d3 = self.up3(b)
        x3 = self.att3(g=d3, x=e3)
        d3 = self.dec3(torch.cat((x3, d3), dim=1))

        d2 = self.up2(d3)
        x2 = self.att2(g=d2, x=e2)
        d2 = self.dec2(torch.cat((x2, d2), dim=1))

        d1 = self.up1(d2)
        x1 = self.att1(g=d1, x=e1)
        d1 = self.dec1(torch.cat((x1, d1), dim=1))

        return self.final_conv(d1)
