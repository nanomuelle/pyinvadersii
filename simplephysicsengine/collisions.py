def checkCollision(body1, body2):
    (l1, t1, r1, b1) = body1.getLTRB()
    (l2, t2, r2, b2) = body2.getLTRB()
    
    return (l1 > l2 and l1 < r2 and t1 > t2 and t1 < b2) or (l2 > l1 and l2 < r1 and t2 > t1 and t2 < b1)

def checkCollisions( group1, group2 ):
    collisions = []
    for body1 in group1:
        for body2 in group2:
            if checkCollision(body1, body2):
                collisions.append( (body1, body2 ) )
    return collisions