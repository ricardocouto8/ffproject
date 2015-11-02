import random
import Line

PLAYER_GLOBALS = {
    "MIN_NAME"  : 1,
    "MAX_NAME"  : 18,
    "MIN_SKILL" : 1,
    "MAX_SKILL" : 50,
    "SKILL_RANGES": 10,
    "MIN_AGE"   : 18,
    "MAX_AGE"   : 36,
    "AGE_STEPS" : 36 - 18,
    "AGE_RANGES": 5,
    "MEAN_AGE"  : 26.5,
    "STD_DEV_AGE" : 4.5,
    "MIN_SALARY" : 400.0,
    "MIN_VALUE" : 100000.0,
    "AGE_TRAINING_INF": (0, 0.25, 0.5, 0.75, 1, 2),
    "TRAINING_PER_AGE": (0.09, 0.07, 0.04, 0.005, 0, 0),
    "PRICE_AGE": (6.5, 4.2, 2.7, 0.9, 0.1, 0),
    "PRICE_SKILL": (4.8, 2.1, 1.45, 1.25, 1.15),
    "AVERAGE_SALARIES_PER_VALUE": 3.0
}

TEAM_GLOBALS = {
    "MIN_REP"   : 1,
    "MAX_REP"   : 20,
    "PLAYERS_PER_POSITION" : (2, 5, 5, 3),
    "TACTICS"   :((3,3,4),(3,4,3),(3,5,2),(4,5,1),(4,4,2),
                  (4,3,3),(4,2,4),(5,2,3),(5,3,2),(5,4,1)),
    "MIN_MONEY" : 1000000.0,
    "MIN_TRAINING_GROUND" : 0,
    "MAX_TRAINING_GROUND" : 5,
    "MAX_PLAYERS" : 25,
}

GAME_GLOBALS = {
    "ACTIVE_LEAGUES"    : 4,
    "TEAMS_PER_LEAGUE" : 8,
    "DEMOTED_PER_LEAGUE" : 2,
    "TOTAL_TURNS" : (8 - 1) * 2,
    "MAX_PLAYERS_BENCH" : 5,
}

MATCH_GLOBALS = {
    "TACTIC_INFLUENCE": 0.2,
    "MAX_GOAL_PER_POSS" : 0.07,
    "MIN_GOAL_PER_POSS" : 0.007,
    "MAX_POSSESSION" : 0.85,
    "TOTAL_TURNS" : 90 * 1,
    "GOAL_BEGINNING_END_MULTI" : 2.5,
    "ANTI_GOLEADAS" : 0.35,
    "MAX_SUBSTITUTIONS" : 3,
}

def normalize(value, minimum, maximum):
    value = min(max(value, minimum), maximum)
    return (value - minimum) / float(maximum - minimum)

def denormalize(value, minimum, maximum):
    x1 = 0
    y1 = minimum
    x2 = 1
    y2 = maximum
    return ysolver((x1, y1), (x2, y2), value)

def normalize_list(li):
    norm = [float(i)/sum(li) for i in li]
    return norm

def weighted_choice(choices):
    total = sum(w for c, w in choices)
    r = random.uniform(0, total)
    upto = 0
    for c, w in choices:
        if upto + w > r:
            return c
        upto += w
    assert False, "Shouldn't get here"

def ysolver(point1, point2, x):
    return Line.Line((point1, point2)).solve_for_y(x)

def num2str(number):
    # sign = int(number/abs(number))
    # number = int(round(abs(number),1))
    return str(int(number))
    # ktest = number/1000
    # if ktest >= 1:
    #     if ktest >= 10:
    #         if ktest >= 1000:
    #             if ktest >= 10000:
    #                 return str(int(round(ktest/1000.0, 1))) + 'M'
    #             else:
    #                 return str(round(sign * ktest/1000.0, 1)) + 'M'
    #         else:
    #             return str(int(round(sign * ktest, 1))) + 'k'
    #     else:
    #         return str(round(sign * number/1000.0, 1)) + 'k'
    # else:
    #     return str(int(round(sign * number, 1)))

PEOPLE_NAMES = ['Aaberg', 'Abbasi', 'Abee', 'Abling', 'Abruzzo', 'Acey', 'Acord', 'Adauto', 'Adey', 'Adside', 'Agee', 'Agricola', 'Ahern', 'Ahuja', 'Aispuro', 'Akim', 'Alar', 'Alberti', 'Alcorn', 'Alejandro', 'Aley', 'Alier', 'Allder', 'Alligood', 'Almanza', 'Aloy', 'Altaras', 'Altshuler', 'Alvira', 'Amason', 'Ameling', 'Amisano', 'Amphy', 'Anastasi', 'Andeson', 'Andries', 'Angeletti', 'Anglemyer', 'Annable', 'Anspach', 'Antonelli', 'Apa', 'Apperson', 'Arabie', 'Arbo', 'Arcilla', 'Arenburg', 'Arguellez', 'Arjune', 'Armesto', 'Arnholt', 'Arouri', 'Arrizaga', 'Artman', 'Asamoah', 'Ashcraft', 'Asleson', 'Astley', 'Atienza', 'Aube', 'Aughtman', 'Aungst', 'Autman', 'Aver', 'Awtrey', 'Aynes', 'Baade', 'Babonis', 'Bachus', 'Baddley', 'Baez', 'Bahadue', 'Bailony', 'Bakaler', 'Balay', 'Baldino', 'Balistrieri', 'Balliew', 'Baltazar', 'Banahan', 'Bania', 'Banwarth', 'Baray', 'Barboza', 'Barefield', 'Barile', 'Barlowe', 'Baron', 'Barribeau', 'Barshaw', 'Bartin', 'Bartow', 'Baselice', 'Basques', 'Basua', 'Batrez', 'Baty', 'Baumfalk', 'Bawer', 'Baysmore', 'Beadnell', 'Beas', 'Beauparlant', 'Becker', 'Beddoe', 'Beeching', 'Beetley', 'Behner', 'Beish', 'Belden', 'Bellafiore', 'Bellinghausen', 'Belongia', 'Bemboom', 'Bendavid', 'Benesch', 'Benko', 'Benskin', 'Benzinger', 'Berenson', 'Berggren', 'Berkich', 'Bernardez', 'Bernosky', 'Berstein', 'Bertoni', 'Beshears', 'Beth', 'Bettman', 'Beverley', 'Bezzo', 'Biava', 'Bicknase', 'Bielefeld', 'Biesecker', 'Bihler', 'Billey', 'Bina', 'Biondi', 'Birkholz', 'Bischoff', 'Bitetto', 'Bjork', 'Blackson', 'Blakesley', 'Blanko', 'Blatti', 'Bleggi', 'Bligen', 'Blomdahl', 'Blovin', 'Bly', 'Bobeck', 'Bockelmann', 'Bodin', 'Boehnke', 'Boettner', 'Boglioli', 'Bohney', 'Bokal', 'Boleyn', 'Bolnick', 'Bonadurer', 'Bonesteel', 'Bonn', 'Bonvillain', 'Booton', 'Borek', 'Borkin', 'Borrello', 'Bosack', 'Bosserman', 'Botros', 'Bouchillon', 'Boulter', 'Bourque', 'Bovie', 'Bowlick', 'Boykin', 'Brabant', 'Bradd', 'Brahler', 'Bramson', 'Brandolini', 'Branseum', 'Brasseur', 'Bravard', 'Bread', 'Bree', 'Breitbart', 'Breniser', 'Bressler', 'Breznay', 'Bridgette', 'Briglia', 'Bring', 'Briski', 'Broach', 'Brocklehurst', 'Broe', 'Bronaugh', 'Brophy', 'Broun', 'Broz', 'Brueske', 'Brummett', 'Brunot', 'Bryan', 'Bubert', 'Buchli', 'Buckner', 'Budrovich', 'Bueschel', 'Buhler', 'Bulisco', 'Bumba', 'Bunkley', 'Burbage', 'Bureau', 'Burgoyne', 'Burkman', 'Burnie', 'Burrs', 'Busbey', 'Busitzky', 'Busuttil', 'Buttermore', 'Buzzelle', 'Byran', 'Cabe', 'Cachero', 'Caetano', 'Caillier', 'Calbert', 'Calico', 'Callendar', 'Caltabiano', 'Cambareri', 'Cammack', 'Campoverde', 'Candia', 'Cann', 'Cantell', 'Capaldo', 'Caples', 'Caprio', 'Caravella', 'Cardenas', 'Carfrey', 'Carlile', 'Carmickle', 'Carolla', 'Carratala', 'Carrithers', 'Carthew', 'Casados', 'Casello', 'Casolary', 'Cassey', 'Castellaw', 'Castorena', 'Cate', 'Cattladge', 'Cavalier', 'Cawthron', 'Cecilio', 'Cembura', 'Cercy', 'Certalich', 'Chachere', 'Chaix', 'Chamnanphony', 'Channey', 'Chararria', 'Chartraw', 'Chauez', 'Chebahtah', 'Cheney', 'Chesebro', 'Chey', 'Chick', 'Chimenti', 'Chischilly', 'Chock', 'Chow', 'Christiani', 'Chryst', 'Churner', 'Cicali', 'Cifelli', 'Cintron', 'Cisnero', 'Claflin', 'Clarkston', 'Claybourne', 'Clements', 'Click', 'Cloke', 'Cloyd', 'Coant', 'Cocco', 'Coday', 'Cogen', 'Colacone', 'Colder', 'Collamore', 'Collozo', 'Colter', 'Comings', 'Comunale', 'Condroski', 'Conlogue', 'Conquest', 'Contini', 'Cooksley', 'Coote', 'Copus', 'Cordia', 'Corish', 'Cornetta', 'Corredor', 'Corte', 'Cosico', 'Costenive', 'Cotti', 'Counselman', 'Couse', 'Covey', 'Coxon', 'Craffey', 'Crank', 'Crawn', 'Creeley', 'Cresta', 'Crippin', 'Critchfield', 'Croll', 'Cropp', 'Crough', 'Cruiz', 'Crutsinger', 'Cucco', 'Cujas', 'Culwell', 'Cunniffe', 'Curio', 'Curylo', 'Cuti', 'Cygrymus', 'Czerno', 'Daddona', 'Daguerre', 'Dainels', 'Dalhover', 'Dalziel', 'Dampier', 'Danh', 'Dansby', 'Darcey', 'Darnick', 'Das', 'Daubendiek', 'Dauzat', 'Davolt', 'Deadmond', 'Dearo', 'Debernardi', 'Debruin', 'Dechavez', 'Deculus', 'Deets', 'Defrank', 'Degori', 'Dehl', 'Dejackome', 'Delage', 'Delarme', 'Deldeo', 'Delhierro', 'Dellen', 'Delong', 'Delson', 'Demarcus', 'Demello', 'Demming', 'Denapoli', 'Denise', 'Denski', 'Deperro', 'Dequinzio', 'Derienzo', 'Derouin', 'Desanto', 'Desiderio', 'Despain', 'Deters', 'Deuell', 'Deveny', 'Devora', 'Dewyer', 'Diano', 'Dichiaro', 'Didlake', 'Diepenbrock', 'Diffley', 'Dike', 'Dillenburg', 'Dimassimo', 'Dine', 'Dinora', 'Dircks', 'Dishner', 'Ditti', 'Dizer', 'Dobratz', 'Dodrill', 'Doiel', 'Dolinger', 'Dome', 'Domnick', 'Donelly', 'Donning', 'Dorais', 'Dornak', 'Dorst', 'Dottin', 'Douthit', 'Downey', 'Dragan', 'Drawbaugh', 'Dresher', 'Drinnen', 'Droubay', 'Drye', 'Dublin', 'Duchscherer', 'Duelm', 'Dufour', 'Dukeshire', 'Dumke', 'Dunham', 'Dunphe', 'Dupoux', 'Durian', 'Durst', 'Dutile', 'Dwyar', 'Dysinger', 'Eaker', 'Easey', 'Ebbesen', 'Ebrahimi', 'Eckland', 'Edelson', 'Edman', 'Efford', 'Egleston', 'Ehrhart', 'Eidemiller', 'Eiseman', 'Ekis', 'Elem', 'Eliopoulos', 'Ellerbe', 'Ellrod', 'Elsheimer', 'Emayo', 'Emley', 'Ence', 'Engelhardt', 'Englin', 'Ensey', 'Eppard', 'Erdelt', 'Erlenbusch', 'Ertman', 'Esco', 'Eslick', 'Esposita', 'Estanislau', 'Esty', 'Euresti', 'Evenstad', 'Evora', 'Eyster', 'Facello', 'Fagnant', 'Fairbrother', 'Falconeri', 'Falor', 'Fannell', 'Faren', 'Farness', 'Farve', 'Faubel', 'Fausnaugh', 'Faye', 'Febbo', 'Fedorko', 'Fehringer', 'Felberbaum', 'Feller', 'Fencl', 'Fenton', 'Ferjerang', 'Ferrando', 'Ferrise', 'Fetterhoff', 'Fickas', 'Fierman', 'Fijal', 'Fillers', 'Findlen', 'Finley', 'Fiorino', 'Fishbaugh', 'Fitzke', 'Flaks', 'Fleagle', 'Flenard', 'Flink', 'Florence', 'Fluellen', 'Foertsch', 'Folland', 'Fontaine', 'Forbus', 'Forkin', 'Forschner', 'Fortunato', 'Fought', 'Foxman', 'Fraley', 'Francy', 'Franzel', 'Frayser', 'Freeberg', 'Freidhof', 'Frerichs', 'Fricker', 'Friendly', 'Frisina', 'Frohling', 'Fruin', 'Fuelling', 'Fujisawa', 'Fulop', 'Furblur', 'Furtado', 'Fykes', 'Gabriele', 'Gaestel', 'Gailes', 'Galas', 'Galicinao', 'Gallegoz', 'Galloway', 'Gamba', 'Gamrath', 'Ganim', 'Gara', 'Gardin', 'Garin', 'Garo', 'Garry', 'Gascot', 'Gastineau', 'Gatza', 'Gauntt', 'Gawron', 'Gealy', 'Geelan', 'Geier', 'Geller', 'Generalao', 'Gentilcore', 'Geraci', 'Gerig', 'Gerraro', 'Gerweck', 'Gettman', 'Gherman', 'Giampapa', 'Gibbens', 'Giera', 'Gilarski', 'Gilio', 'Gillingham', 'Gilzow', 'Gioffre', 'Girman', 'Gittinger', 'Gladhart', 'Glass', 'Gledhill', 'Glock', 'Glueckert', 'Gochal', 'Godsey', 'Goes', 'Goich', 'Goldfield', 'Golemba', 'Golston', 'Gonsales', 'Gooder', 'Goodsite', 'Gord', 'Gorn', 'Gosney', 'Gotter', 'Goulet', 'Goyda', 'Graddy', 'Grahn', 'Granato', 'Grano', 'Grate', 'Graybill', 'Greenberger', 'Greenwood', 'Greist', 'Greulich', 'Griest', 'Grimaldo', 'Grisham', 'Grocott', 'Groner', 'Grossi', 'Grubel', 'Grundmeier', 'Guadagnolo', 'Gubser', 'Guerard', 'Guggemos', 'Guiles', 'Guirgis', 'Gulledge', 'Gundrum', 'Guridi', 'Gustason', 'Gutschow', 'Guzon', 'Haan', 'Hack', 'Haddox', 'Hafenbrack', 'Hagg', 'Haid', 'Hajdukiewicz', 'Hales', 'Halligan', 'Halseth', 'Hambrick', 'Hammarlund', 'Hampon', 'Handing', 'Haning', 'Hanney', 'Hanson', 'Haran', 'Hardell', 'Harell', 'Harkness', 'Harnly', 'Harriger', 'Hartgrave', 'Hartsfield', 'Harwin', 'Haskins', 'Hatada', 'Hatzenbihler', 'Hauptmann', 'Havermale', 'Haxby', 'Haynsworth', 'Heaberlin', 'Hearns', 'Hebert', 'Hedgepeth', 'Heffern', 'Hehir', 'Heikkila', 'Heininger', 'Heisser', 'Helfenbein', 'Hellner', 'Helstrom', 'Hemmen', 'Henderlite', 'Henigan', 'Henninger', 'Hentz', 'Herby', 'Hermann', 'Herpolsheimer', 'Hersh', 'Herzig', 'Hethcote', 'Hevey', 'Hibbard', 'Hickton', 'Higginson', 'Hilchey', 'Hillbrant', 'Hilscher', 'Hinchcliff', 'Hinke', 'Hipple', 'Hirz', 'Hix', 'Hobday', 'Hockley', 'Hoefflin', 'Hoey', 'Hoga', 'Hohlfeld', 'Holbert', 'Holibaugh', 'Holliday', 'Holmers', 'Holterman', 'Holznecht', 'Hondel', 'Honza', 'Hopf', 'Horenstein', 'Hornik', 'Horuath', 'Hospkins', 'Houchen', 'Houser', 'Hovorka', 'Hoxie', 'Hsi', 'Huckabay', 'Huebert', 'Hufft', 'Huhtala', 'Hulshoff', 'Humpert', 'Hunsucker', 'Hurless', 'Husein', 'Hutchens', 'Huynh', 'Hynum', 'Ianuzzi', 'Idriss', 'Ijames', 'Imada', 'In', 'Ingemi', 'Innocent', 'Iozzo', 'Isaack', 'Isham', 'Italia', 'Iwanicki', 'Jackels', 'Jacquot', 'Jainlett', 'Jamwant', 'Janke', 'Janusz', 'Jarnutowski', 'Jaspers', 'Jayroe', 'Jefferis', 'Jen', 'Jentzsch', 'Jervis', 'Jex', 'Jirik', 'Joh', 'Joler', 'Joosten', 'Joswick', 'Jubic', 'Juliar', 'Junkin', 'Justen', 'Kabus', 'Kaemmerer', 'Kahre', 'Kalandek', 'Kalisch', 'Kalt', 'Kamirez', 'Kanda', 'Kansas', 'Kappen', 'Kareem', 'Karoly', 'Kasal', 'Kassem', 'Kathel', 'Kauffmann', 'Kawano', 'Keagle', 'Keaveny', 'Keenan', 'Keib', 'Kelch', 'Kellough', 'Kempen', 'Kenfield', 'Keno', 'Kerbs', 'Kerrick', 'Kesselring', 'Kettler', 'Khalili', 'Khuu', 'Kiel', 'Kiili', 'Killary', 'Kilty', 'Kimura', 'Kingcade', 'Kinnan', 'Kinville', 'Kiritsy', 'Kirsten', 'Kissner', 'Kitzerow', 'Klamn', 'Klebes', 'Kleintop', 'Klick', 'Klingshirn', 'Kloppenburg', 'Kluver', 'Knazs', 'Kniess', 'Knoell', 'Knupp', 'Kochis', 'Koelzer', 'Kofler', 'Koitzsch', 'Kolinski', 'Komara', 'Konik', 'Koopman', 'Kopperud', 'Koritko', 'Korzenski', 'Koslowski', 'Kot', 'Kotzur', 'Kovats', 'Kozisek', 'Krajcer', 'Krasley', 'Kreatsoulas', 'Kreke', 'Krichbaum', 'Kristek', 'Krogman', 'Krouse', 'Krupansky', 'Krzesinski', 'Kubin', 'Kuder', 'Kuhl', 'Kuklis', 'Kumfer', 'Kunzel', 'Kurnik', 'Kusick', 'Kuypers', 'Kyker', 'Labbe', 'Labrie', 'Lackage', 'Ladell', 'Lafevre', 'Lafromboise', 'Lagrasse', 'Laine', 'Lalich', 'Lamattina', 'Lamica', 'Lamparski', 'Lanctot', 'Landolfo', 'Langager', 'Langlo', 'Lanna', 'Lantis', 'Lapid', 'Larabell', 'Larimore', 'Larrick', 'Laser', 'Lassere', 'Latiker', 'Latzig', 'Lauigne', 'Laurino', 'Lavalle', 'Lavine', 'Lawry', 'Lazaroff', 'Leak', 'Leavengood', 'Lebron', 'Leday', 'Leehan', 'Lefler', 'Leghorn', 'Lehoullier', 'Leiferman', 'Leistiko', 'Leman', 'Lemond', 'Lenhart', 'Lents', 'Lepera', 'Lescano', 'Lessly', 'Letterman', 'Leve', 'Leviner', 'Lewitt', 'Libberton', 'Lichtenstein', 'Lieberg', 'Liesveld', 'Ligman', 'Limardo', 'Lindahl', 'Lindmeyer', 'Lingenfelter', 'Linsdau', 'Lipman', 'Lisbey', 'Litchmore', 'Litzenberg', 'Lizardi', 'Lobbins', 'Locket', 'Loeffler', 'Lofquist', 'Lohmeyer', 'Lollis', 'Loney', 'Longtin', 'Lopeman', 'Lorent', 'Losa', 'Lotempio', 'Loughborough', 'Lousteau', 'Lovette', 'Lowrance', 'Luarca', 'Luchetti', 'Luczki', 'Lueders', 'Lui', 'Lumantas', 'Lundsford', 'Lupul', 'Lutkins', 'Lybbert', 'Lyne', 'Mabe', 'Maccarter', 'Macguire', 'Macinnis', 'Mackowiak', 'Macpherson', 'Maddux', 'Madren', 'Mafnas', 'Maggiore', 'Magnusson', 'Maharg', 'Maiava', 'Mainz', 'Majied', 'Malachowski', 'Maldomado', 'Malinky', 'Mallinger', 'Maltby', 'Manasco', 'Manderscheid', 'Mangaoang', 'Manifold', 'Mannheimer', 'Mansi', 'Manuell', 'Mar', 'Marbry', 'Marchione', 'Marder', 'Margolis', 'Marinos', 'Markos', 'Marner', 'Marrapese', 'Marsell', 'Martes', 'Martinz', 'Marwick', 'Mascorro', 'Masloski', 'Massingale', 'Masupha', 'Mathe', 'Matis', 'Matsuura', 'Mattis', 'Matzinger', 'Maus', 'Maxin', 'Mayner', 'Mazique', 'Mcadoo', 'Mcavoy', 'Mccall', 'Mccarl', 'Mccausland', 'Mccleese', 'Mcclurg', 'Mcconnaughhay', 'Mccrackin', 'Mccuien', 'Mcdaneld', 'Mcdowell', 'Mcelyea', 'Mcfetridge', 'Mcghaney', 'Mcglone', 'Mcgregor', 'Mchattie', 'Mckamey', 'Mckennie', 'Mckinnie', 'Mclauchlen', 'Mcmahan', 'Mcmonigle', 'Mcneely', 'Mcpartlin', 'Mcquitty', 'Mctiernan', 'Meador', 'Mechler', 'Medill', 'Meerdink', 'Mehle', 'Meinert', 'Melaun', 'Melikyan', 'Melloy', 'Menapace', 'Mends', 'Mennenga', 'Merales', 'Mericle', 'Merola', 'Mervine', 'Messamore', 'Metevia', 'Metzner', 'Mezzatesta', 'Michel', 'Mickles', 'Mier', 'Mihalick', 'Mikota', 'Mildred', 'Millard', 'Millison', 'Miltner', 'Minder', 'Minihane', 'Minrod', 'Miraglia', 'Misek', 'Misty', 'Mittleman', 'Mizutani', 'Moczulski', 'Moening', 'Mohead', 'Molands', 'Mollenhauer', 'Momphard', 'Mondello', 'Mongomery', 'Monsen', 'Montegut', 'Montijano', 'Moog', 'Moradian', 'Morden', 'Moretto', 'Morioka', 'Morowski', 'Mortenson', 'Mosena', 'Mostert', 'Moudy', 'Mouzas', 'Mozick', 'Muckey', 'Muhammed', 'Mulhollen', 'Mullner', 'Mund', 'Munn', 'Muran', 'Muros', 'Muscato', 'Mussel', 'Mutter', 'Myree', 'Nachtrieb', 'Nagelhout', 'Nakahara', 'Nan', 'Napps', 'Nasby', 'Nath', 'Navarra', 'Nead', 'Nederostek', 'Negro', 'Neiper', 'Nembhard', 'Neske', 'Nettleingham', 'Neuweg', 'Newborn', 'Newsom', 'Nibler', 'Nickleberry', 'Nicome', 'Niemczyk', 'Nighman', 'Nims', 'Nisly', 'Niznik', 'Noeldner', 'Nolen', 'Nop', 'Noreiga', 'Norse', 'Noss', 'Novara', 'Noxon', 'Nuner', 'Nutzmann', 'Oak', 'Obergfell', 'Obray', 'Ochocki', 'Oderkirk', 'Oehmig', 'Ogami', 'Ohair', 'Ohotto', 'Okimoto', 'Olay', 'Olewine', 'Olivid', 'Olshan', 'Oms', 'Ontiveros', 'Opperman', 'Ordon', 'Orick', 'Orms', 'Orsburn', 'Ory', 'Oshita', 'Ostasiewicz', 'Ostrum', 'Otterbein', 'Oursler', 'Overholt', 'Owsley', 'Paap', 'Pacitti', 'Padmore', 'Pagni', 'Palacois', 'Palinski', 'Palmino', 'Pamphile', 'Panepinto', 'Panowicz', 'Papadopoulos', 'Pappy', 'Pardieck', 'Parke', 'Paroda', 'Parsi', 'Paschall', 'Pasquarella', 'Pastula', 'Patman', 'Patty', 'Paulshock', 'Pavolini', 'Payseur', 'Pears', 'Peckens', 'Pedroso', 'Peguero', 'Pelis', 'Pelotte', 'Pendergast', 'Pennelle', 'Penttila', 'Perce', 'Perham', 'Perng', 'Perrill', 'Persten', 'Pesso', 'Petite', 'Petrin', 'Petsche', 'Petzel', 'Pfefferle', 'Phang', 'Philbin', 'Phipps', 'Picado', 'Pickell', 'Piechocki', 'Pierpont', 'Pigna', 'Pilkington', 'Pinchbeck', 'Pinkert', 'Pio', 'Pirrello', 'Pithan', 'Pizira', 'Plamer', 'Platte', 'Plessinger', 'Plouffe', 'Poag', 'Pody', 'Poire', 'Polcyn', 'Polito', 'Polselli', 'Pomroy', 'Pooni', 'Poppema', 'Portales', 'Posis', 'Poteete', 'Pouliotte', 'Poydras', 'Prasomsack', 'Precissi', 'Prentiss', 'Presume', 'Prichett', 'Prince', 'Privett', 'Prokes', 'Protsman', 'Prudom', 'Przybyl', 'Puerto', 'Pulizzi', 'Punch', 'Pursifull', 'Puzinski', 'Quackenbush', 'Quartuccio', 'Quesenberry', 'Quimby', 'Quire', 'Rabehl', 'Rachi', 'Rader', 'Radziwon', 'Raggs', 'Raike', 'Rajan', 'Raman', 'Ramjhon', 'Ramsour', 'Raner', 'Rao', 'Rary', 'Raspotnik', 'Ratkowski', 'Raulerson', 'Raw', 'Rayna', 'Reagle', 'Reazer', 'Reckner', 'Redfearn', 'Reech', 'Regehr', 'Rehman', 'Reidler', 'Reinard', 'Reinsfelder', 'Reitzes', 'Remkus', 'Renee', 'Rensen', 'Reppell', 'Restrepo', 'Reutter', 'Reye', 'Rheinhardt', 'Rhyne', 'Richardson', 'Ricker', 'Rider', 'Riedmayer', 'Riess', 'Riggleman', 'Rily', 'Ringbloom', 'Riojas', 'Risha', 'Ritchko', 'Riveras', 'Roades', 'Roberg', 'Robleto', 'Rockefeller', 'Rodebush', 'Rodolph', 'Roehrig', 'Rog', 'Rohlack', 'Roland', 'Rolon', 'Rombs', 'Rondinelli', 'Root', 'Rosch', 'Rosencrantz', 'Rosiak', 'Rossignol', 'Rothell', 'Rotunno', 'Rousey', 'Rowett', 'Rozance', 'Ruberte', 'Ruddell', 'Rueb', 'Ruffini', 'Rujawitz', 'Rumphol', 'Rupert', 'Rushman', 'Rusu', 'Ruwet', 'Rydzewski', 'Rysz', 'Sabatino', 'Saccone', 'Sadoski', 'Sagar', 'Said', 'Sakiestewa', 'Salazer', 'Saling', 'Salonia', 'Salvati', 'Samber', 'Sampica', 'Sancrant', 'Sandino', 'Sanez', 'Sanna', 'Santangelo', 'Santore', 'Saraceno', 'Sarin', 'Sarson', 'Satawa', 'Sauerbry', 'Savageau', 'Savko', 'Sayed', 'Scalf', 'Scarff', 'Scelsi', 'Schaetzle', 'Schappach', 'Schaumburg', 'Scheidel', 'Schepker', 'Schiaffino', 'Schildt', 'Schkade', 'Schlenker', 'Schlossman', 'Schmick', 'Schnakenberg', 'Schnorbus', 'Schoenig', 'Schommer', 'Schoultz', 'Schreurs', 'Schuble', 'Schulke', 'Schurr', 'Schwarm', 'Schwenck', 'Sciabica', 'Scofield', 'Scozzafava', 'Scullin', 'Seajack', 'Seaver', 'Secord', 'Seeds', 'Segall', 'Seid', 'Seipp', 'Selic', 'Seltz', 'Sempek', 'Senne', 'Sepulveda', 'Serini', 'Servatius', 'Setlock', 'Severson', 'Sforza', 'Shady', 'Shalwani', 'Shankman', 'Sharp', 'Shaul', 'Sheck', 'Sheive', 'Sheltra', 'Sherfey', 'Shetler', 'Shifflett', 'Shimkus', 'Shiplet', 'Shiyou', 'Shones', 'Shoulars', 'Shriver', 'Shuler', 'Shusterman', 'Sic', 'Sideris', 'Siegfreid', 'Sievers', 'Siker', 'Siller', 'Silvi', 'Simko', 'Simpelo', 'Singh', 'Sioma', 'Sirna', 'Sitar', 'Sivertson', 'Skains', 'Skevofilakas', 'Skogstad', 'Skultety', 'Slatin', 'Slemmons', 'Sloane', 'Sluder', 'Smeathers', 'Smither', 'Smulik', 'Snellen', 'Snyder', 'Sochocki', 'Sogol', 'Solas', 'Solle', 'Somayor', 'Songer', 'Sopha', 'Soroka', 'Sothen', 'Southall', 'Sowl', 'Spallina', 'Spartichino', 'Speed', 'Spera', 'Spiegle', 'Spinello', 'Splatt', 'Spracklen', 'Springer', 'Spunt', 'Staal', 'Staebler', 'Stain', 'Stam', 'Stancoven', 'Stangl', 'Stapel', 'Starnes', 'Stathis', 'Stayner', 'Steckline', 'Stefano', 'Steidl', 'Steinhauser', 'Stelluti', 'Stenquist', 'Sterback', 'Steverson', 'Stidam', 'Stille', 'Stinger', 'Stjuste', 'Stoddard', 'Stohlton', 'Stoltzman', 'Stopka', 'Stotler', 'Stpaul', 'Strangstalien', 'Strawberry', 'Streich', 'Strictland', 'Stroh', 'Strough', 'Strzelecki', 'Studwell', 'Stupak', 'Stvil', 'Sucre', 'Sugar', 'Sulikowski', 'Sumers', 'Sundborg', 'Sur', 'Susany', 'Suttin', 'Swaggert', 'Swanzy', 'Swearengin', 'Swehla', 'Swiger', 'Swoager', 'Sylvia', 'Szaflarski', 'Szopinski', 'Tabeling', 'Tadd', 'Taglieri', 'Takeshita', 'Talley', 'Tammen', 'Tanke', 'Tapia', 'Tarin', 'Taruc', 'Taton', 'Tavenner', 'Teague', 'Teehan', 'Teitsworth', 'Temby', 'Tennant', 'Teravainen', 'Terrell', 'Tess', 'Tewari', 'Thammavong', 'Theiling', 'Thi', 'Thilmony', 'Thompkins', 'Thornley', 'Thronton', 'Thy', 'Tiefenauer', 'Tigue', 'Timbrook', 'Tindol', 'Tipold', 'Tiso', 'Toalson', 'Todora', 'Tokunaga', 'Tolontino', 'Tomichek', 'Tongate', 'Toone', 'Torain', 'Torongeau', 'Tortu', 'Toudle', 'Towley', 'Tradup', 'Trank', 'Traves', 'Trefethen', 'Trench', 'Trevathan', 'Tricoche', 'Trinh', 'Trnka', 'Trombino', 'Troutman', 'Trueheart', 'Trupia', 'Tscrious', 'Tucciarone', 'Tuite', 'Tunget', 'Turdo', 'Turnmire', 'Tuter', 'Twilley', 'Tynan', 'Uchida', 'Uhrig', 'Ulsamer', 'Underhill', 'Uong', 'Urbany', 'Urquidi', 'Utsey', 'Vaci', 'Val', 'Valenzuela', 'Vallerand', 'Vanalphen', 'Vancleave', 'Vanderark', 'Vanderroest', 'Vandeweert', 'Vanepps', 'Vanhoesen', 'Vanloh', 'Vanosdol', 'Vanstone', 'Vanwingerden', 'Vargason', 'Varvel', 'Vastine', 'Veach', 'Vein', 'Velotta', 'Venier', 'Vera', 'Verges', 'Vero', 'Veshedsky', 'Viard', 'Vidal', 'Viesca', 'Vilandre', 'Villamarin', 'Villescas', 'Vinson', 'Virrey', 'Viteaux', 'Vivona', 'Voetberg', 'Volek', 'Vonallmen', 'Voorheis', 'Voth', 'Vukich', 'Waddell', 'Wagenheim', 'Waiau', 'Wakins', 'Waldram', 'Walkowski', 'Wally', 'Walton', 'Wangler', 'Wardian', 'Warmoth', 'Wartchow', 'Waskom', 'Waterworth', 'Wawers', 'Wearing', 'Wedd', 'Weers', 'Weiand', 'Weikert', 'Weirather', 'Weissman', 'Weller', 'Wende', 'Wensman', 'Wernicki', 'Wesselhoft', 'Westermeier', 'Wetherington', 'Whan', 'Whetstine', 'Whit', 'Whitesel', 'Whitted', 'Wiatr', 'Wicks', 'Wiechec', 'Wiens', 'Wiggett', 'Wilcinski', 'Wiles', 'Willaims', 'Williamson', 'Willrich', 'Wimbs', 'Windover', 'Wings', 'Winokur', 'Wion', 'Wishard', 'Witcher', 'Witthuhn', 'Wnek', 'Wojcicki', 'Wolff', 'Wolner', 'Wonser', 'Woodling', 'Woolson', 'Wormley', 'Woznick', 'Wrye', 'Wurzbacher', 'Wynes', 'Yacko', 'Yamanaka', 'Yankovitz', 'Yarwood', 'Yearego', 'Yelvington', 'Yett', 'Yokel', 'Yoshi', 'Youngren', 'Yuengling', 'Zabbo', 'Zadorozny', 'Zaiss', 'Zamor', 'Zanotti', 'Zarn', 'Zaxas', 'Zegar', 'Zelenko', 'Zeni', 'Zeschke', 'Ziebarth', 'Ziesman', 'Zingale', 'Zito', 'Zollinger', 'Zozaya', 'Zukof', 'Zurmiller']