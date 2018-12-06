# (size, board)
def pgmToBoard(file_loc: str) -> (int, [[int]]):
    mapp = []
    size = 0
    with open(file_loc, 'rb') as f:
        lines = f.readlines()
        size = int(lines[1].split()[0])
        bits = str(lines[3].split()[0])
        
        # remove b
        bits = bits[2:]
        bits = bits.split('\\')
        bits = bits[1:]

        # parse
        subMap = []
        y = 0
        x = 0
        for b in bits:
            symb = 0 if b[1:2] == '0' else 1
            subMap.append(symb)

            x += 1
            if x > size - 1:
                mapp.append(subMap)
                x = 0
                y += 1
                subMap = []
        f.close()
    return (size, mapp)