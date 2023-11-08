from django.shortcuts import render, redirect
from .models import Category, Item
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import FilterForm
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Count
from cart.forms import CartAddItemForm


def index(request):
    return render(request, "catalog/pages/index.html")


class CatalogView(ListView):
    template_name = "catalog/pages/catalog.html"
    context_object_name = "items"
    paginate_by = 9

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        self.paginator = Paginator(self.object_list, self.paginate_by)
        page_number = request.GET.get("page")
        self.page = self.paginator.get_page(page_number)
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_queryset(self):
        sort_param = self.request.GET.get("sort_by", None)
        queryset = Item.objects.filter(availability=True).order_by(
            "-number_of_views", "-number_of_sales"
        )
        if sort_param == "price":
            queryset = Item.objects.filter(availability=True).order_by("-price")
        elif sort_param == "number_of_views":
            queryset = Item.objects.filter(availability=True).order_by(
                "-number_of_views"
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page"] = self.page
        context["quantity"] = len(self.get_queryset())
        return context


class CategoryView(ListView):
    model = Item
    template_name = "catalog/pages/catalog.html"
    context_object_name = "items"
    paginate_by = 9

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        self.paginator = Paginator(self.object_list, self.paginate_by)
        page_number = request.GET.get("page")
        self.page = self.paginator.get_page(page_number)
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_queryset(self):
        cat = self.kwargs["cat_slug"]
        queryset = Item.objects.filter(category__slug=cat, availability=True)
        sort_param = self.request.GET.get("sort_by")

        if sort_param == "price":
            queryset = queryset.order_by("-price")
        elif sort_param == "number_of_views":
            queryset = queryset.order_by("-number_of_views")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.filter(slug=self.kwargs["cat_slug"])
        cat_title = category[0].title
        cat_text = category[0].description
        context["page"] = self.page
        context["quantity"] = len(self.get_queryset())
        context["title"] = cat_title
        context["text"] = cat_text
        return context


def product_filter(request):
    paginate_by = 9
    form = FilterForm(request.GET)
    items = Item.objects.filter(availability=True)

    if form.is_valid():
        cat = form.cleaned_data.get("cat")
        min_price = form.cleaned_data.get("min_price")
        max_price = form.cleaned_data.get("max_price")
        materials = request.GET.getlist("material")
        collections = request.GET.getlist("collection")

        if min_price is not None and min_price:
            items = items.filter(price__gte=min_price)
        if max_price is not None and max_price:
            items = items.filter(price__lte=max_price)
        if cat and cat != "0":
            items = items.filter(category_id=cat)

        if materials:
            items = items.filter(material__in=materials)

        if collections:
            items = items.filter(collection__in=collections)

        sort_param = request.GET.get("sort_by", None)
        if sort_param == "price":
            items = items.order_by("-price")
        elif sort_param == "number_of_views":
            items = items.order_by("-number_of_views")

        if not (min_price or max_price or materials or collections):
            category = Category.objects.get(title=cat)
            cat_slug = category.slug
            return HttpResponseRedirect(
                reverse("catalog_app:category", args=[cat_slug])
            )

    else:
        print(form.errors)

    paginator = Paginator(items, paginate_by)
    page_num = request.GET.get("page", 1)
    page = paginator.get_page(page_num)

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    context = {
        "items": items,
        "form": form,
        "page": page,
        "quantity": len(items),
    }

    return render(request, "catalog/pages/catalog.html", context)


class ItemDetailView(DetailView):
    model = Item
    template_name = "catalog/pages/item.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = self.object
        item.add_view()
        context["cart_product_form"] = CartAddItemForm()
        return context
