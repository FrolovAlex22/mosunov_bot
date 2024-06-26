library_of_articles: dict[int, list] = {
    1: ['Инструкция по применению препарата Ledikast\n',
        'https://smr.apteka-clever.ru/upload/iblock/cf7/cf74908e84989db1febf38e365ab11ab.pdf'
    ],
    2: ['Инструкция по применению препарата Velakast\n',
        'https://smr.apteka-clever.ru/upload/iblock/cee/cee34524377fea9d585c0126ed65f075.pdf'
    ],
    3: ['Инструкция по применению препарата Velpanat\n',
        'https://smr.apteka-clever.ru/upload/iblock/768/768c1b8cb51c11142435b810e5349a27.pdf'
    ],
}

products_in_sale: dict[int, list] = {
    1: ['Ледикаст(Ledikast)',
        'Препарат LediKast создан для лечения гепатита С. Выступает в роли '
        'ингибитора протеазы иполимеразы. Лекарство используется для лечения '
        'взрослой группы пациентов без интерферонов.',
        41700,
        'ledicast.jpg'
    ],
    2: ['Велакаст(Velakast)',
        'Это индийский дженерик, противовирусный препарат который используется '
        'для лечения гепатита С всех основных генотипов (1, 2, 3, 4, 5, 6) с '
        'эффективностью до 99%.',
        39000,
        'velakast.png'
    ],
    3: ['Велпанат(Velpanat)',
        'Велпанат – это лекарственное средство, содержащее активные вещества '
        'софосбувир и велпатасвир в одной таблетке. Оно применяется для лечения'
        ' хронического вирусного гепатита C у взрослых (пациентов в возрасте от'
        ' 18 лет и старше)',
        43200,
        'velpanat.jpg'
    ],
}

_LIBRARY_TEXT = ''

for key, meaning in library_of_articles.items():
    _LIBRARY_TEXT += f'{key} - {meaning[0]}\n'