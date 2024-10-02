from typing import Dict, List, Union, Optional

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db import models
from django.urls import reverse


class TreeManager(models.Manager):

    __paths: Dict[int, List[int]] = {}

    def get(self) -> Dict[str, Union[Dict[int, List[int]], Dict[int, Dict]]]:
        res = cache.get('sections_tree_manager_result_cache')
        if not res:
            res = {
                'tree': self.__build(),
                'paths': self.__paths,
            }
            cache.set('sections_tree_manager_result_cache', res, 3600 * 24 * 365 * 888)
        return res

    def get_el(self, el_id: int) -> 'Sections':
        res = self.get()
        if res['paths'].get(el_id) is None:
            return res['tree'][el_id]
        return eval(
            f'res["tree"][{
                ']["children"]['.join(map(str, res['paths'][el_id]))
            }]["children"][{el_id}]'
        )

    def __build(
        self,
        el_id: Optional[int] = None,
        els: Optional[Dict[int, Dict[str, Optional[Union[int, str]]]]] = None,
        path: Optional[List[int]] = None,
    ) -> Dict[int, Dict[str, Dict]]:
        res = {}
        if el_id is None:
            els = {}
            for item in super().get_queryset().filter(is_active=Sections.Status.ACTIVE):
                els[item.pk] = item
        for item_k in list(els):
            if els.get(item_k) is None:
                continue
            item_v = els[item_k]
            if item_v.parent_id == el_id:
                if path == None:
                    cat_path = [el_id]
                else:
                    cat_path = path.copy()
                    cat_path.append(el_id)
                if cat_path == [None]:
                    cat_path = []
                else:
                    self.__paths[item_k] = cat_path
                res[item_k] = {'el': item_v}
                del els[item_k]
                res[item_k]['children'] = self.__build(item_k, els, cat_path)
                if not res[item_k]['children']:
                    del res[item_k]['children']
        return res

class Sections(models.Model):

    class Status(models.IntegerChoices):
        ACTIVE = 1, 'Active'
        NO_ACTIVE = 0, 'No active'

    id = models.AutoField(primary_key=True, verbose_name='ID категории')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    # null=True, to allow in database
    # blank=True, to allow in form validation
    code = models.CharField(max_length=255, db_index=True, unique=True)
    name = models.CharField(max_length=251, verbose_name='Название категории')
    description = models.TextField(blank=True)
    sort = models.IntegerField(default=800)
    is_active = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)), default=Status.ACTIVE)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'[{self.pk}]: {self.name}'

    class Meta:
        verbose_name = 'Каталог'
        verbose_name_plural = 'Каталоги'
    #     ordering = ['-sort']
    #     indexes = [models.Index(fields=['-sort'])]

    '''
    После добавления своего менеджера удаляется стандартный и
    Sections.objects.all() перестает работать. Возвращаем его обратно:
    '''
    objects = models.Manager()

    tree = TreeManager()

    def get_absolute_url(self):
        path = Sections.tree.get()['paths'].get(self.pk)
        if path is None:
            return reverse('section', kwargs={'section_code': self.code})
        else:
            path_list = []
            for el_id in path:
                path_list.append(Sections.tree.get_el(el_id)['el'].code)
            return reverse('section', kwargs={
                'section_code': self.code,
                'section_path': '/'.join(path_list),
            })

    def save(self, *args, **kwargs) -> None:
        self.code = f'{self.code}-page'
        super().save(*args, **kwargs)

class Elements(models.Model):

    class Meta:
        verbose_name = 'Элемент'
        verbose_name_plural = 'Элементы'

    class Status(models.IntegerChoices):
        ACTIVE = 1, 'Active'
        NO_ACTIVE = 0, 'No active'

    id = models.AutoField(primary_key=True)
    photo = models.ImageField(
        upload_to='elements_photos/%Y/%m/%d',
        default=None, null=True, blank=True
    ) # FileField
    sections = models.ManyToManyField(Sections, blank=True)
    code = models.CharField(max_length=255, db_index=True, unique=True)
    name = models.CharField(max_length=255, verbose_name='Название элемента')
    description = models.TextField(blank=True)
    sort = models.IntegerField(default=800)
    is_active = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)), default=Status.ACTIVE)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        related_name='element_item',
        null=True,
        default=None,
    )

    def __str__(self) -> str:
        return f'[{self.pk}]: {self.name}'
