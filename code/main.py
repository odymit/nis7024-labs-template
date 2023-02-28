from typing import Any
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision import datasets
import torchvision.transforms as transforms
import lightning as L

# define your victim model
class Model(L.LightningModule):
    def __init__(self, num_class, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.num_class = num_class
        self.features = nn.Sequential(
                        nn.Conv2d(1, 16, 5),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(16, 32, 5),
            nn.ReLU(),
            nn.MaxPool2d(2, 2)
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(32 * 4 * 4, 512),
            nn.Linear(512, self.num_class)
        )

    def forward(self, x):
        x = self.features(x)
        return self.classifier(x)

    def training_step(self, batch, batch_idx):
        x, y = batch
        logits = self.forward(x)
        loss = F.cross_entropy(logits, y)
        return loss
    
    def test_step(self, batch, batch_idx): 
        # test loop
        x, y = batch
        feats = self.features(x)
        logits = self.classifier(feats)
        loss = F.cross_entropy(logits, y)

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=1e-3)
        return optimizer


# define your attack
class Attack():
    
    def attack(self, input):
        # implement your attack method here
        mal_input = input
        return mal_input


# define your detector
class Detector():

    def detect(self, input):
        # implement your detect method here 
        detect_results = input
        return False
    

# collect everything you need here
class Parameters(object):
    def __init__(self) -> None:
        # define and get your dataset
        self.transform = transforms.ToTensor()
        self.train_set = datasets.MNIST(root="../dataset", download=True, train=True, transform=self.transform)
        self.train_loader = DataLoader(self.train_set)
        self.test_set = datasets.MNIST(root="../dataset", download=True, train=False, transform=self.transform)
        self.test_loader = DataLoader(self.test_set)
        # get your victim model instance 
        self.model = Model(num_class=10)
        # define your attack
        self.attack = Attack().attack
        # define your detector
        self.detect = Detector().detect


# do all your process here
def train(params):
    # train your victim model
    trainer = L.Trainer(fast_dev_run=True)
    trainer.fit(params.model, params.train_loader)
    trainer.test(params.model, params.test_loader)

    # implement input modify attack as below
    for batch_idx, (x, y) in enumerate(params.train_loader):
        y_normal = params.model(x)
        y_malicious = params.model(params.attack(x))
        break

    # implement model retrain attack as below
    params.model = params.attack(params.model)


    # implement your sample detection as below
    for batch_idx, (x, y) in enumerate(params.train_loader):
        is_malicious = params.detect(x)
        if is_malicious:
            # drop x
            continue
        break
    # implement your model detection as below
    is_malicious = params.detect(params.model)


if __name__ == '__main__':
    params = Parameters()
    train(params)