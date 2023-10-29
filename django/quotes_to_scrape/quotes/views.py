from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator

from .forms import QuoteForm, AuthorForm, TagForm
from .models import Author, Tag
from utils.mongo_migration import Quote as QuoteMongo


# Create your views here.
def main(request, page=1):
    quotes = QuoteMongo.objects()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(request, "quotes/index.html", context={"quotes": quotes_on_page})


@login_required
def tag(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()
            return redirect(to="quotes:root")
        else:
            return render(request, "quotes/tag.html", {"form": form})

    return render(request, "quotes/tag.html", {"form": TagForm()})


@login_required
def author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            author = form.save(commit=False)
            author.user = request.user
            author.save()
            return redirect(to="quotes:root")
        else:
            return render(request, "quotes/author.html", {"form": form})

    return render(request, "quotes/author.html", {"form": AuthorForm()})


@login_required
def quote(request):
    tags = Tag.objects.all()

    if request.method == "POST":
        form = QuoteForm(request.POST)

        if form.is_valid():
            new_quote = form.save(commit=False)
            new_quote.user = request.user
            new_quote.save()
            choice_tags = Tag.objects.filter(name__in=request.POST.getlist("tags"))
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)

            return redirect(to="quotes:root")
        else:
            return render(
                request,
                "quotes/quote.html",
                {"tags": tags, "form": form},
            )

    return render(
        request,
        "quotes/quote.html",
        {"tags": tags, "form": QuoteForm()},
    )


def about(request, author_id):
    author = get_object_or_404(Author, pk=author_id)

    return render(request, "quotes/about.html", {"author": author})
