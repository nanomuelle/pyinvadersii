def checkCollision(body1, body2):
    pos1 = body1.pos
    size1 = body1.size

    pos2 = body2.pos
    size2 = body2.size

    return pos1[0] < pos2[0].x + size2[0] and pos1[0] + size1[0] > pos2[0] and pos1[1] < pos2[1] + size2[1] and pos1[1] + size1[1] > size2[1]

def checkCollisions( group1, group2 ):
    collisions = []
    for body1 in group1:
        for body2 in group2:
            if checkCollision(body1, body2):
                collisions.append( (body1, body2 ) )
    return collisions