#!/usr/bin/python

ROOT_URL = 'http://numismatics.org/'
SEARCH_URL = 'ocre/results?q='
JSON_API_URL = 'ocre/id/'
NOMISMA_URL = 'http://nomisma.org/id/'
BRITISH_MUSEUM_URL = (
    'http://collection.britishmuseum.org/'
    'id/person-institution/'
)
BRITISH_MUSEUM_NAMES_BY_ID = {
    '53770': 'Horus',
    '54025': 'Isis',
    '56979': 'Venus',
    '56988': 'Apollo',
    '57039': 'Diana',
    '57049': 'Asclepius',
    '57060': 'Minerva',
    '57291': 'Bonus Eventus',
    '57638': 'Concordia',
    '57655': 'Cupid',
    '57657': 'Cybele',
    '57930': 'Ceres',
    '57951': 'Dioscuri',
    '58247': 'Felicitas',
    '58260': 'Fortuna',
    '58396': 'Genius',
    '58409': 'Three Graces',
    '58616': 'Sol',
    '58624': 'Juno',
    '58658': 'Spes',
    '58668': 'Salus',
    '58921': 'Jupiter',
    '59099': 'Liberalitas',
    '59100': 'Libertas',
    '59284': 'Mars',
    '59792': 'Pietas',
    '59843': 'Providentia',
    '60203': 'Romulus & Remus Twins',
    '60208': 'Roma',
    '60209': 'Lupa',
    '60911': 'Vesta',
    '60915': 'Victory',
    '64218': 'Annona',
    '69305': 'Fides',
    '71928': 'Terra',
    '75120': 'Moneta',
    '76227': 'Pax',
    '80685': 'Virtus',
    '85985': 'Aequitas',
    '98260': 'Securitas',
    '132743': 'Pudicitia',
    '178090': 'Indulgentia',
    '187735': 'Fecunditas',
    '188733': 'Dea Caelestis',
}
