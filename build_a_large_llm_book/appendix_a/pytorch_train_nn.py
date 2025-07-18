import torch
import torch.nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torch.utils.data import Dataset

class NeuralNetwork(torch.nn.Module):
    def __init__(self, num_inputs, num_outputs):
        super().__init__()

        self.layers = torch.nn.Sequential(

            # 1st hidden layer
            torch.nn.Linear(num_inputs, 30),
            torch.nn.ReLU(),

            # 2nd hidden layer
            torch.nn.Linear(30, 20),
            torch.nn.ReLU(),

            # output layer
            torch.nn.Linear(20, num_outputs),
        )

    def forward(self, x):
        logits = self.layers(x)
        return logits

x_train = torch.tensor([
    [-1.2, 3.1],
    [-0.9, 2.9],
    [-0.5, 2.6],
    [2.3, -1.1],
    [2.7, -1.5]
])

y_train = torch.tensor([0, 0, 0, 1, 1])

x_test = torch.tensor([
    [-0.8, 2.8],
    [2.6, -1.6]
])

y_test = torch.tensor([0,1])

torch.manual_seed(123)

class ToyDataset(Dataset):
    def __init__(self, x, y):
        self.features = x
        self.labels = y

    def __getitem__(self, index):
        one_x = self.features[index]
        one_y = self.labels[index]
        return one_x, one_y

    def __len__(self):
        return self.labels.shape[0]

train_ds = ToyDataset(x_train, y_train)
test_ds = ToyDataset(x_test, y_test)


train_loader = DataLoader(
    dataset=train_ds,
    batch_size=2,
    shuffle=True,
    num_workers=0,
    drop_last=True
)

test_laoder = DataLoader(
    dataset=test_ds,
    batch_size=2,
    shuffle=False,
    num_workers=0
)

for idx, (x, y) in enumerate(train_loader):
    print(f"Batch {idx+1}:", x, y)


model = NeuralNetwork(num_inputs=2, num_outputs=2)
optimizer = torch.optim.SGD(
    model.parameters(), lr=0.5
)

num_epochs = 3
for epoch in range (num_epochs):
    model.train()
    
    for batch_idx, (features, labels) in enumerate(train_loader):
        logits = model(features)
        loss = F.cross_entropy(logits, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        ### LOGGING
        print (f"Epoch: {epoch+1:03d}/{num_epochs:03d}"
               f" | Batch {batch_idx:03d}/{len(train_loader) :03d}"
               f" | Train Loss: {loss:.2f}")

    model.eval()


model.eval()
with torch.no_grad():
    outputs = model(x_train) 
print(outputs)

torch.set_printoptions(sci_mode=False)
probas = torch.softmax(outputs, dim=1)
print (probas)

predictions = torch.argmax(probas, dim=1)
print(predictions)

predictions = torch.argmax(outputs, dim=1)
print(predictions)

print(predictions == y_train)

print (torch.sum(predictions == y_train))
