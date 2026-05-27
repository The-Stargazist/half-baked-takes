import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from blog.models import Post

User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: admin / admin123')

samples = [
    dict(title='Why I started writing publicly', slug='why-i-started-writing', category='general',
         summary='A few months ago I decided to start putting thoughts into words. Here is why.',
         content='## The push\n\nI\'ve been keeping notes for years — scattered across Notion, Apple Notes, and random text files. At some point I realized none of it was ever being revisited.\n\nWriting publicly forces clarity. When you know someone *might* read it, you stop being sloppy with your thinking.\n\n## What this blog is\n\nNo particular niche. Just things I find worth writing about: projects, papers, half-formed ideas, occasional rants.'),
    dict(title='Training runs and weekend experiments', slug='training-runs-experiments', category='general',
         summary='Notes from a weekend of running small experiments just to see what breaks.',
         content='## Saturday\n\nSpun up a quick experiment to test something I\'d been wondering about. Broke immediately. Spent two hours debugging a shape mismatch that turned out to be a transposed matrix.\n\n## Sunday\n\nActually got it working. The results were boring, which is its own kind of useful — rules out a whole class of approaches.'),
    dict(title='Current reading list', slug='current-reading-list', category='general',
         summary='What is on my desk right now and what I\'m hoping to get out of each.',
         content='## Books\n\n- *The Information* — James Gleick\n- *Thinking, Fast and Slow* — Kahneman (rereading)\n\n## Papers\n\nSee the Research section for proper writeups.'),
    dict(title='Attention Is All You Need — a close read', slug='attention-is-all-you-need', category='research',
         summary='What the transformer paper actually says, what surprised me, and what I think people misread.',
         content='## Background\n\nI\'d "read" this paper twice before without really reading it. Third time through, with a pen, was different.\n\n## What surprised me\n\nThe multi-head attention formulation is cleaner than I remembered. The real insight is that running attention in parallel across multiple subspaces is cheap and empirically powerful.\n\n## What gets misread\n\nPeople treat the positional encodings as an afterthought. They\'re not — without them the architecture is completely permutation invariant and loses all sequential structure.'),
    dict(title='Scaling Laws — what the Chinchilla paper changed', slug='chinchilla-scaling-laws', category='research',
         summary='The Hoffmann et al. paper rewrote the conventional wisdom on compute-optimal training.',
         content='## The claim\n\nFor a given compute budget, you should train a *smaller* model on *more* data than was common practice. The optimal ratio is roughly 1:1 tokens to parameters.\n\n## Why it matters\n\nGPT-3 was undertrained relative to its size. Chinchilla (same compute, smaller model, more data) outperformed it. This reshaped how every major lab thinks about training runs.'),
    dict(title='Flash Attention — reading the engineering', slug='flash-attention', category='research',
         summary='Less about the math, more about why the IO-awareness is the actual insight.',
         content='## The idea\n\nStandard attention materializes the full N×N attention matrix in HBM. FlashAttention avoids this by tiling the computation so it stays in SRAM.\n\n## Why this is hard\n\nSRAM is fast but tiny (~20MB on an A100 vs 80GB HBM). The tiling algorithm has to be carefully designed so the partial results can be combined correctly without materializing the full matrix.'),
    dict(title='Backtester — trading strategy simulator', slug='backtester-trading', category='projects',
         summary='Built a modular backtesting framework for algorithmic trading strategies from scratch.',
         content='## What it does\n\nTakes historical price data, runs a strategy function over it tick-by-tick, tracks positions and PnL, and spits out performance metrics.\n\n## Architecture\n\n```python\nclass Strategy:\n    def on_tick(self, state: MarketState) -> list[Order]:\n        ...\n```\n\nEach strategy implements `on_tick`. The engine feeds it market data and collects orders. Simple, composable, easy to test.\n\n## What I learned\n\nSlippage modelling is where most backtests lie to you. Getting it wrong makes everything look better than it is.'),
    dict(title='Minimal neural net from scratch', slug='neural-net-scratch', category='projects',
         summary='Implemented backprop and a small MLP using only NumPy to make sure I actually understand it.',
         content='## Motivation\n\nI\'d used PyTorch for two years without being able to correctly derive the backward pass from scratch. That bothered me.\n\n## What I built\n\nA small autograd engine — basically micrograd — then a two-layer MLP trained on MNIST. Reached ~97.8% accuracy.\n\n## The thing that finally clicked\n\nThe chain rule isn\'t magic. Once you see it as "how much does this node\'s output affect the loss, given everything downstream", the code writes itself.'),
    dict(title='This blog — design and stack', slug='this-blog-stack', category='projects',
         summary='How this site is built, why I picked Django, and what I\'d do differently.',
         content='## Stack\n\n- **Django** — batteries included, I know it well\n- **SQLite** — more than enough for a personal blog\n- **Vanilla CSS** — no framework, just custom properties and a bit of care\n\n## What I\'d do differently\n\nProbably add full-text search earlier. Right now I\'m just filtering by category.'),
]

for s in samples:
    if not Post.objects.filter(slug=s['slug']).exists():
        Post.objects.create(**s)
        print(f"Created: {s['title']}")

print('Done.')
