menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'}
        ]

class DataMixin:
    paginate_by = 2
    title_page = None
    extra_context = {}

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page
        # if 'menu' not in self.extra_context:
        #     self.extra_context['menu'] = menu

    def get_mixin_context(self, context, **kwargs):
        if self.title_page:
            context['title'] = self.title_page

        # context['menu'] = menu
        context['cat_selected'] = None
        context.update(kwargs)
        return context