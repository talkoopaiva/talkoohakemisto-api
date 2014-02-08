# -*- coding: utf-8 -*-
"""Populate `municipality` table

Revision ID: 2e20f23a8ffd
Revises: 3228d3c17da3
Create Date: 2014-02-08 15:27:38.174711

"""

# revision identifiers, used by Alembic.
revision = '2e20f23a8ffd'
down_revision = '3228d3c17da3'

from alembic import op


MUNICIPALITIES = [
    (91, 'Helsinki'),
    (49, 'Espoo'),
    (18, 'Askola'),
    (445, 'Parainen'),
    (170, 'Jomala'),
    (51, 'Eurajoki'),
    (761, 'Somero'),
    (702, 'Ruovesi'),
    (297, 'Kuopio'),
    (678, 'Raahe'),
    (785, 'Vaala'),
    (273, 'Kolari'),
    (732, 'Salla'),
    (529, 'Naantali'),
    (887, 'Urjala'),
    (981, 'Ypäjä'),
    (562, 'Orivesi'),
    (405, 'Lappeenranta'),
    (580, 'Parikkala'),
    (743, 'Seinäjoki'),
    (848, 'Tohmajärvi'),
    (71, 'Haapavesi'),
    (564, 'Oulu'),
    (698, 'Rovaniemi'),
    (261, 'Kittilä'),
    (433, 'Loppi'),
    (109, 'Hämeenlinna'),
    (576, 'Padasjoki'),
    (538, 'Nousiainen'),
    (734, 'Salo'),
    (249, 'Keuruu'),
    (915, 'Varkaus'),
    (146, 'Ilomantsi'),
    (753, 'Sipoo'),
    (165, 'Janakkala'),
    (111, 'Heinola'),
    (480, 'Marttila'),
    (286, 'Kouvola'),
    (178, 'Juva'),
    (97, 'Hirvensalmi'),
    (740, 'Savonlinna'),
    (946, 'Vöyri'),
    (426, 'Liperi'),
    (92, 'Vantaa'),
    (858, 'Tuusula'),
    (149, 'Inkoo'),
    (710, 'Raasepori'),
    (609, 'Pori'),
    (837, 'Tampere'),
    (536, 'Nokia'),
    (418, 'Lempäälä'),
    (285, 'Kotka'),
    (139, 'Ii'),
    (683, 'Ranua'),
    (614, 'Posio'),
    (505, 'Mäntsälä'),
    (908, 'Valkeakoski'),
    (410, 'Laukaa'),
    (905, 'Vaasa'),
    (280, 'Korsnäs'),
    (272, 'Kokkola'),
    (9, 'Alavieska'),
    (615, 'Pudasjärvi'),
    (320, 'Kemijärvi'),
    (532, 'Nastola'),
    (853, 'Turku'),
    (503, 'Mynämäki'),
    (790, 'Sastamala'),
    (77, 'Hankasalmi'),
    (233, 'Kauhava'),
    (499, 'Mustasaari'),
    (69, 'Haapajärvi'),
    (202, 'Kaarina'),
    (400, 'Laitila'),
    (271, 'Kokemäki'),
    (935, 'Virolahti'),
    (739, 'Savitaipale'),
    (153, 'Imatra'),
    (729, 'Saarijärvi'),
    (491, 'Mikkeli'),
    (164, 'Jalasjärvi'),
    (846, 'Teuva'),
    (762, 'Sonkajärvi'),
    (607, 'Polvijärvi'),
    (47, 'Enontekiö'),
    (927, 'Vihti'),
    (434, 'Loviisa'),
    (398, 'Lahti'),
    (781, 'Sysmä'),
    (179, 'Jyväskylä'),
    (226, 'Karstula'),
    (263, 'Kiuruvesi'),
    (276, 'Kontiolahti'),
    (758, 'Sodankylä'),
    (444, 'Lohja'),
    (684, 'Rauma'),
    (211, 'Kangasala'),
    (992, 'Äänekoski'),
    (75, 'Hamina'),
    (598, 'Pietarsaari'),
    (599, 'Pedersöre'),
    (765, 'Sotkamo'),
    (851, 'Tornio'),
    (976, 'Ylitornio'),
    (583, 'Pelkosenniemi'),
    (478, 'Maarianhamina'),
    (5, 'Alajärvi'),
    (707, 'Rääkkylä'),
    (687, 'Rautavaara'),
    (694, 'Riihimäki'),
    (560, 'Orimattila'),
    (50, 'Eura'),
    (108, 'Hämeenkyrö'),
    (145, 'Ilmajoki'),
    (921, 'Vesanto'),
    (593, 'Pieksämäki'),
    (260, 'Kitee'),
    (791, 'Siikalatva'),
    (106, 'Hyvinkää'),
    (481, 'Masku'),
    (592, 'Petäjävesi'),
    (420, 'Leppävirta'),
    (167, 'Joensuu'),
    (205, 'Kajaani'),
    (838, 'Tarvasjoki'),
    (214, 'Kankaanpää'),
    (749, 'Siilinjärvi'),
    (148, 'Inari'),
    (886, 'Ulvila'),
    (142, 'Iitti'),
    (60, 'Finström'),
    (20, 'Akaa'),
    (475, 'Maalahti'),
    (777, 'Suomussalmi'),
    (241, 'Keminmaa'),
    (408, 'Lapua'),
    (535, 'Nivala'),
    (832, 'Taivalkoski'),
    (611, 'Pornainen'),
    (98, 'Hollola'),
    (301, 'Kurikka'),
    (236, 'Kaustinen'),
    (90, 'Heinävesi'),
    (483, 'Merijärvi'),
    (82, 'Hattula'),
    (689, 'Rautjärvi'),
    (231, 'Kaskinen'),
    (925, 'Vieremä'),
    (172, 'Joutsa'),
    (430, 'Loimaa'),
    (143, 'Ikaalinen'),
    (230, 'Karvia'),
    (176, 'Juuka'),
    (61, 'Forssa'),
    (989, 'Ähtäri'),
    (854, 'Pello'),
    (834, 'Tammela'),
    (980, 'Ylöjärvi'),
    (507, 'Mäntyharju'),
    (620, 'Puolanka'),
    (742, 'Savukoski'),
    (636, 'Pöytyä'),
    (103, 'Humppila'),
    (300, 'Kuortane'),
    (171, 'Joroinen'),
    (16, 'Asikkala'),
    (399, 'Laihia'),
    (626, 'Pyhäjärvi'),
    (495, 'Multia'),
    (541, 'Nurmes'),
    (922, 'Vesilahti'),
    (213, 'Kangasniemi'),
    (476, 'Maaninka'),
    (240, 'Kemi'),
    (747, 'Siikainen'),
    (892, 'Uurainen'),
    (208, 'Kalajoki'),
    (105, 'Hyrynsalmi'),
    (845, 'Tervola'),
    (102, 'Huittinen'),
    (182, 'Jämsä'),
    (305, 'Kuusamo'),
    (245, 'Kerava'),
    (531, 'Nakkila'),
    (893, 'Uusikaarlepyy'),
    (890, 'Utsjoki'),
    (232, 'Kauhajoki'),
    (545, 'Närpiö'),
    (35, 'Brändö'),
    (638, 'Porvoo'),
    (931, 'Viitasaari'),
    (489, 'Miehikkälä'),
    (421, 'Lestijärvi'),
    (402, 'Lapinlahti'),
    (625, 'Pyhäjoki'),
    (257, 'Kirkkonummi'),
    (601, 'Pihtipudas'),
    (584, 'Perho'),
    (204, 'Kaavi'),
    (619, 'Punkalaidun'),
    (250, 'Kihniö'),
    (291, 'Kuhmoinen'),
    (19, 'Aura'),
    (288, 'Kruunupyy'),
    (322, 'Kemiönsaari'),
    (543, 'Nurmijärvi'),
    (78, 'Hanko'),
    (631, 'Pyhäranta'),
    (169, 'Jokioinen'),
    (403, 'Lappajärvi'),
    (316, 'Kärkölä'),
    (680, 'Raisio'),
    (239, 'Keitele'),
    (686, 'Rautalampi'),
    (224, 'Karkkila'),
    (635, 'Pälkäne'),
    (857, 'Tuusniemi'),
    (81, 'Hartola'),
    (484, 'Merikarvia'),
    (140, 'Iisalmi'),
    (751, 'Simo'),
    (76, 'Hammarland'),
    (895, 'Uusikaupunki'),
    (500, 'Muurame'),
    (416, 'Lemi'),
    (74, 'Halsua'),
    (563, 'Oulainen'),
    (616, 'Pukkila'),
    (174, 'Juankoski'),
    (561, 'Oripää'),
    (508, 'Mänttä-Vilppula'),
    (759, 'Soini'),
    (440, 'Luoto'),
    (768, 'Sulkava'),
    (290, 'Kuhmo'),
    (844, 'Tervo'),
    (10, 'Alavus'),
    (152, 'Isokyrö'),
    (700, 'Ruokolahti'),
    (295, 'Kumlinge'),
    (256, 'Kinnula'),
    (977, 'Ylivieska'),
    (746, 'Sievi'),
    (624, 'Pyhtää'),
    (849, 'Toholampi'),
    (422, 'Lieksa'),
    (924, 'Veteli'),
    (748, 'Siikajoki'),
    (319, 'Köyliö'),
    (177, 'Juupajoki'),
    (498, 'Muonio'),
    (581, 'Parkano'),
    (889, 'Utajärvi'),
    (577, 'Paimio'),
    (911, 'Valtimo'),
    (309, 'Outokumpu'),
    (578, 'Paltamo'),
    (859, 'Tyrnävä'),
    (186, 'Järvenpää'),
    (52, 'Evijärvi'),
    (934, 'Vimpeli'),
    (86, 'Hausjärvi'),
    (413, 'Lavia'),
    (691, 'Reisjärvi'),
    (244, 'Kempele'),
    (407, 'Lapinjärvi'),
    (588, 'Pertunmaa'),
    (442, 'Luvia'),
    (287, 'Kristiinankaupunki'),
    (151, 'Isojoki'),
    (62, 'Föglö'),
    (275, 'Konnevesi'),
    (441, 'Luumäki'),
    (284, 'Koski Tl'),
    (936, 'Virrat'),
    (704, 'Rusko'),
    (494, 'Muhos'),
    (425, 'Liminka'),
    (681, 'Rantasalmi'),
    (235, 'Kauniainen'),
    (783, 'Säkylä'),
    (216, 'Kannonkoski'),
    (738, 'Sauvo'),
    (697, 'Ristijärvi'),
    (850, 'Toivakka'),
    (595, 'Pielavesi'),
    (317, 'Kärsämäki'),
    (604, 'Pirkkala'),
    (778, 'Suonenjoki'),
    (833, 'Taivassalo'),
    (218, 'Karijoki'),
    (312, 'Kyyjärvi'),
    (46, 'Enonkoski'),
    (181, 'Jämijärvi'),
    (771, 'Sund'),
    (831, 'Taipalsaari'),
    (504, 'Myrskylä'),
    (99, 'Honkajoki'),
    (283, 'Hämeenkoski'),
    (423, 'Lieto'),
    (941, 'Vårdö'),
    (217, 'Kannus'),
    (630, 'Pyhäntä'),
    (608, 'Pomarkku'),
    (918, 'Vehmaa'),
    (736, 'Saltvik'),
    (43, 'Eckerö'),
    (755, 'Siuntio'),
    (79, 'Harjavalta'),
    (318, 'Kökar'),
    (623, 'Puumala'),
    (304, 'Kustavi'),
    (435, 'Luhanka'),
    (265, 'Kivijärvi'),
    (438, 'Lumparland'),
    (65, 'Geta'),
    (72, 'Hailuoto'),
    (436, 'Lumijoki'),
    (766, 'Sottunga'),
    (417, 'Lemland'),
]


def upgrade():
    conn = op.get_bind()
    conn.execute(
        'INSERT INTO municipality (code, name) VALUES (%s, %s)',
        *MUNICIPALITIES
    )


def downgrade():
    op.execute('DELETE FROM municipality')