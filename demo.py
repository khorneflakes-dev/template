
iduser = None
print(iduser)
def demo2(value):
    global iduser
    if value > 12345:
        iduser = value
    elif value < 12345:
        iduser = 'no encontrado'
    
demo2(123422)

print(iduser)