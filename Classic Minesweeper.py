#Nadine Mohamed 21 decembre 2022
# 21 decembre 2022
#
# Ce programme permet de jouer au demineur classique.


# (1) Generer une grille vide de dimension demandes et l'afficher au joueur.
def grilleVierge(largeur, hauteur):
    
    # Assure que les largeurs et hauteurs sont des entiers positives.
    if largeur < 0 or hauteur < 0:
        print('entrer un chiffre positive')
        
    array = []
    blank = '<img src="http://codeboot.org/images/minesweeper/blank.png">'
    grilleStr = ''
    
    # Cree un tableau dans html et un array correspondant a la grille vide.
    for i in range(hauteur):
        row = []
        grilleStr += '<tr>' 
        for j in range(largeur):
            row.append('blank')
            id = str(i)+str(j)
            
            # String du code html pour inserer des tuile avec un id unique. 
            grilleStr += '<td id="tuile'+id+'" onclick="clic(event,'+str(i)+'.'+str(j)+')">'+blank+'</td>'
        
        array.append(row)
        grilleStr += '</tr>'
    
    # insere un string de toute la grille au innerHTML.
    grilleHtml = document.querySelector('#grille')
    grilleHtml.innerHTML = grilleStr    
    
    return array
#_____________________________________________________________________________#
# (2) Planter des bombs dans une grille vide.
def planterBombes(largeur, hauteur):
    global grille
    grille = grilleVierge(largeur, hauteur)
    bombes = 0
    dim = largeur*hauteur
    
    # Permet de ne pas planter plus de bombes que demandees.
    while bombes < numBombes : 
        pos = math.floor(dim*random())
        
        row = pos//len(grille[0])
        col = pos % len(grille[0])
        
        # Evite de planter une bombe au meme position.
        if grille[row][col] == "mine" or [row,col] == [rTuile, cTuile]:
            continue
            
        grille[row][col] = "mine"
        bombes += 1
        
    return grille
#_____________________________________________________________________________#
# (3) Assigner une valeur en fonction des nombres de bombes adjacents.
def assignerValueur():
    for row in range(hauteur):
        for col in range(largeur) :
            if grille[row][col] == "mine":
                continue
            else:
                grille[row][col] = numBombesAdj(row, col)
#_____________________________________________________________________________#               
# (4) compter le nombre des bombes adjacents a une tuile.             
def numBombesAdj(row, col):
    bombesAdj = 0
    
    # Verifier tuiles adjacents, incluant les diagonales.
    for r in range(max(0,row-1), min(hauteur, (row+1)+1)):
        for c in range(max(0, col-1), min(largeur, (col+1)+1)):
            if r == row and c == col:
                continue    # dont check our original location
            if grille[r][c] == 'mine':
                bombesAdj += 1
                
    return bombesAdj
#_____________________________________________________________________________#
# (5) Creuser une tuile et mettre a jour memoire des tuiles creuses
def creuser(row, col):
    global tuilesOverts
    mineRouge = '<img src="http://codeboot.org/images/minesweeper/mine-red.png">'
    
    # Change l'image d'une mine cachee lorsqu'elle est creusee.
    tuile = document.querySelector('#tuile'+ str(row)+str(col))
    tuile.innerHTML = '<img src="http://codeboot.org/images/minesweeper/'+str(grille[row][col])+'.png">'
    
    # Met fin a la boucle recursive si une bombe est creuse.
    if grille[row][col] == "mine":
        tuile = document.querySelector('#tuile'+ str(row)+str(col))
        tuile.innerHTML = mineRouge
        return False
    
    # Sauvegare en memoire a chque fois une tuile est creusee.
    tuilesOuverts.append([row,col])
    
    # Si n'est adjacente a aucune bombe.
    if grille[row][col] > 0:
        return True
    
    # Creuser recursivement jusqu'a une tuile adjacente a une bombe est creuse.
    if grille[row][col] == 0:
        for r in range(max(0,row-1), min(len(grille), (row+1)+1)):
            for c in range(max(0, col-1), min(len(grille[0]), (col+1)+1)):
                if [r,c] in tuilesOuverts:
                    continue
                creuser(r,c)
            
    return True
#_____________________________________________________________________________#
#(8)
def jouer(row, col) :
    global tuilesOuverts, safe, grille
    Safe = True
    tuilesOuverts = [row, col]
    mineRouge = '<img src="http://codeboot.org/images/minesweeper/mine-red-x.png">'
    
    # Plante les bombes et demarre le jeu suite au premier clic.
    if clics == 1 : 
        grille = planterBombes(largeur, hauteur)
        assignerValueur()
        
    # Continue a creuser jusqu'au prochain tuile adjacent a une bombe et tanque
    # jouer est vivant.
    while len(tuilesOuverts) < largeur*hauteur :
        safe = creuser(row, col)
        if not safe :
            break
    
    # Si jouer clic sur une bombe, devoile toute la grille. 
    if not safe :
        print('GAME OVER')
        for i in range(len(grille)):
            for j in range(len(grille[0])):
                
                # Permet d'afficher une mineRouge sans x au dernier clic.
                if [i,j] == [rTuile, cTuile]:
                    continue
                # Affiche une mine rouge avec mine d'une tuile avec drapeau.
                if [i,j] in flags and grille[i][j] == 'mine':
                    tuile = document.querySelector('#tuile'+ str(i)+str(j))
                    tuile.innerHTML = mineRouge
                    continue
                # Si pas une mine, affiche sa valeur respective ou blank.   
                tuile = document.querySelector('#tuile'+ str(i)+str(j))
                tuile.innerHTML = '<img src="http://codeboot.org/images/minesweeper/'+str(grille[i][j])+'.png">'
     
    # Signale au joueur qu'il viens de gagner.
    #if len(tuilesOuverts) = 
#_____________________________________________________________________________#
#(7) Initialiser le script html et affiche une grille vide.
def init(x, y):
    global grilleVide, flags, largeur, hauteur, clics
    largeur = x
    hauteur = y
    clics = 0
    flags = []
    
    #evite de repeter de copier les liens des images.
    global blank, flag, mine, mineRouge, mineRougeX
    main = document.querySelector('#main')

    main.innerHTML = """
      <style>
      #main table {
        border: 1px solid black;
        margin: 10px;
      }
      #main table td {
        width: 30px;
        height: 30px;
        border: none;
      }
      </style>
      
      <link rel="preload" href="http://codeboot.org/images/minesweeper/0.png">
      <link rel="preload" href="http://codeboot.org/images/minesweeper/1.png">
      <link rel="preload" href="http://codeboot.org/images/minesweeper/2.png">
      <link rel="preload" href="http://codeboot.org/images/minesweeper/3.png">
      <link rel="preload" href="http://codeboot.org/images/minesweeper/4.png">
      <link rel="preload" href="http://codeboot.org/images/minesweeper/5.png">
      <link rel="preload" href="http://codeboot.org/images/minesweeper/6.png">
      <link rel="preload" href="http://codeboot.org/images/minesweeper/7.png">
      <link rel="preload" href="http://codeboot.org/images/minesweeper/8.png">
      <link rel="preload" href="http://codeboot.org/images/minesweeper/blank.png">
      <link rel="preload" href="http://codeboot.org/images/minesweeper/flag.png">
      <link rel="preload" href="http://codeboot.org/images/minesweeper/mine.png">
      <link rel="preload" href="http://codeboot.org/images/minesweeper/mine-red.png">
      <link rel="preload" href="http://codeboot.org/images/minesweeper/mine-red-x.png">

      
      <table id="grille"></table>"""
    
    # Generer une nouvelle grille SANS bombes
    grilleVide = grilleVierge(largeur, hauteur) 
#_____________________________________________________________________________#
#(8) fonction pour clicker

def clic(event, idTuile):
    global rTuile, cTuile, clics
    rTuile = int(str(idTuile)[0])
    cTuile = int(str(idTuile)[-1])
    blank = '<img src="http://codeboot.org/images/minesweeper/blank.png">'
    flag = '<img src="http://codeboot.org/images/minesweeper/flag.png">'
    # Assure que le premiere clic affiche une grille vide
    clics += 1
    
    # Permet de marquer et demarquer une tuille avec un drapeau
    if event.shiftKey and clics > 1 :
        if [rTuile, cTuile] in tuilesOuverts:
            return False
        # Si tuile deja marque, un deuxieme shit+clic le demarque.
        if [rTuile, cTuile] in flags:
            tuile = document.querySelector("#tuile"+str(rTuile)+str(cTuile))
            tuile.innerHTML = blank
            return True
        # Ajoute les coordonnees de la tuile marquee a une memoire.
        tuile = document.querySelector("#tuile"+str(rTuile)+str(cTuile))
        tuile.innerHTML = flag
        flags.append([rTuile, cTuile])
    
    # Demarre la boucle de jeu apres un clic.
    else:
        jouer(rTuile, cTuile)
#_____________________________________________________________________________#
hauteur = 10
largeur = 8
numBombes = 8
init(largeur, hauteur)



# Tests unitaires
def testGrilleVierge():
    assert grilleVierge(2, 2) == [['blank', 'blank'], ['blank', 'blank']]
    assert grilleVierge(1,1) == [['blank']]
    assert grilleVierge(0,0) == []
    assert grilleVierge(0,0) == print('entrer un chiffre positive')
    

# Tester si une bombe ne se plante au position du premier clic
def testPlanterBombes():
    numBombes = 4
    rTuile = 1
    cTruile = 1
    assert planterBombes(2, 2)[1,1] != 'mine'


# Ce fonctionne teste le bon compte est fait et remplce dans la grille.              
def testAssignerValueBombesAdj():
    largeur = 2
    hauteur = 2
    grille = [['mine','blank'],['blank','mine']]
    assert assignerValueur() == [['mine', 2], [2, 'mine']]


def testCreuser():
    grille = [['mine', 1, 0], 
              [1, 1, 0], 
              [0, 0, 0]]
    tuilesOuverts = []
    # tester si creuser une mine
    creuser(2,2)
    assert [0,0] not in tuilesOuverts
    assert creuser(0,0) == False
    # tester si toiles creuses vont au memoire. 
    assert creuser(1,2) == True
    # tester si recursion fonctione.
    assert tuilesOuverts == [[1, 2], [0, 1], [0, 2], [1, 1], [2, 1], [1, 0], 
                             [2, 0], [2, 2]]

def testJouer():
    clics = 2
    largeur = 3
    hauteur = 3
    rTuile = 0
    cTuile = 0
    flags = []
    grille = [['mine', 1, 0], 
              [1, 1, 0], 
              [0, 0, 0]]
    
    # tester si creuse sur mine met fin au jeu
    assert jouer(0,0) == print('GAME OVER')



