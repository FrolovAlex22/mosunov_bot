library_of_articles: dict[int, list] = {
    1: ['мой гитхаб', 'https://github.com/FrolovAlex22'],
    2: ['подробно про инлайн кнопки и урлы', 'https://stepik.org/lesson/759406/step/2'],
    3: ['яндекс', 'https://ya.ru/'],
}

products_in_sale: dict[int, list] = {
    1: ['Отвсехболезнит', 'Замечательный продукт который поможет со указанными симптомами', 1500],
    2: ['Еслибольнопомогит', 'Когда уже ничего не помогает а боль не проходит', 2500],
    3: ['Здоровъесохранит', 'БАД помогает только в путь,все хвалят', 3500],
}

_LIBRARY_TEXT = ''

for key, meaning in library_of_articles.items():
    _LIBRARY_TEXT += f'{key} - {meaning[0]}\n'