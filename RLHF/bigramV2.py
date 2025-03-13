import torch
import torch.nn as nn 
from torch.nn import functional as F

# define the hyperparameters 
batch_size = 64 # independent sequences will be parallelly processed  
block_size = 256 # maximum context lenght for predicitons 
max_iters = 5000 
eval_interval = 500 
learning_rate = 3e-4 
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(device)
print('8-' * 6)
eval_iters = 200 
n_embed = 384

n_head= 8
n_layer = 8
dropout = 0.2

torch.manual_seed(1337)

# read it in to inspect it
with open('input.txt', 'r', encoding='utf-8') as f:
    text = f.read()
    
chars = sorted(list(set(text)))
vocab_size = len(chars)
stoi = {ch:i for i,ch in enumerate(chars)}
itos = {i:ch for i,ch in enumerate(chars)}
encode = lambda s: [stoi[c] for c in s] # encoder: take a string, output a list of integers 
decode = lambda n: ''.join([itos[i] for i in n]) # decoder: take a numbers, output a list of string 

#Train test split 
data = torch.tensor(encode(text), dtype=torch.long) # convert text strings in to long torch tensors
n = int(0.9*len(data)) # grap 90% of the data
train_data = data[:n] # take 90% of data for training 
val_data = data[n:] # take the rest 10% of data for validation 

# loading the data and preparing batches
def get_batch(split):
    data = train_data if split =='train' else val_data
    ix = torch.randint(len(data)-block_size, (batch_size,))
    x = torch.stack([data[i:i+block_size] for i in ix])
    y = torch.stack([data[i+1:i+block_size+1] for i in ix])
    x, y = x.to(device), y.to(device)
    return x, y 

@torch.no_grad()
def estimate_loss():
    out = {}
    model.eval()
    for split in ['train', 'val']:
        losses = torch.zeros(eval_iters)
        for k in range(eval_iters):
            X, Y = get_batch(split) 
            logits, loss = model(X, Y)
            losses[k] = loss.item()
        out[split] = losses.mean()
    model.train()
    return out 

class Head(nn.Module):
    def __init__(self, head_size):
        super().__init__()
        self.key = nn.Linear(n_embed, head_size, bias=False)
        self.query = nn.Linear(n_embed, head_size, bias=False)
        self.value = nn.Linear(n_embed, head_size, bias=False)
        self.register_buffer('tril', torch.tril(torch.ones(block_size, block_size)))
        self.dropout = nn.Dropout(dropout)
        
    def forward(self, x):
        B, T, C = x.shape
        k = self.key(x) # (B, T, C)
        q = self.query(x) # (B, T, C)
        #Compute the attention scores (affinities)
        wei = q @ k.transpose(-2, -1) * C ** -0.5 # (B, T, C) * (B, C, T) --> (B, T, T)
        wei = wei.masked_fill(self.tril[:T, :T] == 0, float('-inf'))
        wei = F.softmax(wei, dim=-1)
        wei = self.dropout(wei)
        v = self.value(x) # (B,T,C)
        out = wei @ v # (B, T, T) @ (B, T, C ) --> (B, T, C)
        return out 

class MultiHeadAttention(nn.Module):
    def __init__(self, num_heads, head_size):
        super().__init__()
        self.heads = nn.ModuleList([Head(head_size) for _ in range(num_heads)])
        self.proj = nn.Linear(n_embed, n_embed)
        self.dropout = nn.Dropout(dropout)
        
    def forward(self, x):
        out = torch.cat([h(x) for h in self.heads], dim=-1) 
        out = self.proj(out)
        return out
        
class FeedForward(nn.Module):
    def __init__(self, n_embed):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(n_embed, 4 * n_embed),
            nn.ReLU(),
            nn.Linear(4 * n_embed, n_embed),
            nn.Dropout(dropout),
        )
    def forward(self, x):
        return self.net(x)
        
class Block(nn.Module):
    #communication fd by computation 
    def __init__(self, n_embd, n_head):
        #n_embd: embedding dimension, n_head: number of heads
        super().__init__() 
        head_size = n_embd // n_head
        self.sa = MultiHeadAttention(n_head, head_size)
        self.ffwd = FeedForward(n_embd) 
        self.ln1 = nn.LayerNorm(n_embed)
        self.ln2 = nn.LayerNorm(n_embed) # 32 
        
    def forward(self, x):
        x = x + self.sa(self.ln1(x))
        x = x + self.ffwd(self.ln2(x))
        return x 


class BatchNorm1d:
    def __init__(self, dim, eps=1e-5, momentum=0.1):
        self.eps = eps 
        self.gamma = torch.ones(dim)
        self.beta = torch.zeros(dim) 
        
    def __call__(self, x):
        xmean = x.mean(1, keepdim=True) # batch mean 
        xvar = x.var(1, keepdim=True) # batch variance
        xhat = (x-xmean) / torch.sqrt(xvar + self.eps) # normalize to unit variance 
        self.out = self.gamma * xhat + self.beta 
        return self.out 
    
    def parameters(self):
        return [self.gamma, self.beta] 
    
torch.manual_seed(1337)
module = BatchNorm1d(100)
x = torch.randn(32, 100) # batch size 32 of 100 dim vectors
x = module(x)
print(x.shape)



class BigramLanguageModel(nn.Module):
    def __init__(self ):
        super().__init__()
        self.token_embedding_table = nn.Embedding(vocab_size, n_embed) # each token reads off the logits for the next token from a lookup table 
        self.position_embedding_table = nn.Embedding(block_size, n_embed)
        # self.sa_head = MultiHeadAttention(4, n_embed//4) # 4 heads of 8-Dim
        # self.ffwd = FeedForward(n_embed)
        # self.lm_head = nn.Linear(n_embed, vocab_size)
        # self.blocks = nn.Sequential(
        #     Block(n_embed, n_head=4),
        #     Block(n_embed, n_head=4),
        #     Block(n_embed, n_head=4),
        #     nn.LayerNorm(n_embed),
        # )
        self.blocks = nn.Sequential(*[Block(n_embed, n_head=n_head) for _ in range(n_layer)])
        self.ln_f = nn.LayerNorm(n_embed) # final layer norm
        self.lm_head = nn.Linear(n_embed, vocab_size)
        
    def forward(self, idx, targets=None):
        B, T = idx.shape
        token_embed = self.token_embedding_table(idx) # B,T,C ..> idx and targets are both (B,T) Tensor fo t ineterers  C embed 
        pos_emb = self.position_embedding_table(torch.arange(T, device=device)) # T,C
        x = token_embed + pos_emb # B,T,C 
        # x = self.sa_head(x) # apply one head self attenation . (B, T, C)
        # x = self.ffwd(x) # (B,T,C)
        x = self.blocks(x) # (B, T, C)
        x = self.ln_f(x) # (B, T, C)
        logits = self.lm_head(x) # (B, T, C) C vocab size
        
        #measure a loss usin negative log
        if targets is None:
            loss = None 
        else:
            
            B,T,C = logits.shape 
            logits = logits.view(B*T, C)
            targets = targets.view(B*T)
            loss = F.cross_entropy(logits, targets)
        
        return logits, loss
   
    
    def generate(self, idx, max_new_tokens):
        #idx is (B, T) array of indices in the current context 
        for _ in range(max_new_tokens):
            idx_cond = idx[:, -block_size:]
            logits, loss = self(idx_cond) # get predicitons
            logits = logits[:, -1, :] # last time step >>> (B,C) 
            probs = F.softmax(logits, dim=-1) # get probabilities (B,C)
            idx_next = torch.multinomial(probs, num_samples=1) # (B,1) -- sample from the distribution 
            idx = torch.cat((idx, idx_next), dim=1) # (B, T+1) .. append sampled index to the running sequence 
        return idx 
    
    
model = BigramLanguageModel()
print(device, '*' * 3)
print(model)
m = model.to(device)
print(m)
print('Model is running on: ', device)
    
    
optimizer = torch.optim.AdamW(m.parameters(), lr=1e-3)

for iter in range(max_iters):
    if iter%eval_interval == 0:
        losses = estimate_loss()
        print(f"step {iter}: train loss {losses['train']:.4f}, val loss {losses['val']:.4f}")
        
    xb, yb = get_batch('train')
    
    #evaluate 
    logits, loss = model(xb, yb)
    optimizer.zero_grad() #optimizer.zero_grad(set_to_none=True)
    loss.backward()
    optimizer.step()
    
    
    

# generate the context 
context = torch.zeros((1,1), dtype=torch.long, device=device) 
print(decode(m.generate(context, max_new_tokens=500)[0].tolist()))