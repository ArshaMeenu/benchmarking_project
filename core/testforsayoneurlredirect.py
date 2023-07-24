
def get_success_url(): #dynamic url
    return reverse('blog-detail')
class BlogDetailView(BannerClassMixin, DetailView):
    template_name = 'v2/zinnia/entry_detail.html'
    model = Entry
    banner_class = 'sub-in-banner blog-banner'
    context_object_name = 'blog'

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

    def get_object(self, *args, **kwargs):
        # Return any previously-cached object
        if getattr(self, 'object', None):
            return self.object
        return super(BlogDetailView, self).get_object(*args, **kwargs)

    def get(self, *args, **kwargs):
        # Make sure to use the canonical URL
        self.object = self.get_object()
        obj_url = self.object.get_absolute_url()
        if self.request.path != obj_url:
            print('obj_url',obj_url)
            return HttpResponsePermanentRedirect(obj_url)
        return super(BlogDetailView, self).get(*args, **kwargs);



    def get(self,request,**kwargs):
        print('abc')
        obj = get_object_or_404(Entry, slug=kwargs['slug'])
        print('obj.slug', obj)
        print(" kwargs['slug']", kwargs['slug'])
        if obj.slug != kwargs['slug']:
            print('no')
            return redirect('blog', slug=obj.slug, status = 301)
        print('yse')
        # return HttpResponseRedirect(get_success_url())
        return redirect(obj)
