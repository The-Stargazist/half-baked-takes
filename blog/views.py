import json as _json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.utils import timezone
from django.contrib import messages
import markdown as md
from .models import Post, SiteConfig
from .forms import PostForm, SiteConfigForm


def _auto_publish_scheduled():
    """Flip published=True for any scheduled posts whose time has come."""
    Post.objects.filter(published=False, publish_at__lte=timezone.now()).update(published=True, publish_at=None)


def homepage(request):
    _auto_publish_scheduled()
    published = Post.objects.filter(published=True)
    general  = list(published.filter(category='general')[:3])
    research = list(published.filter(category='research')[:3])
    projects = list(published.filter(category='projects')[:3])

    used_pks = {p.pk for p in general + research + projects}
    overflow = list(published.exclude(pk__in=used_pks))
    for section in [general, research, projects]:
        while len(section) < 3 and overflow:
            section.append(overflow.pop(0))

    drafts = Post.objects.filter(published=False, publish_at=None).order_by('-created_at') if request.user.is_authenticated else []
    scheduled = Post.objects.filter(published=False, publish_at__isnull=False).order_by('publish_at') if request.user.is_authenticated else []

    return render(request, 'blog/home.html', {
        'general': general,
        'research': research,
        'projects': projects,
        'drafts': drafts,
        'scheduled': scheduled,
    })


def post_detail(request, slug):
    _auto_publish_scheduled()
    if request.user.is_authenticated:
        post = get_object_or_404(Post, slug=slug)
    else:
        post = get_object_or_404(Post, slug=slug, published=True)
    content_html = md.markdown(post.content, extensions=['fenced_code', 'tables', 'nl2br'])
    related = Post.objects.filter(category=post.category, published=True).exclude(pk=post.pk)[:3]
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'content_html': content_html,
        'related': related,
    })


def category_list(request, category):
    label_map = {'general': 'General', 'research': 'Research', 'projects': 'Projects'}
    if category not in label_map:
        return redirect('home')
    posts = Post.objects.filter(category=category, published=True)
    return render(request, 'blog/category_list.html', {
        'posts': posts,
        'category': category,
        'category_label': label_map[category],
    })


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            if not post.slug:
                post.slug = slugify(post.title)
            # If scheduled, ensure not marked published yet
            if post.publish_at and post.publish_at > timezone.now():
                post.published = False
                messages.success(request, f'Post scheduled for {post.publish_at.strftime("%b %d, %Y at %H:%M IST")}.')
            elif post.published:
                messages.success(request, 'Post published.')
            else:
                messages.success(request, 'Draft saved.')
            post.save()
            return redirect(post.get_absolute_url())
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form, 'action': 'New Post'})


@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            updated = form.save(commit=False)
            if updated.publish_at and updated.publish_at > timezone.now():
                updated.published = False
                messages.success(request, f'Post scheduled for {updated.publish_at.strftime("%b %d, %Y at %H:%M IST")}.')
            elif updated.published:
                messages.success(request, 'Post updated & published.')
            else:
                messages.success(request, 'Draft saved.')
            updated.save()
            return redirect(post.get_absolute_url())
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form, 'action': 'Edit Post', 'post': post})


@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted.')
        return redirect('home')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})


@login_required
def site_settings(request):
    config = SiteConfig.get()
    if request.method == 'POST':
        form = SiteConfigForm(request.POST, request.FILES, instance=config)
        if form.is_valid():
            cfg = form.save(commit=False)
            raw = request.POST.get('socials_data', '[]')
            try:
                socials = _json.loads(raw)
            except (_json.JSONDecodeError, ValueError):
                socials = []
            cfg.set_socials(socials)
            cfg.save()
            messages.success(request, 'Profile updated.')
            return redirect('home')
    else:
        form = SiteConfigForm(instance=config)
    socials = config.get_socials()
    return render(request, 'blog/settings.html', {
        'form': form,
        'config': config,
        'socials': socials,
        'socials_json': _json.dumps(socials),
    })
