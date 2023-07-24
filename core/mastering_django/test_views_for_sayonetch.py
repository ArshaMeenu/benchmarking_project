class BlogDetailView(BannerClassMixin, DetailView):
    template_name = 'v2/zinnia/entry_detail.html'
    model = Entry
    banner_class = 'sub-in-banner blog-banner'
    context_object_name = 'blog'

    def dispatch(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        if slug == '9-advantages-of-reactjs-why-choose-it-for-your-web-project':
            return redirect('sayone:blog-detail',slug ='advantages-of-react-js')
        return super(BlogDetailView, self).dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        e_book_for_blog = self.get_object().ebook
        context['e_book'] = e_book_for_blog if e_book_for_blog else EBook.published_items().order_by('-created').first()
        context['related_e_books'] = EBook.published_items().filter(
            categories__in=self.get_object().categories.all()).distinct().order_by(
            '-created')[:2]
        context['faqs'] = BlogFAQ.get_faq_for_this_blog(self.get_object())
        context['authors'] = self.get_object().authors.all()
        return context

    # def get_redirect_url(self):
    #     try:
    #         print('try')
    #         slug = Entry.objects.filter(slug=self.kwargs['slug']).first().slug
    #     except Entry.DoesNotExist:
    #         print('not added')
    #         context = self.get_context_data()
    #         print('conte',context)
    #         return self.render_to_response(context)
    #     return reverse('sayone:blog-detail', args=(slug))


    # def get_queryset(self):
    #     entry = Entry.objects.filter(slug=self.kwargs['slug']).first().slug
    #     print('entry',entry)
    #     return entry
    #
    # def get(self, request, *args, **kwargs):
    #     print('geto')
    #     self.object_list = self.get_queryset()
    #     print('obj',self.object_list)
    #     if self.object_list:
    #         print('yes object')
    #         context = self.get_context_data()
    #         print('conte',context)
    #         return self.render_to_response(context)
    #     print('no slug')
    #     return redirect('sayone:blog-detail', slug=self.object_list,status = 301)




     # def get(self, request, **kwargs):
     #    obj = get_object_or_404(Entry, slug=kwargs['slug'])
     #    if obj.slug != kwargs['slug']:
     #        print('not slug')
     #        return redirect('sayone:blog-detail', slug=obj.slug,status = 301)
     #    print('slug hav')
     #    return reverse("sayone:blog-detail", kwargs={"slug":self.kwargs['slug']})


     # def get_success_url(self):
     #    # return redirect('sayone:blog-detail', slug=self.kwargs['slug'],status = 301)
     #    print("self.kwargs['slug']",self.kwargs['slug'])
     #    return reverse("sayone:blog-list", kwargs={"slug":self.kwargs['slug']})
